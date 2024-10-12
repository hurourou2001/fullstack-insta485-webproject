import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import Comment from "./comment";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);

dayjs.extend(relativeTime);
dayjs.extend(utc);

export default function Post({ posturl }) {
<<<<<<< HEAD
  /* Display image and post owner of a single post */

  if (!posturl) {
    return <div>Loading...</div>; // Display a loading message until the post is fetched
  }

=======
  // Declare state variables outside of conditional blocks
>>>>>>> 77bf5e502602e4df37a59b75e85eadd89eda91b1
  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [comments, setComments] = useState([]);
  const [commentsUrl, setCommentsUrl] = useState("");
  const [created, setCreated] = useState("");
  const [likes, setLikes] = useState({
    lognameLikesThis: false,
    numLikes: 0,
    url: "",
  });
  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [postShowUrl, setPostShowUrl] = useState("");
  const [postid, setPostid] = useState(0);
  const [ownerShowUrl, setOwnerShowUrl] = useState("");
  const [newCommentText, setNewCommentText] = useState("");
<<<<<<< HEAD
  const [postLoad, setpostLoad] = useState(false);
=======
  const [postLoad, setPostLoad] = useState(false);
>>>>>>> 77bf5e502602e4df37a59b75e85eadd89eda91b1

  useEffect(() => {
    let ignoreStaleRequest = false;

<<<<<<< HEAD
    // Call REST API to get the post's information
    fetch(posturl, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log(data);

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

=======
    if (posturl) {
      // Call REST API to get the post's information
      fetch(posturl, { credentials: "same-origin" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          if (!ignoreStaleRequest) {
            setImgUrl(data.imgUrl);
            setOwner(data.owner);
            setCommentsUrl(data.comments_url); // Changed from camelcase issue
            setCreated(data.created);
            setLikes(data.likes);
            setOwnerImgUrl(data.ownerImgUrl);
            setPostShowUrl(data.postShowUrl);
            setPostid(data.postid);
            setComments(data.comments);
            setOwnerShowUrl(data.ownerShowUrl);
            setPostLoad(true);
          }
        })
        .catch((error) => console.log(error));
    }
>>>>>>> 77bf5e502602e4df37a59b75e85eadd89eda91b1
    return () => {
      ignoreStaleRequest = true;
    };
  }, [posturl]);

<<<<<<< HEAD
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
=======
  function handleClick(commentid) {
    const deleteUrl = `/api/v1/comments/${commentid}/`;
    fetch(deleteUrl, { method: "DELETE", credentials: "same-origin" })
      .then((response) => {
        if (response.ok) {
          setComments(comments.filter((x) => x.commentid !== commentid));
        } else {
          console.log("Error deleting comment");
        }
      })
      .catch((error) => {
        console.log("There is an error in deleting the comment", error);
      });
>>>>>>> 77bf5e502602e4df37a59b75e85eadd89eda91b1
  }

  function handleLike() {
    const method = likes.lognameLikesThis ? "DELETE" : "POST";
    const likeUrl =
      method === "DELETE" ? likes.url : `/api/v1/likes/?postid=${postid}`;

    const requestOptions = {
      method,
      credentials: "same-origin",
    };

    if (method === "POST") {
      requestOptions.headers = {
        "Content-Type": "application/json",
      };
      requestOptions.body = JSON.stringify({ postid });
    }

    fetch(likeUrl, requestOptions)
      .then((response) =>
        method === "POST" ? response.json() : Promise.resolve(),
      )
      .then((data) => {
        if (method === "POST") {
          setLikes((prevLikes) => ({
            ...prevLikes,
            lognameLikesThis: true,
            numLikes: prevLikes.numLikes + 1,
            url: `/api/v1/likes/${data.likeid}/`,
          }));
        } else if (method === "DELETE") {
          setLikes((prevLikes) => ({
            ...prevLikes,
            lognameLikesThis: false,
            numLikes: prevLikes.numLikes - 1,
            url: null,
          }));
        }
      })
<<<<<<< HEAD

=======
>>>>>>> 77bf5e502602e4df37a59b75e85eadd89eda91b1
      .catch((error) => {
        console.error("There was an error updating the like status:", error);
      });
  }

  function handleDoubleClickLike() {
    const likesUrl = `/api/v1/likes/?postid=${postid}`;
    if (!likes.lognameLikesThis) {
      fetch(likesUrl, {
        method: "POST",
        credentials: "same-origin",
      })
        .then((response) => response.json())
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

  function handleAddComment(event) {
    event.preventDefault();

    if (!newCommentText.trim()) {
      return;
    }

    fetch(commentsUrl, {
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
        setNewCommentText(""); // Clear input after comment is added
      })
      .catch((error) => {
        console.error("Error adding comments:", error);
      });
  }

  function handleKeyDown(event) {
    if (event.key === "Enter") {
      handleAddComment(event);
    }
  }

  return (
    <div className="post">
      {postLoad ? (
        <>
          <a href={ownerShowUrl}>
            <img src={ownerImgUrl} alt="owner_image" />
          </a>
          <a href={ownerShowUrl}>{owner}</a>
          <a href={postShowUrl}>
<<<<<<< HEAD
          <p>{dayjs.utc(created).local().fromNow()}</p>
            {/* TODO: Add human readable timestamp */}
          </a>
  
          <img
            src={imgUrl}
            alt="post_image"
            onDoubleClick={handleDoubleClickLike}
          />
  
          {/* Like Section */}
          <div>
            <button data-testid="like-unlike-button" onClick={handleLike}>
              {likes.lognameLikesThis ? "Unlike" : "Like"} ({likes.numLikes})
            </button>
          </div>

          <div>
           {likes.numLikes === 1 ? "1 like" : `${likes.numLikes} likes`}
          </div>
  
          {/* Comments Section */}
=======
            <p>{dayjs.utc(created).local().fromNow()}</p>
          </a>

          <img
            src={imgUrl}
            alt="post_image"
            onDoubleClick={handleDoubleClickLike}
          />

          <div>
            <button
              data-testid="like-unlike-button"
              onClick={handleLike}
              type="button"
            >
              {likes.lognameLikesThis ? "Unlike" : "Like"} ({likes.numLikes})
            </button>
          </div>

          <div>
            {likes.numLikes === 1 ? "1 like" : `${likes.numLikes} likes`}
          </div>

>>>>>>> 77bf5e502602e4df37a59b75e85eadd89eda91b1
          {comments.map((x) => (
            <Comment
              key={x.commentid}
              commentid={x.commentid}
              lognameOwnsThis={x.lognameOwnsThis}
              owner={x.owner}
              ownerShowUrl={x.ownerShowUrl}
              text={x.text}
              url={x.url}
<<<<<<< HEAD
              handleClick={handleClick}
            />
          ))}
  
          {/* Comment Form */}
          <form data-testid="comment-form" onSubmit={handleAddComment}>
            <input
              type="text"
=======
              handleClick={() => handleClick(x.commentid)}
            />
          ))}

          <form data-testid="comment-form" onSubmit={handleAddComment}>
            <input
              type="text"
              value={newCommentText}
>>>>>>> 77bf5e502602e4df37a59b75e85eadd89eda91b1
              onChange={(e) => setNewCommentText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Add a comment..."
            />
          </form>
        </>
      ) : (
<<<<<<< HEAD
        <p>Loading...</p>  // This will render when postLoad is false
=======
        <p>Loading...</p>
>>>>>>> 77bf5e502602e4df37a59b75e85eadd89eda91b1
      )}
    </div>
  );
}

Post.propTypes = {
  posturl: PropTypes.string.isRequired,
};
<<<<<<< HEAD

=======
>>>>>>> 77bf5e502602e4df37a59b75e85eadd89eda91b1
