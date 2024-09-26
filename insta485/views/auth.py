"""
Insta485 index (main) view.

URLs include:
/accounts/auth/
"""
import flask
import insta485

# Create a logger instance for this module
LOGGER = flask.logging.create_logger(insta485.app)


@insta485.app.route('/accounts/auth/')
def auth():
    """
    Authenticate if a user is logged in.

    This route checks if the 'username' exists in the session, which indicates
    that a user is authenticated. If a user is logged in, it returns a 200 OK
    response. Otherwise, it returns a 403 Forbidden error.

    :return: An empty response with status code 200 if authenticated.
    """
    if 'username' in flask.session:
        return '', 200  # User is authenticated, return 200 OK
    return flask.abort(403)  # User is not authenticated, return 403 Forbidden
