import { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Line } from 'react-chartjs-2';
import { createChart, CrosshairMode } from 'lightweight-charts';
import 'chart.js/auto';


const StockDetailPage = () => {
    const { stockSymbol } = useParams();
    const lineChartContainerRef = useRef(null); // Ref for the line chart container if needed
    const chartContainerRef = useRef(null); // Ref for the Lightweight Chart container
    const [stockData, setStockData] = useState({ prices: [], timestamps: [], candlestickData: [] });
    const [ws, setWs] = useState(null);
    const [chart, setChart] = useState(null);
    const [series, setSeries] = useState(null);

    useEffect(() => {
        // Initialize the chart only once
        if (chartContainerRef.current && !chart) {
            const newChart = createChart(chartContainerRef.current, {
                width: chartContainerRef.current.offsetWidth,
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
                    scaleMargins: {
                        top: 0.1,
                        bottom: 0.25,
                    },
                    borderVisible: false,
                },
                timeScale: {
                    borderVisible: false,
                },
                crosshair: {
                    mode: CrosshairMode.Normal,
                },
            });
            const newSeries = newChart.addCandlestickSeries();
            setChart(newChart);
            setSeries(newSeries);


        return () => {
            newChart.remove();
            setChart(null);
            setSeries(null);
        };
    }
 }, []);


    useEffect(() => {
        const websocket = new WebSocket('wss://delayed.polygon.io/stocks');

        websocket.onopen = () => {
            console.log('WebSocket Connected');
            // Only send messages after the connection is open
            websocket.send(JSON.stringify({ action: "auth", params: 'unLg31iXhM99E5yWodIRsOe3pugcBLnl' }));
            websocket.send(JSON.stringify({ action: "subscribe", params: `A.${stockSymbol}` }));
            const pingInterval = setInterval(() => {
                if (websocket.readyState === WebSocket.OPEN) {
                    websocket.send(JSON.stringify({ action: "ping" }));
                }
            }, 1000);

            // Make sure to clear the interval when the websocket closes
            websocket.onclose = () => clearInterval(pingInterval);
        };
        websocket.onmessage = (event) => {
            console.log('WebSocket message received:', event.data);
            const messages = JSON.parse(event.data);

            messages.forEach(message => {
                if (message.ev && message.ev === 'A') {
                    const newTimestamp = Math.floor(new Date(message.s).getTime() / 1000); // Lightweight Charts uses UNIX timestamp in seconds
                    const newCandlestickData = {
                        time: newTimestamp,
                        open: message.o,
                        high: message.h,
                        low: message.l,
                        close: message.c,
                    };

                    // Update the React state for prices and timestamps
                    setStockData(prevData => ({
                        ...prevData,
                        prices: [...prevData.prices, message.c].slice(-60),
                        timestamps: [...prevData.timestamps, new Date(message.s).toLocaleTimeString()].slice(-60),
                        candlestickData: [...prevData.candlestickData, newCandlestickData].slice(-60)
                    }));

                    // Only try to update the series if it exists
                    if (series) {
                        series.update(newCandlestickData);
                        // chart.timeScale().fitContent();
                    }
                }
            });
        };

        // This cleanup function belongs to the useEffect and ensures WebSocket is closed when component unmounts or stockSymbol changes
        return () => {
            if (websocket.readyState === WebSocket.OPEN) {
                websocket.send(JSON.stringify({ action: "unsubscribe", params: `A.${stockSymbol}` }));
                websocket.close();
            }
        };
    }, [stockSymbol, series]); // Add `series` to useEffect dependencies to ensure it captures the latest series instance.
    // Line chart data setup
    const lineChartData = {
        labels: stockData.timestamps,
        datasets: [{
            label: `${stockSymbol} Stock Price`,
            data: stockData.prices,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
        }],
    };

    return (
        <div>
            <h2>Stock Details for {stockSymbol}</h2>
            <div>
                <h3>Line Chart</h3>
                {stockData.prices.length > 0 ? (
                    <Line data={lineChartData} />
                ) : (
                    <p>No line chart data available.</p>
                )}
            </div>
            <div>
                <h3>Candlestick Chart</h3>
                <div ref={chartContainerRef} style={{ width: '600px', height: '300px' }}></div>
            </div>
        </div>
    );
};

export default StockDetailPage;
