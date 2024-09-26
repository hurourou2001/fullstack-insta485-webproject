"""
Insta485 index (main) view.

URLs include:
/
"""
import os
import flask
import insta485


@insta485.app.route('/users/<user_url_slug>/')
def show_user(user_url_slug):
    """
    Display the user's profile page.

    If the logged-in user is viewing their own profile, the option to follow
    or unfollow is disabled. For other profiles, the logged-in user can see
    if they are following the profile owner and can choose to follow or
    unfollow. The page also displays the user's number of posts, followers,
    and followings.

    :param user_url_slug: The username from the URL.
    :return: Render the user profile page with the user's info.
    """
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    logname = flask.session['username']

    connection = insta485.model.get_db()
    q_name = '''
        SELECT username, fullname
        FROM users
        WHERE username = ?
    '''
    cur = connection.execute(q_name, (user_url_slug,))
    user = cur.fetchone()
    if user is None:
        flask.abort(404)
    user = dict(user)

    q_if_follow = '''
        SELECT username1
        FROM following
        WHERE username1 = ? AND username2 = ?
    '''
    if user_url_slug == logname:
        user["if_follow"] = "None"
    else:
        cur = connection.execute(q_if_follow, (logname, user_url_slug))
        result = cur.fetchall()
        if not result:
            user["if_follow"] = "not_following"
        else:
            user["if_follow"] = "following"

    q_num_posts = '''
        SELECT COUNT(*) as num_posts
        FROM posts
        WHERE owner = ?
    '''
    cur = connection.execute(q_num_posts, (user_url_slug,))
    user["num_posts"] = cur.fetchone()['num_posts']

    q_num_following = '''
        SELECT COUNT(DISTINCT username2) as f
        FROM following
        WHERE username1 = ?
    '''
    cur = connection.execute(q_num_following, (user_url_slug,))
    user["num_following"] = cur.fetchone()['f']

    q_num_followers = '''
        SELECT COUNT(DISTINCT username1) as fi
        FROM following
        WHERE username2 = ?
    '''
    cur = connection.execute(q_num_followers, (user_url_slug,))
    user["num_followers"] = cur.fetchone()['fi']

    q_image = '''
        SELECT postid, filename as img_name
        FROM posts
        WHERE owner = ?
        ORDER BY postid
    '''
    cur = connection.execute(q_image, (user_url_slug,))
    image = cur.fetchall()
    # Add database info to context
    context = {"user": user,
               "image": image,
               "logname": logname,
               "user_url_slug": user_url_slug}
    return flask.render_template("user.html", **context)


@insta485.app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve the uploaded files.

    This view is responsible for serving the uploaded files from the upload
    folder. If the user is not logged in or the file does not exist, the
    appropriate HTTP error is returned.

    :param filename: The name of the file requested.
    :return: The file from the upload folder if it exists.
    """
    if 'username' not in flask.session:
        return flask.abort(403)

    file_path = os.path.join(insta485.app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(file_path):
        return flask.abort(404)

    return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                                     filename)
