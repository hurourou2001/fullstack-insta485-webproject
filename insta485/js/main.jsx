import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Post from "./post";
import InfiniteScroll from "react-infinite-scroll-component";
import { useInfiniteScroll } from './infiniteScroll';

// Create a root
const root = createRoot(document.getElementById("reactEntry"));

// This method is only called once
// Insert the post component into the DOM
root.render(
//   <StrictMode>
    <Main />
//   </StrictMode>
);

export default function Main() {
    const { items: posts, fetchItems: fetchPosts, hasMore, loading} = useInfiniteScroll('/api/v1/posts/');
    console.log(posts)
    return (
        <div className="main-page">
            {loading && posts.length === 0 && (
                <div className="loading-placeholder">
                    <p>Loading posts...</p>
                </div>
            )}

            <InfiniteScroll
                dataLength={posts.length}
                next={fetchPosts}
                hasMore={hasMore}
                loader={<h4>Loading more posts...</h4>}
                endMessage={<p>No more posts to show</p>}
                
            >
                {posts.map((post) => (
                    <Post key={post.postid} posturl={post.url} />
                ))}
            </InfiniteScroll>
        </div>
    );
}