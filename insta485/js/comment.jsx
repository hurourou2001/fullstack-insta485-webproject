import PropTypes from "prop-types";
import React from "react";

<<<<<<< HEAD
export default function Comment({ commentid, lognameOwnsThis, owner, ownerShowUrl, text, url, handleClick }) {
    return(
        <div className="comment">
            <a href={ownerShowUrl}>
                {owner}
            </a> 
            <span data-testid ="comment-text"> {text} </span>
            {lognameOwnsThis && (
                <button 
                data-testid="delete-comment-button"
                onClick={() => handleClick(commentid)}>
                Delete
                </button>
            )}
        </div>
    );
=======
export default function Comment({
  commentid,
  lognameOwnsThis,
  owner,
  ownerShowUrl,
  text,
  handleClick,
}) {
  return (
    <div className="comment">
      <a href={ownerShowUrl}>{owner}</a>
      <span data-testid="comment-text"> {text} </span>
      {lognameOwnsThis && (
        <button
          type="button"
          data-testid="delete-comment-button"
          onClick={() => handleClick(commentid)}
        >
          Delete
        </button>
      )}
    </div>
  );
>>>>>>> 77bf5e502602e4df37a59b75e85eadd89eda91b1
}

Comment.propTypes = {
  commentid: PropTypes.number.isRequired,
  lognameOwnsThis: PropTypes.bool.isRequired,
  owner: PropTypes.string.isRequired,
  ownerShowUrl: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  handleClick: PropTypes.func.isRequired,
};
