"""
Insta485 posts view.

Handles the display and updates for posts.

URLs include:
/posts/<postid_url_slug>/
/posts/
"""
import uuid
import os
import pathlib
import flask
import arrow
import insta485


@insta485.app.route('/posts/<int:postid_url_slug>/')
def show_posts(postid_url_slug):
    """
    Display a specific post by post ID.

    If the user is not logged in, they are redirected to the login page.
    Otherwise, the post is fetched from the database and displayed with
    relevant details like likes, comments, and user information.

    :param postid_url_slug: The post ID from the URL.
    :return: Render the post page with context data.
    """
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    connection = insta485.model.get_db()
    logname = flask.session['username']

    # Get post information
    q_info = '''
        SELECT posts.filename, posts.created, posts.owner
        FROM posts
        WHERE postid = ?
    '''
    c = connection.execute(q_info, (postid_url_slug,))
    post_info = c.fetchone()
    post = {}

    # Get the user's profile picture
    q_user_pic = '''
        SELECT filename
        FROM users
        WHERE username = ?
    '''
    c = connection.execute(q_user_pic, (post_info['owner'],))
    post['user_pic'] = c.fetchone()['filename']

    # Get number of likes
    q_likes = '''
        SELECT COUNT(*) AS num_likes
        FROM likes
        WHERE postid = ?
    '''
    c = connection.execute(q_likes, (postid_url_slug,))
    post['number_likes'] = c.fetchone()['num_likes']

    # Get comments
    q_comments = '''
        SELECT comments.text, comments.created,
        users.username AS comment_owner, comments.commentid
        FROM comments
        JOIN users ON users.username = comments.owner
        WHERE comments.postid = ?
        ORDER BY comments.created
    '''
    c = connection.execute(q_comments, (postid_url_slug,))
    post['comments'] = c.fetchall()

    # Check if the logged-in user liked the post
    q_like_or_unlike = '''
        SELECT likes.owner
        FROM likes
        WHERE owner = ? AND postid = ?
    '''
    c_l = connection.execute(q_like_or_unlike, (logname, postid_url_slug))
    post["like_or_unlike"] = "like" if not c_l.fetchall() else "unlike"

    # Add time since post creation
    post_info = dict(post_info)
    post_info['time_since'] = arrow.get(post_info['created']).humanize()

    # Prepare context for rendering
    context = {
        "post": post,
        "post_info": post_info,
        "logname": logname,
        "postid_url_slug": postid_url_slug
    }
    return flask.render_template("posts.html", **context)


LOGGER = flask.logging.create_logger(insta485.app)


@insta485.app.route("/posts/", methods=["POST"])
def update_posts():
    """
    Handle creating and deleting posts.

    This view processes POST requests to either create a new post or delete
    an existing post. The appropriate action is determined by the 'operation'
    parameter in the form data.

    :return: Redirects to the target URL after processing the request.
    """
    logname = flask.session['username']
    connection = insta485.model.get_db()
    operation = flask.request.form["operation"]
    target = flask.request.args.get("target")

    if not target:
        target = flask.url_for('show_user', user_url_slug=logname)

    if operation == "create":
        # Create a new post
        if 'file' not in flask.request.files or \
           flask.request.files['file'].filename == '':
            flask.abort(400, description="No file uploaded")

        fileobj = flask.request.files['file']
        filename = fileobj.filename

        # Generate a unique filename and save the file
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"

        fileobj.save(
            insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
            )

        q_create = '''
            INSERT INTO posts (filename, owner)
            VALUES (?, ?)
        '''
        connection.execute(q_create, (uuid_basename, logname))

    elif operation == "delete":
        # Delete an existing post
        postid = flask.request.form.get("postid")
        if not postid:
            flask.abort(400)

        # Verify post ownership before deleting
        q_post_owner = '''
            SELECT owner, filename
            FROM posts
            WHERE postid = ?
        '''
        post = connection.execute(q_post_owner, (postid,)).fetchone()

        if post is None:
            flask.abort(404)

        if post["owner"] != logname:
            flask.abort(403)

        # Remove the image from the filesystem
        image_path = (
            pathlib.Path(
                insta485.app.config["UPLOAD_FOLDER"]
                ) / post["filename"]
        )
        if image_path.exists():
            os.remove(image_path)

        # Delete the post from the database
        q_delete_post = 'DELETE FROM posts WHERE postid = ?'
        connection.execute(q_delete_post, (postid,))

    return flask.redirect(target)
