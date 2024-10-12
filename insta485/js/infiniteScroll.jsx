import { useState, useEffect, useCallback } from "react";

const useInfiniteScroll = (initialUrl) => {
  const [items, setItems] = useState([]);
  const [nextUrl, setNextUrl] = useState(initialUrl);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);
  const [xx, setXx] = useState(false);

  const fetchItems = useCallback(async () => {
    if (!nextUrl || loading || !xx) return;

    setLoading(true);
    console.log(nextUrl);

    fetch(nextUrl, {
      method: "GET",
      credentials: "same-origin",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        setItems((prevItems) => [...prevItems, ...data.results]);
        console.log(nextUrl);
        setNextUrl(data.next);
        setHasMore(!!data.next);
        setLoading(false);
        setXx(false);
        console.log(nextUrl);
      })
      .catch((error) => console.log(error));
  }, [nextUrl, loading, xx]); // Add dependencies here to avoid unnecessary re-creation

  useEffect(() => {
    console.log("useEffect triggered, loading:", loading, "nextUrl:", nextUrl);
    if (nextUrl && hasMore) {
      fetchItems();
      setXx(true);
    }
  }, [nextUrl, hasMore, fetchItems, loading]);

  return { items, fetchItems, hasMore, loading };
};

export default useInfiniteScroll;
