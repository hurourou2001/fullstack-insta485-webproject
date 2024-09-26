"""
Insta485 views for followers and following operations.

This module handles displaying followers, following, and operations
such as following/unfollowing users.

URLs include:
/users/<user_url_slug>/followers/
/users/<user_url_slug>/following/
/following/
"""
import flask
import insta485


@insta485.app.route('/users/<user_url_slug>/followers/')
def show_followers(user_url_slug):
    """
    Display the followers of the user specified by `user_url_slug`.

    If the logged-in user is not following a follower, the relationship
    is marked as 'not_following'. If the logged-in user is the follower,
    the relationship is left blank. This ensures the proper status of
    each follower is displayed.

    :param user_url_slug: The username of the user whose followers to display.
    :return: Renders the followers template with user and follower data.
    """
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    logname = flask.session['username']
    connection = insta485.model.get_db()

    # Check if the user exists
    user = connection.execute(
        "SELECT username FROM users WHERE username = ?",
        (user_url_slug,)
    ).fetchone()

    if user is None:
        flask.abort(404)  # Return a 404 if the user does not exist

    # Get all followers of `user_url_slug`
    followers = connection.execute(
        '''
        SELECT username1 AS follower, users.filename AS icon
        FROM following
        JOIN users ON following.username1 = users.username
        WHERE username2 = ?
        ''', (user_url_slug,)
    ).fetchall()

    # Prepare the list of followers with their relationship to the logged-in
    followers_data = []
    for follower in followers:
        follower_data = {
            "username": follower["follower"],
            "icon": follower["icon"],
            "relationship": ""
        }

        # If the logged-in user is the follower, leave relationship blank
        if logname != follower["follower"]:
            is_following = connection.execute(
                '''
                SELECT 1 FROM following
                WHERE username1 = ? AND username2 = ?
                ''', (logname, follower["follower"])
            ).fetchone()

            if is_following:
                follower_data["relationship"] = "following"
            else:
                follower_data["relationship"] = "not_following"

        followers_data.append(follower_data)

    # Pass the data to the template
    context = {
        "user_url_slug": user_url_slug,
        "followers": followers_data,
        "logname": logname
    }
    return flask.render_template("followers.html", **context)


@insta485.app.route('/users/<user_url_slug>/following/')
def show_following(user_url_slug):
    """
    Display the users that `user_url_slug` is following.

    If the logged-in user is following a user in the list, the relationship
    is marked as 'following'. If the logged-in user is the same as the user
    being followed, the relationship is left blank.

    :param user_url_slug: The username of the user whose following list to
    :return: Renders the following template with user and following data.
    """
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    logname = flask.session['username']
    connection = insta485.model.get_db()

    # Check if the user exists
    user = connection.execute(
        "SELECT username FROM users WHERE username = ?",
        (user_url_slug,)
    ).fetchone()

    if user is None:
        flask.abort(404)  # Return a 404 if the user does not exist

    # Get all users that `user_url_slug` is following
    following = connection.execute(
        '''
        SELECT username2 AS following, users.filename AS icon
        FROM following
        JOIN users ON following.username2 = users.username
        WHERE username1 = ?
        ''', (user_url_slug,)
    ).fetchall()

    # Prepare the list of following users with their relationship
    following_data = []
    for follow in following:
        follow_data = {
            "username": follow["following"],
            "icon": follow["icon"],
            "relationship": ""
        }

        # If the logged-in user is not following this user, check rela
        if logname != follow["following"]:
            is_following = connection.execute(
                '''
                SELECT 1 FROM following
                WHERE username1 = ? AND username2 = ?
                ''', (logname, follow["following"])
            ).fetchone()

            if is_following:
                follow_data["relationship"] = "following"
            else:
                follow_data["relationship"] = "not_following"

        following_data.append(follow_data)

    # Pass the data to the template
    context = {
        "user_url_slug": user_url_slug,
        "following": following_data,
        "logname": logname
    }
    return flask.render_template("following.html", **context)


@insta485.app.route('/following/', methods=['POST'])
def follow_user():
    """
    Handle the operation to follow or unfollow a user.

    The form must include the username of the user to follow or unfollow and
    the operation ('follow' or 'unfollow'). If the operation is invalid, it
    raises an error.

    :return: Redirects the user to the target URL or index.
    """
    logname = flask.session['username']
    connection = insta485.model.get_db()
    username = flask.request.form['username']
    operation = flask.request.form["operation"]
    target = flask.request.args.get("target", flask.url_for('show_index'))

    # Check if the follow/unfollow operation exists in the database
    q_check_exist_follow = '''
        SELECT username1, username2
        FROM following
        WHERE username1 = ? AND username2 = ?
    '''
    result = connection.execute(q_check_exist_follow,
                                (logname, username)).fetchone()

    # Handle follow operation
    if operation == 'follow':
        if result:
            flask.abort(409)  # Conflict, already following

        q_add = '''
            INSERT INTO following (username1, username2)
            VALUES (?, ?)
        '''
        connection.execute(q_add, (logname, username))

    # Handle unfollow operation
    elif operation == 'unfollow':
        if not result:
            flask.abort(409)  # Conflict, not following

        q_delete = '''
            DELETE FROM following
            WHERE username1 = ? AND username2 = ?
        '''
        connection.execute(q_delete, (logname, username))

    # Redirect to the target page
    return flask.redirect(target)
