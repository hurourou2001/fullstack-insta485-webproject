import { useState, useEffect } from 'react';
import Post from "./post";

export const useInfiniteScroll = (initialUrl) => {
    const [items, setItems] = useState([]);
    const [nextUrl, setNextUrl] = useState(initialUrl);
    const [hasMore, setHasMore] = useState(true);
    const [loading, setLoading] = useState(false);
    const [xx, setxx] = useState(true);
    
    const fetchItems = async () => {
        console.log('try fetching items')
        if (!nextUrl || loading || !xx) return;
        console.log('fetching items')
        setLoading(true);
        console.log(nextUrl)
    
        fetch(nextUrl, { method: 'GET',
            credentials: 'same-origin'
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            console.log(data.results);
            setItems((prevItems) => [...prevItems, ...data.results]);
            console.log(items);
            setNextUrl(data.next || null);
            setHasMore(!!data.next);
            setLoading(false);
            setxx(false);
        })
        .catch((error) => console.log(error));
    };

    useEffect(() => {
        fetchItems();
        setxx(true);
    }, [nextUrl]);
    return { items, fetchItems, hasMore, loading};
};
