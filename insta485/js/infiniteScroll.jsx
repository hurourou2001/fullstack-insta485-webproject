import { useState, useEffect } from 'react';
import Post from "./post";

export const useInfiniteScroll = (initialUrl) => {
    const [items, setItems] = useState([]);
    const [nextUrl, setNextUrl] = useState(initialUrl);
    const [hasMore, setHasMore] = useState(true);
    const [loading, setLoading] = useState(false);
    const [xx, setxx] = useState(true);

    // const fetchPostDetail = async (url) => {
    //     try {
    //         const response = await fetch(url,{
    //             method: 'GET',
    //             credentials: 'same-origin',
    //         });
    //         if(!response.ok) throw new Error('Failed to fetch post details');
    //         const postData = await response.json();
    //         return postData;
    //     } catch (error) {
    //         console.error('Error fetching post details ', error);
    //         return null;
    //     }
    // };

    const fetchItems = async () => {
        if (!nextUrl || loading || !xx) return;

        setLoading(true);
        console.log(nextUrl)
        //try {

        //     const response = await fetch(nextUrl, {
        //         method: 'GET',
        //         credentials: 'same-origin',
        //     });
        //     const posts = await response.json();
            
        //     // Fetch the details for each post in parallel using Promise.all
        //     const postDetails = await Promise.all(
        //         posts.results.map((post) => fetchPostDetail(post.url))
        //     );
            
        //     // Filter out any null results (failed fetches)
        //     const validPosts = postDetails.filter((post) => post !== null);
        //     console.log(validPosts)
        //     setItems((prevItems) => [...prevItems, ...validPosts]);
        //     setNextUrl(posts.next || null);
        //     setHasMore(!!posts.next); //if there is no next URL, stop loading more
        //     setLoading(false);
        // }  catch(error) {
        //     console.error('Error fetching items: ', error);
        //     setLoading(false);
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
    }, []);
    return { items, fetchItems, hasMore, loading};
};
