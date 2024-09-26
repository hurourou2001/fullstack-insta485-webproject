"""
Insta485 explore view.

Handles requests to display the explore page, showing users that the
logged-in user is not following.

URLs include:
/explore/
"""
import flask
import insta485


@insta485.app.route('/explore/')
def show_explore():
    """
    Display the explore page if the user is logged in.

    If the user is logged in, this view shows users that the logged-in
    user is not currently following. If the user is not logged in, they
    are redirected to the login page.

    :return: Redirect to login page if not logged in, or render the
             explore page template with a list of users not followed.
    """
    # Check if the user is logged in
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    # Get the logged-in user's username
    logname = flask.session['username']

    # Connect to the database
    connection = insta485.model.get_db()

    # Fetch users who are not the logged-in user and are not being followed
    cur = connection.execute(
        """
        SELECT username, filename AS profile
        FROM users
        WHERE username != ?
        AND username NOT IN (
            SELECT username2
            FROM following
            WHERE username1 = ?
        )
        """,
        (logname, logname)
    )

    # Fetch all the users
    users = cur.fetchall()

    # Pass the data to the template for rendering
    context = {
        "users": users,
        "logname": logname
    }

    # Close the database connection after the request
    insta485.model.close_db(None)

    # Render the explore page template
    return flask.render_template('explore.html', **context)
