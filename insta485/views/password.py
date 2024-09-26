"""
Insta485 account password view.

URLs include:
/accounts/password/
"""
import flask
import insta485


@insta485.app.route('/accounts/password/')
def password():
    """
    Display the password change page if the user is logged in.

    If the user is not logged in, they are redirected to the login page.
    Otherwise, the password change page is displayed.

    :return: Redirect to the login page if not logged in, or render the
             password change page with the logged-in user's information.
    """
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    logname = flask.session['username']
    context = {'logname': logname}
    return flask.render_template("password.html", **context)
