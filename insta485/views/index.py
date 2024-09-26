"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    logname = flask.session['username']

    # Connect to database
    connection = insta485.model.get_db()

    # Query database for posts and user information
    query = '''
        SELECT posts.postid, posts.filename, posts.created, posts.owner,
               users.username, users.filename AS profile_pic
        FROM posts
        JOIN users ON posts.owner = users.username
        WHERE posts.owner = ?
        OR posts.owner IN (
            SELECT username2 FROM following WHERE username1 = ?
        )
        ORDER BY posts.created DESC
    '''
    cur = connection.execute(query, (logname, logname))
    posts = cur.fetchall()  # Fetch all rows from the SQL output

    for post in posts:
        # Get number of likes for each post
        post_id = post['postid']
        q_likes = '''
            SELECT COUNT(*) AS num_likes
            FROM likes
            WHERE postid = ?
        '''
        c = connection.execute(q_likes, (post_id,))
        post['number_likes'] = c.fetchone()['num_likes']

        # Get comments for each post
        q_comments = '''
            SELECT comments.text, comments.created,
                   users.username AS comment_owner
            FROM comments
            JOIN users ON users.username = comments.owner
            WHERE comments.postid = ?
            ORDER BY comments.created ASC
        '''
        c = connection.execute(q_comments, (post_id,))
        post['comments'] = c.fetchall()

        # Check if the user has liked the post
        q_like_or_unlike = '''
            SELECT likes.owner
            FROM likes
            WHERE owner = ? AND postid = ?
        '''
        c_l = connection.execute(q_like_or_unlike, (logname, post_id))
        result = c_l.fetchall()
        post["like_or_unlike"] = "unlike" if result else "like"

        # Calculate how long ago the post was created
        post['time_since'] = arrow.get(post['created']).humanize()

    # Prepare the context for rendering the index page
    context = {
        "posts": posts,
        "logname": logname
    }

    return flask.render_template("index.html", **context)
