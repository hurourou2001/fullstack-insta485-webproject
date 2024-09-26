"""
Insta485 account creation view.

Handles user account creation requests.

URLs include:
/accounts/create/
"""
import flask
import insta485


@insta485.app.route('/accounts/create/')
def create():
    """
    Display the account creation page or redirect if already logged in.

    If the user is already logged in (i.e., 'logname' is in the session),
    they are redirected to the account edit page. Otherwise, the account
    creation page is displayed.

    :return: Redirect to the account edit page if logged in, or render
             the account creation template.
    """
    if 'logname' in flask.session:
        return flask.redirect(flask.url_for('edit'))

    # Render the account creation template
    return flask.render_template("create.html")
