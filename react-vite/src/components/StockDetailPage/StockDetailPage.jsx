import { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Line } from 'react-chartjs-2';
import { createChart, CrosshairMode } from 'lightweight-charts';
import { useSelector } from 'react-redux';
import 'chart.js/auto';
import './StockDetail.css'

const StockDetailPage = () => {
    const { stockSymbol } = useParams();
    const chartContainerRef = useRef(null);
    const [stockData, setStockData] = useState({ prices: [], timestamps: [], candlestickData: [] });
    const [chart, setChart] = useState(null);
    const [series, setSeries] = useState(null);
    const [articles, setArticles] = useState([]);
    const [commentText, setCommentText] = useState('');
    const [articleIdForComment, setArticleIdForComment] = useState(null);
    const [commentsByArticleId, setCommentsByArticleId] = useState({});
    const [editingComment, setEditingComment] = useState({ id: null, text: "" });
    const currentUser = useSelector((state) => state.session.user);
    const [historicalData, setHistoricalData] = useState({ prices: [], dates: [] });



    useEffect(() => {
        const fetchHistoricalData = async () => {
          const endDate = new Date();
          const startDate = new Date();
          startDate.setDate(endDate.getDate() - 14); // Fetching data for the last 14 days

          const from = startDate.toISOString().split('T')[0];
          const to = endDate.toISOString().split('T')[0];
          const url = `https://api.polygon.io/v2/aggs/ticker/${stockSymbol}/range/1/day/${from}/${to}?adjusted=true&sort=asc&apiKey=unLg31iXhM99E5yWodIRsOe3pugcBLnl`;

          try {
            const response = await fetch(url);
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            const data = await response.json();
            const prices = data.results.map(d => d.c);
            const dates = data.results.map(d => new Date(d.t).toISOString().split('T')[0]);

            setHistoricalData({
              prices,
              dates
            });
          } catch (error) {
            console.error('Failed to fetch historical data:', error);
          }
        };

        fetchHistoricalData();
      }, [stockSymbol]); // Re-fetch when stockSymbol changes

      // Data for the line chart
      const lineChartData = {
        labels: historicalData.dates,
        datasets: [
          {
            label: `${stockSymbol} Closing Price`,
            data: historicalData.prices,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }
        ]
      };



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
                    const newTimestamp = Math.floor(new Date(message.s).getTime() / 1000);
                    const newCandlestickData = {
                        time: newTimestamp,
                        open: message.o,
                        high: message.h,
                        low: message.l,
                        close: message.c,
                    };


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




        return () => {
            if (websocket.readyState === WebSocket.OPEN) {
                websocket.send(JSON.stringify({ action: "unsubscribe", params: `A.${stockSymbol}` }));
                websocket.close();
            }
        };
    }, [stockSymbol, series]);



    useEffect(() => {
        const fetchArticles = async () => {
            const apiKey = 'unLg31iXhM99E5yWodIRsOe3pugcBLnl'; // Replace with your Polygon API key
            try {
                const response = await fetch(`https://api.polygon.io/v2/reference/news?ticker=${stockSymbol}&order=desc&limit=5&apiKey=${apiKey}`);
                if (!response.ok) throw new Error('Failed to fetch articles');
                const data = await response.json();

                const saveResponse = await fetch('/api/articles/', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ articles: data.results }),
                  });

                   if (!saveResponse.ok) {
                    const saveResponseData = await saveResponse.json(); // Parse JSON to access potential error messages
                    throw new Error('Failed to save articles: ' + (saveResponseData.error || 'Unknown error'));
                }

                // After ensuring articles are saved (or already exist), fetch them from your backend or use the Polygon data directly
                const savedArticlesData = await saveResponse.json(); // Assuming this returns the saved articles or a success message

                // Depending on your backend, this could be the saved articles or you might need to fetch them again
                console.log(savedArticlesData);
                setArticles(data.results); // Or fetch again from your backend if necessary

                const comments = {};
                for (const article of data.results) {
                    const commentsResponse = await fetch(`/api/comments/${article.id}`);
                    if (commentsResponse.ok) {
                        comments[article.id] = await commentsResponse.json();
                    } else {
                        comments[article.id] = []; // Ensure we always have an array for each article
                    }
                }
                setCommentsByArticleId(comments);

            } catch (error) {
                console.error("Error:", error);
            }
        };

        fetchArticles();
    }, [stockSymbol]);



      // Function to add stock to watchlist
      async function addToWatchlist(stockSymbol, category = 'default') {
        try {
            function getCSRFToken() {
                const cookieString = document.cookie;
                console.log('Cookie string:', cookieString);
                if (cookieString) {
                    const cookies = cookieString.split('; ');
                    for (const cookie of cookies) {
                        const [name, value] = cookie.split('=');
                        if (name.trim() === 'csrf_token') {
                            console.log('CSRF token:', value);
                            return value;
                        }
                    }
                }
                return null;
            }

            const csrfToken = getCSRFToken();

            if (!csrfToken) {
                throw new Error('CSRF token not found');
            }

            await fetch("/api/watchlist", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    stock_id: stockSymbol,
                    category: category
                })
            });

        } catch (error) {
            console.error('Error adding to watchlist:', error);
        }
    }

    const handleAddComment = async (e) => {
        e.preventDefault();

        const commentPayload = {
            article_id: articleIdForComment,
            comment_text: commentText,
        };

        const url = editingComment.id ? `/api/comments/${editingComment.id}` : '/api/comments';
        const method = editingComment.id ? 'PUT' : 'POST';

        if (!articleIdForComment) {
            console.error('Article ID for commenting is not set.');
            return;
        }

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(commentPayload),
            });
            if (!response.ok) throw new Error('Network response was not ok.');

            // Fetch the updated comments after submitting or updating a comment
        const updatedCommentsResponse = await fetch(`/api/comments/${articleIdForComment}`);
        if (!updatedCommentsResponse.ok) throw new Error('Failed to fetch updated comments.');

        const updatedComments = await updatedCommentsResponse.json();

        // Update the local state with the fetched updated comments
        setCommentsByArticleId(prev => ({
            ...prev,
            [articleIdForComment]: updatedComments,
        }));

            // Reset form and editing state
            setCommentText('');
            setEditingComment({ id: null, text: "" });
            setArticleIdForComment(null); // Reset articleIdForComment after submitting the comment
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const startEditComment = (articleId, comment) => {
        setArticleIdForComment(articleId);
        setEditingComment({ id: comment.id, text: comment.text });
        setCommentText(comment.text);
    };
    const handleDeleteComment = async (articleId, commentId) => {
        try {
            const response = await fetch(`/api/comments/${commentId}`, {
                method: 'DELETE',
            });
            if (!response.ok) throw new Error('Network response was not ok.');

            // Remove the deleted comment from the state
            setCommentsByArticleId(prev => ({
                ...prev,
                [articleId]: prev[articleId].filter(comment => comment.id !== commentId),
            }));
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleCancelEdit = () => {

        // Proceed with canceling the edit as before
        setEditingComment({ id: null, text: "" });
        setCommentText('');
        setArticleIdForComment(null); // Optional
    };

    return (
        <div className="container">
    <h2 className="heading">Stock Details for {stockSymbol}</h2>
    <div className="charts-container">
    <div className="chart-container">

        <div className="line-chart-container">
        {stockData.prices.length > 0 ? (
                     <Line data={lineChartData} style={{ width: '500px', height: '300px' }}/>
                ) : (
                    <p>No line chart data available.</p>
                )}
    </div>
    </div>
    <div className="chart-container">
        <div ref={chartContainerRef} className="chart" style={{ width: '400px', height: '250px' }}></div>
        <button onClick={() => addToWatchlist(stockSymbol)}>Add to Watchlist</button>
    </div>
    </div>
    <div className="articles-container">
        <h2 className="heading">Latest Articles for {stockSymbol}</h2>
        <ul className="list">
            {articles.map(article => (
                <li key={article.id} className="list-item">
                    <div className="article-info">
                        {/* Include image if available */}
                        <img src={article.image_url} alt={article.title} />
                        <a href={article.article_url} target="_blank" rel="noopener noreferrer">{article.title}</a>
                        <button onClick={() => setArticleIdForComment(article.id)}>Add Comment</button>
                        {articleIdForComment === article.id && (
                                     <form onSubmit={handleAddComment} style={{ marginTop: '20px' }}>
                                     <textarea
                                         value={commentText}
                                         onChange={(e) => setCommentText(e.target.value)}
                                         placeholder="Write your comment here"
                                         style={{ display: 'block', width: '100%', marginBottom: '10px' }}
                                     />
                                     <button type="submit">{editingComment.id ? 'Update Comment' : 'Submit Comment'}</button>
    <button type="button" onClick={handleCancelEdit} style={{ marginLeft: '10px' }}>Cancel</button> {/* Add this line */}
                                 </form>
                                )}
                                 <div className="comments">
                                 {commentsByArticleId[article.id] && commentsByArticleId[article.id].map((comment, index) => (
   <div key={`${comment.id}_${index}`}>
   <p>{comment.text}</p>
   {currentUser && currentUser.id === comment.user_id && (
    <>
        <button onClick={() => startEditComment(article.id, comment)}>Edit</button>
        <button onClick={() => handleDeleteComment(article.id, comment.id)}>Delete</button>
    </>
)}
</div>
))}
            </div>
                </div>
                </li>
            ))}

        </ul>
    </div>
</div>

    );
};

export default StockDetailPage;
