import PropTypes from "prop-types";
import React from "react";

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
}

Comment.propTypes = {
  commentid: PropTypes.number.isRequired,
  lognameOwnsThis: PropTypes.bool.isRequired,
  owner: PropTypes.string.isRequired,
  ownerShowUrl: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  handleClick: PropTypes.func.isRequired,
};
