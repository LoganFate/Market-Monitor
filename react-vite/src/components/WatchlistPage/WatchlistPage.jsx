import { useEffect, useState, useRef } from 'react';
import { createChart } from 'lightweight-charts';

const WatchlistPage = () => {

    const [watchlist, setWatchlist] = useState([]);

    const chartContainersRefs = useRef({});
    const webSocketRefs = useRef({});

    useEffect(() => {
        fetchWatchlist();
        // Cleanup WebSockets on component unmount
        return () => {
            Object.values(webSocketRefs.current).forEach(ws => ws && ws.close());
        };
    }, []);


    const fetchWatchlist = async () => {
        try {
            const response = await fetch('/api/watchlist', {
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


    useEffect(() => {
        watchlist.forEach(stock => {
            if (stock.symbol && !chartContainersRefs.current[stock.symbol]) {
                // Initialize chart for each stock
                initChart(stock.symbol);
            }
        });
    }, [watchlist]);

    const initChart = (symbol) => {
        // Dynamically create chart container if not already created
        if (!document.getElementById(`chart-container-${symbol}`)) {
            const chartContainer = document.createElement('div');
            chartContainer.id = `chart-container-${symbol}`;
            chartContainer.style.height = '300px';
            document.body.appendChild(chartContainer);

            const chart = createChart(chartContainer, {
                width: chartContainer.offsetWidth,
                height: 300,
            });
            const candleSeries = chart.addCandlestickSeries();


            chartContainersRefs.current[symbol] = chartContainer;


            fetchCandlestickData(symbol, candleSeries);
        }
    };

    const fetchCandlestickData = (symbol, candleSeries) => {
        const ws = new WebSocket('wss://delayed.polygon.io/stocks');
        webSocketRefs.current[symbol] = ws;

        ws.onopen = () => {
            console.log('WebSocket Connected');
            ws.send(JSON.stringify({ action: "auth", params: 'unLg31iXhM99E5yWodIRsOe3pugcBLnl' }));
            ws.send(JSON.stringify({ action: "subscribe", params: `A.${stockSymbol}` }));
        };

        ws.onmessage = (event) => {
            console.log('WebSocket message received:', event.data);
            const data = JSON.parse(event.data);

            const candlestickData = {
                time: '2024-03-06',
                open: data.open,
                high: data.high,
                low: data.low,
                close: data.close,
            };
            candleSeries.update(candlestickData);
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        ws.onclose = () => {
            console.log('WebSocket disconnected');
        };
    };


    return (
        <div>
            <h2>My Watchlist</h2>
            {watchlist.map((stock, index) => (
                <div key={index}>
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
