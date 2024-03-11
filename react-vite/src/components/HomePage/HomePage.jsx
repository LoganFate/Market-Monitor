import { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import './HomePage.css'

function HomePage() {
    const tickers = ['AAPL', 'TSLA', 'GOOGL', 'MSFT']; // Add your tickers here
    const [stocks, setStocks] = useState([]);
    const [articles, setArticles] = useState([12]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [chartData, setChartData] = useState({});
    const apiKey = 'unLg31iXhM99E5yWodIRsOe3pugcBLnl'; // This should be securely handled
    const [articleLimit, setArticleLimit] = useState(12);

    useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true);
            try {
                const stocksResponse = await fetch('/api/stocks');
                if (!stocksResponse.ok) {
                    throw new Error('Stock data could not be fetched');
                }
                const stocksData = await stocksResponse.json();

                // Fetch articles for each ticker
                const articlesPromises = tickers.map(ticker =>
                    fetch(`https://api.polygon.io/v2/reference/news?ticker=${ticker}&apiKey=${apiKey}`)
                        .then(response => {
                            if (!response.ok) throw new Error(`Failed to fetch articles for ${ticker}`);
                            return response.json();
                        })
                        .then(data => data.results)
                        .catch(error => console.error(`Error fetching articles for ${ticker}:`, error))
                );

                const articlesResults = await Promise.all(articlesPromises);
                const combinedArticles = articlesResults.flat(); // Combine all articles into one array
 // Filter for unique articles based on their 'id'
                const uniqueArticles = combinedArticles.reduce((acc, current) => {
                 const x = acc.find(item => item.id === current.id);
                 if (!x) {
                   return acc.concat([current]);
                      } else {
                    return acc;
                  }
                    }, []);

                    setStocks(stocksData);
                        setArticles(uniqueArticles);
// Other state updates...
                setChartData({
                    labels: stocksData.map(stock => stock.symbol),
                    datasets: [
                        {
                            label: 'Stock Price',
                            data: stocksData.map(stock => stock.live_close),
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        }
                    ]
                });
            } catch (error) {
                console.error("Error fetching data:", error);
                setError(error.message);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 600000); // Optional: Refetch data every minute
        return () => clearInterval(interval);
    }, []);

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    const fetchArticleIdByTitle = async (title) => {
        try {
            const response = await fetch(`/api/articles/title/${encodeURIComponent(title)}`);
            if (!response.ok) {
                throw new Error('Failed to fetch article ID');
            }
            const article = await response.json();
            return article.id;  // Assuming the backend returns the article's ID in its response
        } catch (error) {
            console.error("Error fetching article ID by title:", error);
            return null;  // Handle the error appropriately
        }
    };

    const pinArticle = async (articleId, category = 'default') => {
        try {
            const response = await fetch('/api/pinned/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ article_id: articleId, category }),
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to pin article');
            }
            console.log('Article pinned successfully');
            // Optionally, update your state/UI to reflect the pinning
        } catch (error) {
            console.error("Error pinning article:", error.message);
        }
    };

    const handlePinArticleByTitle = async (articleTitle) => {
        const articleId = await fetchArticleIdByTitle(articleTitle);
        if (articleId) {
            // Now you have the article ID, and you can proceed to pin the article.
            await pinArticle(articleId);
        } else {
            console.error("Could not find article to pin.");
            // Handle the situation where the article ID couldn't be fetched
        }
    };


    return (
        <div className="container">
        <h2 className="heading">Featured Stocks</h2>
        {stocks.length > 0 && (
                <div>
                    <div className="chart-container">
                        <Line data={chartData} />
                    </div>
                    <ul className="list">
                        {stocks.map(stock => (
                            <li key={stock.symbol} className="home-list-item">
                                <Link to={`/stock/${stock.symbol}`}>{stock.name}</Link> - ${stock.live_close}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        <h2 className="heading">Latest Articles</h2>
        {/* Articles list */}
        <ul className="list">
    {articles.slice(0, articleLimit).map(article => (
        <li key={article.id} className="home-list-item">
            <div className="article-info">
                <img src={article.image_url} alt={article.title} />
                <a href={article.article_url} target="_blank" rel="noopener noreferrer">{article.title}</a>
                <button onClick={() => handlePinArticleByTitle(article.title)}>Pin</button>
            </div>
        </li>
    ))}
 </ul>
    </div>
    );
}

export default HomePage;
