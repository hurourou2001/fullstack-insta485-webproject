"""REST API for posts."""
import logging
import flask
import insta485
from insta485.views.accounts import hash_password


def verify_auth(connection, username, password):
    """Verify user authentication."""
    query = """
        SELECT password
        FROM users
        WHERE username = ?
    """
    result = connection.execute(query, (username,)).fetchone()
    if result is None:
        return False

    salt = result["password"].split('$')[1]

    if result["password"] == hash_password(password, salt):
        return True
    return False


def is_authenticated(connection):
    """Check if a user is authenticated."""
    auth = flask.request.authorization
    username = ""
    password = ""
    if auth:
        username = auth['username']
        password = auth['password']
        return verify_auth(connection, username, password)

    if 'username' in flask.session:
        username = flask.session['username']
        return True

    return False


@insta485.app.route("/api/v1/posts/")
def get_posts():
    """Return a list of posts."""
    logging.info("Received a GET request for posts")
    connection = insta485.model.get_db()

    if not is_authenticated(connection):
        return flask.jsonify({"message": "Forbidden",
                              "status_code": 403}), 403

    if 'username' in flask.session:
        username = flask.session['username']
    else:
        auth = flask.request.authorization
        username = auth.username

    size = flask.request.args.get('size', default=10, type=int)

    if size < 0:
        return flask.jsonify({"message": "Bad Request",
                              "status_code": 400}), 400
    page = flask.request.args.get('page', default=0, type=int)

    postid_lte = flask.request.args.get('postid_lte')
    if postid_lte is None:
        most_recent_post_id = """
            SELECT postid
            FROM posts
            WHERE (owner = ? OR owner in (
                SELECT username2
                FROM following
                WHERE username1 = ?))
            ORDER BY postid DESC
            LIMIT 1
        """
        rst = connection.execute(most_recent_post_id,
                                 (username, username)).fetchone()
        postid_lte = rst["postid"]

    if size <= 0 or page < 0:
        return flask.jsonify({"message": "Bad Request",
                              "status_code": 400}), 400
    url = flask.request.full_path
    if url.endswith('?'):
        url = url[:-1]
    query = """
        SELECT postid
        FROM posts
        WHERE (owner = ? OR owner in (
            SELECT username2
            FROM following
            WHERE username1 = ?))
        AND postid <= ?
        ORDER BY postid DESC
        LIMIT ? OFFSET ?
    """
    params = [username, username, postid_lte, size, page*size]
    posts = connection.execute(query, params).fetchall()

    nxt = ""
    if len(posts) >= size:
        nxt = (
         f"/api/v1/posts/?size={size}&page={page+1}&postid_lte={postid_lte}"
        )

    response = {
        "next": nxt,
        "results": [{"postid": post['postid'],
                     "url": f"/api/v1/posts/{post['postid']}/"}
                    for post in posts],
        "url": url
    }
    return flask.jsonify(response), 200


@insta485.app.route("/api/v1/posts/<int:postid_url_slug>/")
def get_post_id(postid_url_slug):
    """Return post on postid."""
    connection = insta485.model.get_db()

    if not is_authenticated(connection):
        return flask.jsonify({"message": "Forbidden",
                              "status_code": 403}), 403

    if 'username' in flask.session:
        username = flask.session['username']
    else:
        auth = flask.request.authorization
        username = auth.username

    postid = postid_url_slug

    query_posts = connection.execute("""
        SELECT created, filename, owner FROM posts
        WHERE postid = ?
        """, (postid, )).fetchone()

    if query_posts is None:
        return flask.jsonify({"message": "Not Found",
                              "Status_code": 404}), 404

    query_comments = connection.execute("""
          SELECT commentid, owner, text, created
          FROM comments
          WHERE postid = ?
        """, (postid, )).fetchall()

    query_like = connection.execute("""
        SELECT likeid
        FROM likes
        WHERE postid = ? AND owner = ?
        """, (postid, username)).fetchone()

    query_likenum = connection.execute("""
        SELECT likeid
        FROM likes
        WHERE postid = ?
        """, (postid, )).fetchall()

    if query_like is not None:
        lkes = {
            "lognameLikesThis": True,
            "numLikes": len(query_likenum),
            "url": f"/api/v1/likes/{query_like['likeid']}/"
        }
    else:
        lkes = {
            "lognameLikesThis": False,
            "numLikes": len(query_likenum),
            "url": None
        }

    query_user = connection.execute(
        """
        SELECT filename
        FROM users
        WHERE username = ?
        """, (query_posts['owner'], )).fetchone()

    response = {
        "comments": [
            {
                "commentid": comment['commentid'],
                "lognameOwnsThis": (
                    username == comment['owner']
                ),
                "owner": comment['owner'],
                "ownerShowUrl": f"/users/{comment['owner']}/",
                "text": comment['text'],
                "url": f"/api/v1/comments/{comment['commentid']}/"
            }
            for comment in query_comments
        ],
        "comments_url": f"/api/v1/comments/?postid={postid}",
        "created": query_posts['created'],
        "imgUrl": f"/uploads/{query_posts['filename']}",
        "likes": lkes,
        "owner": query_posts['owner'],
        "ownerImgUrl": f"/uploads/{query_user['filename']}",
        "ownerShowUrl": f"/users/{query_posts['owner']}/",
        "postShowUrl": f"/posts/{postid}/",
        "postid": postid,
        "url": f"/api/v1/posts/{postid}/"
    }

    return flask.jsonify(response), 200


@insta485.app.route("/api/v1/comments/", methods=["POST"])
def add_comment():
    """Update a post with a comment."""
    connection = insta485.model.get_db()

    if not is_authenticated(connection):
        return flask.jsonify({"message": "Unauthorized",
                              "status_code": 403}), 403

    if 'username' in flask.session:
        username = flask.session['username']
    else:
        auth = flask.request.authorization
        username = auth.username

    text = flask.request.json.get("text")
    postid = flask.request.args.get('postid')
    query_posts = connection.execute("""
        SELECT * FROM posts WHERE postid = ?""", (postid,)).fetchone()

    if not query_posts:
        return flask.jsonify({"message": "Not Found",
                              "Status Code": 404}), 404

    connection.execute(
        """
        INSERT INTO comments(postid, owner, text)
        VALUES(?,?,?)
        """, (postid, username, text))

    new_comment = connection.execute(
        """
        SELECT last_insert_rowid() AS commentid
        """
    ).fetchone()['commentid']

    response = {
        "commentid": new_comment,
        "lognameOwnsThis": True,
        "owner": username,
        "ownerShowUrl": f"/users/{username}/",
        "text": text,
        "url": f"/api/v1/comments/{new_comment}/"
    }

    return flask.jsonify(response), 201


@insta485.app.route("/api/v1/comments/<commentid>/", methods=["DELETE"])
def delete_comment(commentid):
    """Delete a comment."""
    connection = insta485.model.get_db()

    if not is_authenticated(connection):
        return flask.jsonify({"message": "Unauthorized",
                              "status_code": 403}), 403

    if 'username' in flask.session:
        username = flask.session['username']
    else:
        auth = flask.request.authorization
        username = auth.username

    if not commentid:
        return flask.jsonify({"message": "Not Found",
                              "Status Code": 404}), 404

    comment = connection.execute("""
                                SELECT *
                                FROM comments
                                WHERE commentid = ?
                                """, (commentid,)).fetchone()

    if not comment:
        return flask.jsonify({"message": "Not Found",
                              "Status Code": 404}), 404

    comment_owner = connection.execute("""
                                        SELECT owner
                                        FROM comments
                                        WHERE commentid = ?
                                    """, (commentid,)).fetchone()['owner']

    if username != comment_owner:
        return flask.jsonify({"message": "Unauthorized",
                              "status_code": 403}), 403

    connection.execute(
        """
        DELETE FROM comments WHERE commentid = ?
        """, (commentid,))

    connection.commit()

    return '', 204
