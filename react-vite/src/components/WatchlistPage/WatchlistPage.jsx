import { useEffect, useState, useRef, useCallback } from 'react';
import { createChart, CrosshairMode } from 'lightweight-charts';

const WatchlistPage = () => {

    const [watchlist, setWatchlist] = useState([]);

    const webSocketRefs = useRef({});
    const chartRefs = useRef({});

    useEffect(() => {
        fetchWatchlist();
        return () => {
            Object.values(webSocketRefs.current).forEach(ws => ws && ws.close());
        };
    }, []);

    useEffect(() => {
        watchlist.forEach(stock => {
            if (!chartRefs.current[stock.symbol]) {
                initChart(stock.symbol);
            }
        });
    }, [watchlist]);// Re-run when watchlist changes

    const fetchCandlestickData = useCallback((symbol, candleSeries) => {
        const ws = new WebSocket('wss://delayed.polygon.io/stocks');
        webSocketRefs.current[symbol] = ws;


        ws.onopen = () => {
            console.log('WebSocket Connected');
            ws.send(JSON.stringify({ action: "auth", params: 'unLg31iXhM99E5yWodIRsOe3pugcBLnl' }));
            ws.send(JSON.stringify({ action: "subscribe", params: `A.${symbol}` }));
        };

        ws.onmessage = (event) => {
            console.log('WebSocket message received:', event.data);
            const messages = JSON.parse(event.data);

            messages.forEach(message => {
                if (message.ev && message.ev === 'A') { // Check for the correct event type for data messages
                    // We'll assume 'data.s' is the timestamp in an acceptable format
                    const newTimestamp = Math.floor(new Date(message.s).getTime() / 1000);
                    const newCandlestickData = {
                        time: newTimestamp,
                        open: message.o,
                        high: message.h,
                        low: message.l,
                        close: message.c,
                    };
                    candleSeries.update(newCandlestickData); // Update the chart with the new data
            }
        })
    }
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        ws.onclose = () => {
            console.log('WebSocket disconnected');
        };
    });

    const initChart = useCallback((symbol) => {
        const chartContainer = document.getElementById(`chart-container-${symbol}`);
        if (chartContainer) {
            const chart = createChart(chartContainer, {
                width: chartContainer.offsetWidth,
                height: 300,
                layout: {
                    backgroundColor: '#FFFFFF',
                    textColor: '#333',
                },
                grid: {
                    vertLines: {
                        color: '#ECECEC',
                    },
                    horzLines: {
                        color: '#ECECEC',
                    },
                },
                priceScale: {
                    borderVisible: false,
                },
                timeScale: {
                    borderVisible: false,
                },
                crosshair: {
                    mode: CrosshairMode.Normal,
                },
            });
            const candleSeries = chart.addCandlestickSeries();
            chartRefs.current[symbol] = chart; // Store the chart instance
            fetchCandlestickData(symbol, candleSeries);
        }
    }, [fetchCandlestickData]);



    const fetchWatchlist = async () => {
        try {
            const response = await fetch('/api/watchlist/', {
                method: 'GET',
                credentials: 'include'
            });
            const data = await response.json();
            console.log(data)


            if (Array.isArray(data)) {
                setWatchlist(data);
            }

            else if (typeof data === 'object') {
                // Example case where the watchlist is under a 'watchlist' property
                if (Array.isArray(data.watchlist)) {
                    setWatchlist(data.watchlist);
                }

                else {
                    setWatchlist([data]);
                }
            }

            else {
                console.error("Unexpected data type received from /api/watchlist:", data);
                setWatchlist([]);
            }
        } catch (error) {
            console.error("Failed to fetch watchlist:", error);
            setWatchlist([]);
        }
    };


    // useEffect(() => {
    //     watchlist.forEach(stock => {
    //         if (stock.symbol && !chartContainersRefs.current[stock.symbol]) {
    //             // Initialize chart for each stock
    //             initChart(stock.symbol);
    //         }
    //     });
    // }, [watchlist, initChart]);




    return (
        <div>
            <h2>My Watchlist</h2>
            {watchlist.map((stock, index) => (
                <div key={stock.symbol}>
                    <h3>{`Stock ${index + 1}: ${stock.symbol}`}</h3>
                    <p>Symbol: {stock.symbol}</p>
                    <p>Name: {stock.name}</p>
                    <p>Price: {stock.price}</p>
                    <div id={`chart-container-${stock.symbol}`} style={{ height: '300px' }}></div>
                </div>
            ))}
        </div>
    );
};

export default WatchlistPage;
