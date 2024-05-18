import { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import './HomePage.css'

function HomePage() {
    const tickers = ['AAPL', 'TSLA', 'GOOGL', 'MSFT']; // Add your tickers here
    const [stocks, setStocks] = useState([]);
    const [articles, setArticles] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [chartData, setChartData] = useState({});
    const apiKey = 'unLg31iXhM99E5yWodIRsOe3pugcBLnl'; // This should be securely handled
    const [articleLimit, setArticleLimit] = useState();
    const [watchlistedStocks, setWatchlistedStocks] = useState([]);
    const [displayLimit, setDisplayLimit] = useState(9);

    useEffect(() => {

        const fetchData = async () => {
            setIsLoading(true);
            try {
                const stocksResponse = await fetch('/api/stocks/');
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
                    const watchlistResponse = await fetch('/api/watchlist/', {
                        credentials: 'include', // Only if your endpoint requires authentication
                    });
                    if (!watchlistResponse.ok) {
                        throw new Error('Failed to fetch watchlist');
                    }
                    const watchlistData = await watchlistResponse.json();

                    // Assuming watchlistData is an array of stock objects, adjust if necessary
                    const watchlistSymbols = watchlistData.map(stock => stock.symbol);
                    setWatchlistedStocks(watchlistSymbols);

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

    async function fetchStockIdBySymbol(stockSymbol) {
        const response = await fetch(`/api/stocks/${stockSymbol}`);
        if (!response.ok) {
            throw new Error('Failed to fetch stock ID');
        }
        const data = await response.json();
        return data.id; // Adjust based on how your API responds
    }

    async function addToWatchlist(stockSymbol) {
        try {
            // Fetch the stock ID using the stock symbol
            const stockId = await fetchStockIdBySymbol(stockSymbol);
            if (!stockId) {
                console.error(`Could not find stock ID for symbol: ${stockSymbol}`);
                alert('Stock ID not found');
                return;
            }

            // Then, make the request to add the stock to the watchlist with the fetched stock ID
            const response = await fetch('/api/watchlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                credentials: 'include', // Only if your endpoint requires authentication
                body: JSON.stringify({
                    stock_id: stockId,
                    category: 'default' // Or any other category you wish to specify
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to add to watchlist');
            }

            // Provide feedback to the user
            setWatchlistedStocks(current => [...current, stockSymbol]);

        } catch (error) {
            console.error("Error adding to watchlist:", error);

        }
    }


    if (isLoading) return (
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      );
    if (error) return <div>Error: {error}</div>;

    // const fetchArticleIdByTitle = async (title) => {
    //     try {
    //         const response = await fetch(`/api/articles/title/${encodeURIComponent(title)}`);
    //         if (!response.ok) {
    //             throw new Error('Failed to fetch article ID');
    //         }
    //         const article = await response.json();
    //         return article.id;  // Assuming the backend returns the article's ID in its response
    //     } catch (error) {
    //         console.error("Error fetching article ID by title:", error);
    //         return null;  // Handle the error appropriately
    //     }
    // };

    // const pinArticle = async (articleId, category = 'default') => {
    //     try {
    //         const response = await fetch('/api/pinned', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             },
    //             credentials: 'include',
    //             body: JSON.stringify({ article_id: articleId, category }),
    //         });
    //         if (!response.ok) {
    //             const errorData = await response.json();
    //             throw new Error(errorData.error || 'Failed to pin article');
    //         }
    //         console.log('Article pinned successfully');
    //         // Optionally, update your state/UI to reflect the pinning
    //     } catch (error) {
    //         console.error("Error pinning article:", error.message);
    //     }
    // };

    // const handlePinArticleByTitle = async (articleTitle) => {
    //     try {
    //         const articleId = await fetchArticleIdByTitle(articleTitle);
    //         if (articleId) {
    //             await pinArticle(articleId);
    //             console.log('Article pinned successfully');
    //             // Update UI/state as needed
    //         } else {
    //             console.error("Could not find article to pin.");
    //         }
    //     } catch (error) {
    //         console.error("Error during pinning process:", error);
    //     }
    // };

    const loadMoreStocks = () => {
        setDisplayLimit(prevLimit => prevLimit + 9); // Load 9 more stocks
      };


    return (
        <div className="container">
        <h2 className="heading">Featured Stocks</h2>
        {stocks.length > 0 && (
                <div>
                    <div className="chart-container">
                        <Line data={chartData} options={{
        responsive: true,
        maintainAspectRatio: false,
        // Any additional options...
    }}  />
                    </div>
                    <div className="stock-container">
                    <ul className="list stock-list">
                    {stocks.slice(0, displayLimit).map(stock => (
                            <li key={stock.symbol} className="home-list-item">
                                <Link to={`/stock/${stock.symbol}`}>{stock.name}</Link> - ${stock.live_close}
                                {!watchlistedStocks.includes(stock.symbol) && (
            <button onClick={() => addToWatchlist(stock.symbol)} className="add-to-watchlist-btn">+</button>
        )}
                            </li>
                        ))}
                    </ul>
                    {displayLimit < stocks.length && (
    <button onClick={loadMoreStocks} className="load-more-btn">
      Load More
    </button>
  )}
                    </div>
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
                {/* <button onClick={() => pinArticle(article.id)}>Pin</button> */}
            </div>
        </li>
    ))}
 </ul>
    </div>
    );
}

export default HomePage;
