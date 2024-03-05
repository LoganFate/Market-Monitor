import { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';



const StockDetailPage = () => {
    const { stockSymbol } = useParams();
    const [stockData, setStockData] = useState({ prices: [], timestamps: [] });
    const [chartData, setChartData] = useState({});
    const [ws, setWs] = useState(null);
    const chartRef = useRef(null);

    useEffect(() => {
        setStockData({ prices: [], timestamps: [] });

        if (ws) {
            // Unsubscribe from the previous symbol's updates
            ws.send(JSON.stringify({ action: "unsubscribe", params: `A.${stockSymbol}` }));
        }


        const websocket = new WebSocket('wss://delayed.polygon.io/stocks');
        setWs(websocket);

        websocket.onopen = () => {
            console.log('WebSocket Connected');
            // Immediately authenticate and subscribe upon connection
            const apiKey = 'unLg31iXhM99E5yWodIRsOe3pugcBLnl'; // Ensure you use the correct way to access your API key
            websocket.send(JSON.stringify({ action: "auth", params: apiKey }));
            websocket.send(JSON.stringify({ action: "subscribe", params: `A.${stockSymbol}` }));
        };

        websocket.onmessage = (event) => {
            console.log('WebSocket message received:', event.data);
            const messages = JSON.parse(event.data);
            messages.forEach(message => {
                if (message.ev && message.ev === 'A') {
                    const newTimestamp = new Date(message.s).toLocaleTimeString();
                    setStockData(prevData => ({
                        prices: [...prevData.prices, message.c],
                        timestamps: [...prevData.timestamps, newTimestamp].slice(-60),
                    }));
                }
            });
        };
        // Clean up on component unmount
        return () => {
            if (ws && ws.readyState === WebSocket.OPEN) {
                websocket.send(JSON.stringify({ action: "unsubscribe", params: `A.${stockSymbol}` }));
                ws.close();
            }
        };
    }, [stockSymbol]);

    useEffect(() => {
        if (chartRef.current) {
            chartRef.current.data.labels = stockData.timestamps;
            chartRef.current.data.datasets[0].data = stockData.prices;
            chartRef.current.update();
        } else {
            // Initialize the chart data
            setChartData({
                labels: stockData.timestamps,
                datasets: [{
                    label: `${stockSymbol} Stock Price`,
                    data: stockData.prices,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            });
        }
    }, [stockData, stockSymbol]);
    // Attempt to send a ping every second, but only if the WebSocket is open
    // useEffect(() => {
    //     const pingInterval = setInterval(() => {
    //         if (ws && ws.readyState === WebSocket.OPEN) {
    //             ws.send(JSON.stringify({ action: "ping" }));
    //         }
    //     }, 15 * 60 * 1000); // Ping every second

    //     return () => clearInterval(pingInterval);
    // }, [ws]);

    // console.log('Current stockData state:', stockData);

    return (
        <div>
            <h2>Stock Details for {stockSymbol}</h2>
            {stockData.prices.length > 0 ? <Line data={chartData} /> : <p>No data available.</p>}
        </div>
    );
};

export default StockDetailPage;
