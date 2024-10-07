import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Comment from "./comment";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ posturl }) {
  /* Display image and post owner of a single post */

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
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
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
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [posturl]);
 

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
    fetch(likes.url, {
      method: method,
      credentials: "same-origin",
    })
      .then((response) => {
        if (response.ok) {
          setLikes((prevLikes) => ({
            ...prevLikes,
            lognameLikesThis: !prevLikes.lognameLikesThis,
            numLikes: !prevLikes.lognameLikesThis
              ? prevLikes.numLikes + 1
              : prevLikes.numLikes - 1,
          }))
        } else {
          console.error("Failed to update like status")
        }
      })
      .catch((error) => {
        console.error("There was an error updating the like status:", error);
      });
  }

  function handleDoubleClickLike() {
    if (!likes.lognameLikesThis) {
      fetch(likes.url, {
        method: "POST",
        credentials: "same-origin",
      })
        .then((response) => {
          if(response.ok) {
            setLikes((prevLikes) => ({
              ...prevLikes,
              lognameLikesThis: true,
              numLikes: prevLikes.numLikes + 1,
            }));
          } else {
            console.error("Failed to like the image");
          }
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
  }

  // Render post image and post owner
  return (
    <div className="post">
       <a href = {ownerShowUrl}>
        <img src={ownerImgUrl} alt="owner_image" />
       </a>
      <a href = {ownerShowUrl}>{owner}</a>
      <p>{created}</p> 
      {/* change format and add link 🔼 */}
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
          value={newCommentText}
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
