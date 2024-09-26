"""
Insta485 index (main) view.

URLs include:
/accounts/
"""
import os
import uuid
import hashlib
import pathlib

import flask

import insta485

# Create logger
LOGGER = flask.logging.create_logger(insta485.app)

# Set secret key for the app
insta485.app.secret_key = (
    b'\xe7k\x1d\x06\xe8D@\xa6\xb8\xd3\xb9O\x8a\x85\xe6[\x8a\xedGB\x13\x0e\xbe3'
)


@insta485.app.route("/accounts/", methods=["POST"])
def accounts():
    """
    Handle account operations.

    The function handles POST requests to perform account-related actions such
    as user login, account creation, account deletion, account editing, and
    password changes.
    """
    LOGGER.debug("operation = %s", flask.request.form["operation"])
    operation = flask.request.form["operation"]
    connection = insta485.model.get_db()

    if operation == "login":
        return login_user(connection)

    if operation == "create":
        return create_account(connection)

    if operation == "delete":
        return delete_account(connection)

    if operation == "edit_account":
        return edit_account(connection)

    if operation == 'update_password':
        return change_password(connection)

    return flask.abort(400)


def login_user(connection):
    """
    Log in a user by verifying the username and password.

    This function takes user input, hashes the password, and checks it
    against the stored value in the database. If the credentials are correct,
    the user is logged in.

    :param connection: Database connection object.
    :return: Redirect to the index page or target URL.
    """
    username = flask.request.form["username"]
    password = flask.request.form["password"]

    if not username or not password:
        flask.abort(400)

    cur = connection.execute(
        'SELECT username, password FROM users WHERE username = ?',
        (username,)
    )
    result = cur.fetchone()

    if not result:
        return flask.abort(403)

    real_password = result['password']
    password_list = real_password.split('$')
    salt = password_list[1]

    password_db_string = hash_password(password, salt)

    cur = connection.execute(
        'SELECT username FROM users WHERE username = ? AND password = ?',
        (username, password_db_string)
    )
    result = cur.fetchone()

    if result:
        flask.session['username'] = username
        target = flask.request.args.get('target')
        if not target:
            return flask.redirect(flask.url_for('show_index'))
        return flask.redirect(target)

    return flask.abort(403)


def create_account(connection):
    """
    Create a new account for a user by inserting their details into database.

    The function collects the required user information and saves it in the
    database, including a hashed version of the password.

    :param connection: Database connection object.
    :return: Redirect to the index page or target URL.
    """
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    fullname = flask.request.form["fullname"]
    email = flask.request.form["email"]
    file = flask.request.files['file']

    if not username or not password or not fullname or not email or not file:
        return flask.abort(400)

    cur = connection.execute(
        'SELECT username FROM users WHERE username = ?',
        (username,)
    )
    if cur.fetchone():
        return flask.abort(409)

    salt = uuid.uuid4().hex
    password_db_string = hash_password(password, salt)

    fileobj = flask.request.files['file']
    filename = fileobj.filename

    # Generate a unique filename and save the file
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    fileobj.save(
        insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
        )

    connection.execute(
        'INSERT INTO users (username, fullname, email, filename, password) '
        'VALUES (?, ?, ?, ?, ?)',
        (username, fullname, email, uuid_basename, password_db_string)
    )

    flask.session['username'] = username
    target = flask.request.args.get('target')
    if not target:
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(target)


def delete_account(connection):
    """
    Delete the current user's account and any files associated with the user.

    :param connection: Database connection object.
    :return: Redirect to the index page or target URL.
    """
    if 'username' not in flask.session:
        return flask.abort(403)

    username = flask.session['username']
    cur = connection.execute(
        'SELECT filename FROM posts WHERE owner = ?',
        (username,)
    )
    posts = cur.fetchall()

    for post in posts:
        filename = post['filename']
        file_path = os.path.join(insta485.app.config["UPLOAD_FOLDER"],
                                 filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    connection.execute('DELETE FROM users WHERE username = ?', (username,))
    flask.session.clear()

    target = flask.request.args.get('target')
    if not target:
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(target)


def edit_account(connection):
    """
    Edit the current user's account details.

    :param connection: Database connection object.
    :return: Redirect to the index page or target URL.
    """
    if 'username' not in flask.session:
        return flask.abort(403)

    fullname = flask.request.form["fullname"]
    email = flask.request.form["email"]
    file = flask.request.files['file']
    username = flask.session['username']

    if not fullname or not email:
        return flask.abort(400)

    connection.execute(
        'UPDATE users SET fullname = ?, email = ? WHERE username = ?',
        (fullname, email, username)
    )

    if file:
        cur = connection.execute(
            'SELECT filename FROM users WHERE username = ?',
            (username,)
        )
        filename = cur.fetchone()["filename"]
        path = os.path.join(insta485.app.config["UPLOAD_FOLDER"], filename)
        os.remove(path)

        file_obj = flask.request.files["file"]
        filename = file_obj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        path = os.path.join(insta485.app.config["UPLOAD_FOLDER"],
                            uuid_basename)
        file_obj.save(path)

        connection.execute(
            'UPDATE users SET filename = ? WHERE username = ?',
            (uuid_basename, username)
        )

    target = flask.request.args.get('target')
    if not target:
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(target)


def change_password(connection):
    """
    Change the password of the current user after verifying the old password.

    :param connection: Database connection object.
    :return: Redirect to the index page or target URL.
    """
    if 'username' not in flask.session:
        return flask.abort(403)

    password = flask.request.form["password"]
    new_password1 = flask.request.form["new_password1"]
    new_password2 = flask.request.form["new_password2"]

    if not password or not new_password1 or not new_password2:
        return flask.abort(400)

    username = flask.session['username']
    cur = connection.execute(
        'SELECT password FROM users WHERE username = ?',
        (username,)
    )
    result = cur.fetchone()

    if not result:
        return flask.abort(403)

    real_password = result['password']
    password_list = real_password.split('$')
    salt = password_list[1]

    if hash_password(password, salt) != real_password:
        return flask.abort(403)

    if new_password1 != new_password2:
        return flask.abort(401)

    new_salt = uuid.uuid4().hex
    new_password_db_string = hash_password(new_password1, new_salt)

    connection.execute(
        'UPDATE users SET password = ? WHERE username = ?',
        (new_password_db_string, username)
    )

    target = flask.request.args.get('target')
    if not target:
        target = flask.redirect(flask.url_for('show_index'))
    return flask.redirect(target)


def hash_password(password, salt):
    """
    Generate a hashed password using the provided salt.

    :param password: Plaintext password.
    :param salt: Salt to append to the password before hashing.
    :return: Hashed password string.
    """
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    return "$".join([algorithm, salt, password_hash])
