import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Comment from "./comment";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ posturl }) {
  /* Display image and post owner of a single post */
  // const [post, setPost] = useState(null);

  // useEffect(() => {
  //   fetch(posturl, { credentials: "same-origin" })
  //     .then((response) => response.json())
  //     .then((data) => setPost(data)) // Set post data when fetched
  //     .catch((error) => console.error("Error fetching post: ", error));
  // }, [posturl]);

  if (!posturl) {
    return <div>Loading...</div>; // Display a loading message until the post is fetched
  }

  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [comments, setComments] = useState([]);
  const [comments_url, setcomments_url] = useState("");
  const [created, setcreated] = useState("");
  const[likes, setLikes] = useState({
    lognameLikesThis: false,  
    numLikes: 0, 
    url: ""
    });
  const [ownerImgUrl, setownerImgUrl] = useState("");
  const [postShowUrl, setpostShowUrl] = useState("");
  const [postid, setpostid] = useState(0);
  const [url, seturl] = useState("");
  const [ownerShowUrl, setOwnerShowUrl] = useState(""); 
  const [newCommentText, setNewCommentText] = useState("");
  const [postLoad, setpostLoad] = useState(false);

useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(posturl, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log(data);
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        // data.results.forEach(post => {
        //   fetch(post.url, {credentials: 'same-origin'})
        //     .then((response) => {
        //       if (!response.ok) throw Error(response.statusText);
        //       return response.json();
        //     })
        //     .then((postData) => {
        //       console.log(postData);
              if (!ignoreStaleRequest) {
                setImgUrl(data.imgUrl);
                setOwner(data.owner);
                setcomments_url(data.comments_url);
                setcreated(data.created);
                setLikes(data.likes);
                setownerImgUrl(data.ownerImgUrl);
                setpostShowUrl(data.postShowUrl);
                setpostid(data.postid);
                seturl(data.url);
                setComments(data.comments);
                setOwnerShowUrl(data.ownerShowUrl);
                setpostLoad(true);
              }
            })
            .catch((error) => console.log(error));
        // });
      // });
    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [posturl]);



  // const [urls, setUrls] = useState([]);

  // useEffect(() => {
  //   let ignoreStaleRequest = false;
  //   fetchPostUrls();
  //   return () => {
  //     // This is a cleanup function that runs whenever the Post component
  //     // unmounts or re-renders. If a Post is about to unmount or re-render, we
  //     // should avoid updating state.
  //     ignoreStaleRequest = true;
  //   };
  // }, [posturl]);

  // async function fetchPostUrls() {
  //   try{
  //     const response = await fetch(posturl, {credentials: "same-origin"});
  //     if(!response.ok) throw Error(response.statusText);
  //     const postsData = await response.json();
  //     const postUrls = postsData.results.map((post) => post.url);
  //     setUrls(postUrls);
  //     showPosts(postUrls);
  //   } catch(error) {
  //     console.error("Error fetching post URLs: ". error);
  //   }
  // }

  // function showPosts(postUrls) {
  //   const entry = document.getElementById("reactEntry");

  //   postUrls.forEach((url) => {
  //     const div = document.createElement("div");
  //     entry.appendChild(div);
      
  //     fetch(url)
  //       .then((response) => {
  //         if (!response.ok) {
  //           throw new Error("Failed to fetch post data");
  //         }
  //         return response.json();
  //       })
  //       .then((post) => {
  //         updateDOM(post, div);
  //       })
  //       .catch((error) => {
  //         console.error("Error fetching post", error);
  //       });
  //   });
  // }

  // function updateDOM(post, div) {
  //   div.innerHTML = `
  //     <div className="post">
  //       <a href = "${post.ownerShowUrl}">
  //         <img src="${post.ownerImgUrl}" alt="owner_image" />
  //       </a>
  //       <a href = "${post.ownerShowUrl}">${post.owner}</a>
  //       <p>{created}</p> 
  //       {/* change format and add link 🔼  TODO: add human readable time stamp*/} 
        
  //       <img 
  //         src="${post.imgUrl}"
  //         alt="post_image"
  //         onDoubleClick="handleDoubleClickLike()"
  //       />
  //       {/* Like Section */}
  //       <div>
  //         <button data-testid='like-unlike-button' onClick="handleLike()">
  //           ${post.likes.lognameLikesThis? "Unlike" : "Like"} (${post.likes.numLikes})
  //         </button>
  //       </div>

  //       ${post.comments.map((x) =>
  //           `<Comment
  //           key=${x.commentid}
  //           commentid=${x.commentid}
  //           lognameOwnsThis=${x.lognameOwnsThis}
  //           owner=${x.owner}
  //           ownerShowUrl=${x.ownerShowUrl}
  //           text=${x.text}
  //           url=${x.url}
  //           handleClick="handleClick(${x.commentid})"
  //         />`
  //       ).join('')}

  //       {/* Comment Form */}
  //       <form data-testid='comment-form' onSubmit="handleAddComment(event)">
  //         <input
  //           type="text"
  //           value=""
  //           onKeyDown="handleKeyDown(event)"
  //           placeholder="Add a comment..."
  //         />
  //       </form>
  //     </div>
  //   `;
  //   return <div id="reactEntry"> Loading posts...</div>;
  // }


  function handleClick(commentid){
    const url = `/api/v1/comments/${commentid}/`
    fetch(url, {method: "DELETE", credentials: "same-origin"})
    .then(response => {
      if(response.ok){
        console.log("Comment deleted successfully");
        setComments(comments.filter((x) => x.commentid !== commentid));
      }
      else{
        console.log("Error deleting comment");
      }
    })
    .catch(error => {
      console.log("there is an error in delete comment", error);
    });
  }

  function handleLike() {
    const method = likes.lognameLikesThis ? "DELETE" : "POST";
    const likeUrl = method === "DELETE" ? likes.url : `/api/v1/likes/?postid=${postid}`; // Fallback for POST if `likes.url` is null
  
    // If it's a POST (like action), we need to provide postid to the backend
    const requestOptions = {
      method: method,
      credentials: "same-origin",
    };
  
    if (method === "POST") {
      // Attach postid for POST request (when liking a post)
      requestOptions.headers = {
        "Content-Type": "application/json",
      };
      requestOptions.body = JSON.stringify({ postid: postid });// Assuming `postid` is available in scope
    }

    console.log(likeUrl);
    // Perform the fetch request
    fetch(likeUrl, requestOptions)
      .then((response) => {
          // Parse the response body as JSON
        return method === "POST" ? response.json() : Promise.resolve(); // Parsing the response JSON
      })
      .then((data) => {
        // Now we have the parsed JSON in the 'data' object
        if (method === "POST") {
          console.log(data); // Check what is returned from the server (likeid, url, etc.)
          setLikes((prevLikes) => ({
            ...prevLikes,
            lognameLikesThis: true,
            numLikes: prevLikes.numLikes + 1,
            url: `/api/v1/likes/${data.likeid}/`, // Set the new like URL using data.likeid
          }));
        } else if (method === "DELETE") {
          setLikes((prevLikes) => ({
            ...prevLikes,
            lognameLikesThis: false,
            numLikes: prevLikes.numLikes - 1,
            url: null, // Reset the like URL after unliking
          }));

        }
      })
      //   } else {
      //     console.error("Failed to update like status");
      //   }
      // })
      .catch((error) => {
        console.error("There was an error updating the like status:", error);
      });
  }

  function handleDoubleClickLike() {
    const likesUrl = `/api/v1/likes/?postid=${postid}`
    if (!likes.lognameLikesThis) {
      fetch(likesUrl, {
        method: "POST",
        credentials: "same-origin",
      })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setLikes((prevLikes) => ({
          ...prevLikes,
          lognameLikesThis: true,
          numLikes: prevLikes.numLikes + 1,
          url: `/api/v1/likes/${data.likeid}/`,
        }));
      })
      .catch((error) => {
        console.error("There was an error liking the image:", error);
      });
    }
  }

  function handleKeyDown(event) {
    if(event.key === "Enter") {
      handleAddComment(event);
    }
  }

  function handleAddComment(event) {
    event.preventDefault();

    if (!newCommentText.trim()) {
      return;
    } //ignore empty comments

    fetch(comments_url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: newCommentText,
      }),
    })
      .then((response) => response.json())
      .then((newComment) => {
        setComments((prevComments) => [...prevComments, newComment]);
        setNewCommentText(""); //clean input field
      })
      .catch((error) => {
        console.error("Error adding comments:", error);
      });
  };

  return (
    <div className="post">
       <a href = {ownerShowUrl}>
        <img src={ownerImgUrl} alt="owner_image" />
       </a>
      <a href = {ownerShowUrl}>{owner}</a>
      <a href = {postShowUrl}>
        <p>{created}</p> 
        {/* change format and add link 🔼  TODO: add human readable time stamp*/} 
      </a>
      
      <img 
        src={imgUrl} 
        alt="post_image"
        onDoubleClick={handleDoubleClickLike} 
      />
      {/* Like Section */}
      
      <div>
        <button data-testid='like-unlike-button' onClick={handleLike}>
          {likes.lognameLikesThis? "Unlike" : "Like"} ({likes.numLikes})
        </button>
      </div>

      {comments.map((x) =>
          <Comment
          key={x.commentid}
          commentid={x.commentid}
          lognameOwnsThis={x.lognameOwnsThis}
          owner={x.owner}
          ownerShowUrl={x.ownerShowUrl}
          text={x.text}
          url={x.url}
          handleClick={handleClick}
        />
      )}

      {/* Comment Form */}
      <form data-testid='comment-form' onSubmit={handleAddComment}>
        <input
          type="text"
          //value={newCommentText}
          onChange={(e) => setNewCommentText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Add a comment..."
        />
      </form>
    </div>
  );
}

Post.propTypes = {
  posturl: PropTypes.string.isRequired,
  // imgurl: PropTypes.string.isRequired,
  // owner: PropTypes.string.isRequired,
  // comments: PropTypes.array.isRequired,
  // created: PropTypes.string.isRequired,
  // likes: PropTypes.object.isRequired,
  // ownerImgUrl: PropTypes.string.isRequired,
  // postShowUrl: PropTypes.string.isRequired,
  // postid: PropTypes.number.isRequired,
  // url: PropTypes.string.isRequired,
  // ownerShowUrl: PropTypes.string.isRequired,
};


  // const [imgUrl, setImgUrl] = useState("");
  // const [owner, setOwner] = useState("");
  // const [comments, setComments] = useState([]);
  // const [comments_url, setcomments_url] = useState("");
  // const [created, setcreated] = useState("");
  // const[likes, setLikes] = useState({
  //   lognameLikesThis: false,  
  //   numLikes: 0, 
  //   url: ""
  //   });
  // const [ownerImgUrl, setownerImgUrl] = useState("");
  // const [postShowUrl, setpostShowUrl] = useState("");
  // const [postid, setpostid] = useState(0);
  // const [url, seturl] = useState("");
  // const [ownerShowUrl, setOwnerShowUrl] = useState(""); 
  // const [newCommentText, setNewCommentText] = useState("");
    
  // useEffect(() => {
  //   // Declare a boolean flag that we can use to cancel the API request.
  //   let ignoreStaleRequest = false;

  //   // Call REST API to get the post's information
  //   fetch(posturl, { credentials: "same-origin" })
  //     .then((response) => {
  //       if (!response.ok) throw Error(response.statusText);
  //       return response.json();
  //     })
  //     .then((data) => {
  //       console.log(data);
  //       // If ignoreStaleRequest was set to true, we want to ignore the results of the
  //       // the request. Otherwise, update the state to trigger a new render.
  //       data.results.forEach(post => {
  //         fetch(post.url, {credentials: 'same-origin'})
  //           .then((response) => {
  //             if (!response.ok) throw Error(response.statusText);
  //             return response.json();
  //           })
  //           .then((postData) => {
  //             console.log(postData);
  //             if (!ignoreStaleRequest) {
  //               setImgUrl(postData.imgUrl);
  //               setOwner(postData.owner);
  //               setcomments_url(postData.comments_url);
  //               setcreated(postData.created);
  //               setLikes(postData.likes);
  //               setownerImgUrl(postData.ownerImgUrl);
  //               setpostShowUrl(postData.postShowUrl);
  //               setpostid(postData.postid);
  //               seturl(postData.url);
  //               setComments(postData.comments);
  //               setOwnerShowUrl(postData.ownerShowUrl);
  //             }
  //           })
  //           .catch((error) => console.log(error));
  //       });
  //     });
  //   return () => {
  //     // This is a cleanup function that runs whenever the Post component
  //     // unmounts or re-renders. If a Post is about to unmount or re-render, we
  //     // should avoid updating state.
  //     ignoreStaleRequest = true;
  //   };
  // }, [posturl]);

    // Render post image and post owner