"""
Insta485 account deletion view.

Handles requests to display the account deletion page.

URLs include:
/accounts/delete/
"""
import flask
import insta485


@insta485.app.route('/accounts/delete/')
def delete():
    """
    Display the account deletion page if the user is logged in.

    If the user is not logged in, they are redirected to the login page.
    If the user is logged in, the account deletion page is displayed.

    :return: Redirect to the login page if not logged in, or render the
             account deletion template if logged in.
    """
    # Check if the user is logged in
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    # Get the logged-in user's username
    logname = flask.session['username']

    # Render the account deletion template with the user's context
    context = {"logname": logname}
    return flask.render_template("delete.html", **context)
