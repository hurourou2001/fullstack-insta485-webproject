"""
Insta485 index (main) view.

URLs include:
/accounts/login/
/accounts/logout/
"""
import flask
import insta485


@insta485.app.route('/accounts/login/')
def login():
    """
    Display the login page.

    If the user is already logged in (i.e., 'username' exists in session),
    they are redirected to the index page. Otherwise, login page is shown.

    :return: Redirect to the index page if logged in, or render login page.
    """
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template("login.html")


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """
    Log out the user by clearing the session.

    This route handles POST requests to log out the user by clearing the
    session and redirecting them to the login page.

    :return: Redirect to the login page after logging out.
    """
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))
