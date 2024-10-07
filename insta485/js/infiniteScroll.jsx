import { useState, useEffect } from 'react';

export const useInfiniteScroll = (initialUrl) => {
    const [items, setItems] = useState([]);
    const [nextUrl, setNextUrl] = useState(initialUrl);
    const [hasMore, setHasMore] = useState(true);
    const [loading, setLoading] = useState(false);

    const fetchItems = () => {
        if (!nextUrl || loading) return;
        
        setLoading(true);
        fetch(nextUrl, {
            method: 'GET',
            credentials: 'same-origin',
        })
        .then((response) => response.json())
        .then((data) => {
            setItems((prevItems) => [...prevItems, ...data.posts]);
            setNextUrl(data.next || null);
            setHasMore(!!data.next); //if there is no next URL, stop loading more
            setLoading(false);
        })
        .catch((error) => {
            console.error('Error fetching items: ', error);
            setLoading(false);
        });
    };

    useEffect(() => {
        fetchItems();
    }, [])
    return { items, fetchItems, hasMore, loading};
};
