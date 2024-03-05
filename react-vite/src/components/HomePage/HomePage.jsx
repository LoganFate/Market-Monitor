import { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import { Line } from 'react-chartjs-2';
import 'chart.js/auto'; // Import to register the controller and elements

function HomePage() {
    const [stocks, setStocks] = useState([]);
    const [articles, setArticles] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [chartData, setChartData] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {

                const stocksResponse = await fetch('/api/stocks');
                const articlesResponse = await fetch('/api/articles');
                if (!stocksResponse.ok || !articlesResponse.ok) {
                    throw new Error('Data could not be fetched');
                }
                const stocksData = await stocksResponse.json();
                const articlesData = await articlesResponse.json();

                setStocks(stocksData);
                setArticles(articlesData);
                // const chartLabels = stocksData.map(stock => stock.date);
                // const chartPrices = stocksData.map(stock => stock.price);
                setChartData({
                    labels: stocksData.map(stock => stock.symbol), // Assuming 'symbol' exists in the stock data
                    datasets: [
                        {
                            label: 'Stock Price',
                            data: stocksData.map(stock => stock.live_close), // Assuming 'live_close' exists in the stock data
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        }
                    ]
                });
            } catch (error) {
                setError(error.message);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 60000);
        return () => clearInterval(interval);
    }, []);

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h2>Featured Stocks</h2>
            {stocks.length > 0 && (
                <div>
                    <Line data={chartData} />
                    <ul>
                        {stocks.map((stock) => (
                            <li key={stock.symbol}>
                                <Link to={`/stock/${stock.symbol}`}>{stock.name}</Link> - ${stock.live_close}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
            <h2>Latest Articles</h2>
            <ul>
                {articles.map(article => (
                    <li key={article.id}>{article.title}</li>
                ))}
            </ul>
        </div>
    );
}

export default HomePage;
