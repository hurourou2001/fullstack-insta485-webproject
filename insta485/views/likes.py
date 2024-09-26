"""
Insta485 likes view.

Handles the functionality for liking and unliking posts.

URLs include:
/likes/
"""
import flask
import insta485

LOGGER = flask.logging.create_logger(insta485.app)


@insta485.app.route("/likes/", methods=["POST"])
def update_likes():
    """
    Handle like/unlike operations for posts.

    This view updates the likes table in the database based on the operation
    (either "like" or "unlike") sent via a POST request. It redirects the
    user to the target URL or the index page after the operation.

    :return: Redirects the client to the target URL or index page.
    """
    # Log the incoming request details
    LOGGER.debug("operation = %s", flask.request.form["operation"])
    LOGGER.debug("postid = %s", flask.request.form["postid"])

    logname = flask.session['username']

    # Connect to the database
    connection = insta485.model.get_db()
    operation = flask.request.form["operation"]
    postid = flask.request.form["postid"]

    # Handle like operation
    if operation == "like":
        existing_like = connection.execute(
            "SELECT 1 FROM likes WHERE owner = ? AND postid = ?",
            (logname, postid)
        ).fetchone()

        if existing_like:
            flask.abort(409)  # Conflict - user already liked the post
        else:
            connection.execute(
                "INSERT INTO likes (owner, postid) VALUES (?, ?)",
                (logname, postid)
            )

    # Handle unlike operation
    elif operation == "unlike":
        deleted_existing = connection.execute(
            "DELETE FROM likes WHERE owner = ? AND postid = ?",
            (logname, postid)
        ).rowcount

        if deleted_existing == 0:
            flask.abort(409)  # Conflict - user hasn't liked the post

    # Redirect the user to the target URL or index page
    target = flask.request.args.get('target')
    if target:
        return flask.redirect(target)
    return flask.redirect(flask.url_for('show_index'))
