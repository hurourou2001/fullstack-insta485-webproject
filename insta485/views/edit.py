"""
Insta485 account edit view.

Handles requests to display the account edit page.

URLs include:
/accounts/edit/
"""
import flask
import insta485


@insta485.app.route('/accounts/edit/')
def edit():
    """
    Display the account edit page if the user is logged in.

    If the user is not logged in, they are redirected to the login page.
    If the user is logged in, the account edit page is displayed, populated
    with the user's account information.

    :return: Redirect to the login page if not logged in, or render the
             account edit template with the user's data if logged in.
    """
    # Check if the user is logged in
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    # Get the logged-in user's username
    logname = flask.session['username']

    # Connect to the database and retrieve the user's details
    connection = insta485.model.get_db()

    cu = connection.execute(
        """
        SELECT username, filename AS profile,
               fullname, email, password
        FROM users
        WHERE username = ?
        """,
        (logname,)
    )

    # Fetch all the user details
    users = cu.fetchone()

    # Pass the user's data to the context for rendering the template
    context = {
        "logname": logname,
        "users": users,
    }

    # Render the account edit template with the user's data
    return flask.render_template('edit.html', **context)
