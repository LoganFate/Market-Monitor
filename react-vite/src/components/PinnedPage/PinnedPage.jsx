// PinnedPage.js
import React, { useEffect, useState } from 'react';

function PinnedPage() {
    const [pinnedArticles, setPinnedArticles] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchPinnedArticles = async () => {
            setIsLoading(true);
            try {
                const response = await fetch('/api/pinned', { credentials: 'include' });
                if (!response.ok) throw new Error('Failed to fetch pinned articles');
                const data = await response.json();
                setPinnedArticles(data);
            } catch (error) {
                console.error("Error fetching pinned articles:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchPinnedArticles();
    }, []);

    if (isLoading) return <div>Loading...</div>;

    return (
        <div>
            <h2>My Pinned Articles</h2>
            <ul className="list">
                {pinnedArticles.map(article => (
                    <li key={article.id} className="home-list-item">
                        <div className="article-info">
                            <a href={article.article_url} target="_blank" rel="noopener noreferrer">{article.title}</a>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default PinnedPage;
