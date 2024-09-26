"""
Insta485 comments view.

URLs include:
/comments/
"""
import flask
import insta485


@insta485.app.route("/comments/", methods=["POST"])
def update_comments():
    """
    Handle comment-related operations: create and delete.

    This view allows users to either create a new comment or delete an
    existing comment based on the operation provided in the POST request.

    POST parameters:
    - operation: Specifies the type of action ("create" or "delete").
    - postid: Required for creating a comment.
    - commentid: Required for deleting a comment.

    :return: A redirect to the target URL or the index page.
    """
    # Get the current user's username from session
    logname = flask.session['username']

    # Get the database connection
    connection = insta485.model.get_db()

    # Extract the operation and optional commentid and target URL
    operation = flask.request.form["operation"]
    target = flask.request.args.get("target")

    # If no target URL is specified, redirect to the index page
    if not target:
        target = flask.url_for('show_index')

    # Handle comment creation
    if operation == "create":
        postid = flask.request.form.get("postid")
        text = flask.request.form.get("text", "").strip()

        # Ensure the necessary fields are provided
        if not operation or not postid:
            flask.abort(400, description="Missing operation or postid")
        if not text:
            flask.abort(400, description="Comment text cannot be empty")

        # Insert the new comment into the database
        q_insert = '''
            INSERT INTO comments (owner, postid, text)
            VALUES (?, ?, ?)
        '''
        connection.execute(q_insert, (logname, postid, text))

    # Handle comment deletion
    elif operation == "delete":
        commentid = flask.request.form.get("commentid")
        if not commentid:
            flask.abort(400, description="Missing commentid")

        # Retrieve the comment owner's name
        q_owner = '''
            SELECT owner
            FROM comments
            WHERE commentid = ?
        '''
        c = connection.execute(q_owner, (commentid,))
        owner = c.fetchone()

        if owner is None:
            flask.abort(404, description="Comment not found")

        # Ensure the current user is the owner of the comment
        if owner["owner"] != logname:
            flask.abort(403)

        # Delete the comment from the database
        q_delete = '''
            DELETE FROM comments
            WHERE commentid = ?
        '''
        connection.execute(q_delete, (commentid,))

    # Redirect the user to the target URL
    return flask.redirect(target)
