"""REST API for posts."""
import flask
import insta485
from insta485.views.accounts import hash_password
import uuid


def verify_auth(connection, username, password):
    query = """
        SELECT password
        FROM users
        WHERE username = ?
    """
    result = connection.execute(query, (username,)).fetchone()
    if result is None:
        return False
    
    if result["password"] == password:
        return True
    return False

def is_authenticated(connection):
    auth = flask.request.authorization

    # 1. HTTP Basic Auth
    if auth:
        username = auth.username
        password = auth.password
        return verify_auth(connection, username, password)

    # 2. Session-based Authentication
    if 'username' in flask.session:
        return True

    return False

    

@insta485.app.route('/api/v1/posts/')
def get_posts():
    connection = insta485.model.get_db()

    if not is_authenticated(connection):
        return flask.jsonify({"message": "Unauthorized", "status_code": 403}),403
    
    if 'username' in flask.session:
        username = flask.session['username']
    else:
        auth = flask.request.authorization
        username = auth.username

    #Check login user username and password
    #if not verify_auth(connection, username, password):
      #  return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    size = flask.request.args.get('size', default = 10, type=int)
    page = flask.request.args.get('page', default = 0, type=int)
 

    most_recent_post_id = """
        SELECT postid
        FROM posts
        ORDER by postid DESC
        LIMIT 1
    """
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
        
    if size == 0 or page < 0:
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

    next = ""
    if len(posts) >= size:
        next = f"/api/v1/posts/?size={size}&page={page+1}&postid_lte={postid_lte}"
    
    response = {
        "next": next,
        "results": [{"postid": post['postid'], 
                     "url": f"/api/v1/posts/{post['postid']}/"} 
                     for post in posts],
        "url": url
    }
    return flask.jsonify(response), 200




@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Return post on postid.

    Example:
    {
      "created": "2017-09-28 04:33:28",
      "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
      "owner": "awdeorio",
      "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "ownerShowUrl": "/users/awdeorio/",
      "postShowUrl": "/posts/1/",
      "postid": 1,
      "url": "/api/v1/posts/1/"
    }
    """
    context = {
        "created": "2017-09-28 04:33:28",
        "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
        "owner": "awdeorio",
        "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
        "ownerShowUrl": "/users/awdeorio/",
        "postShowUrl": f"/posts/{postid_url_slug}/",
        "postid": postid_url_slug,
        "url": flask.request.path,
    }
    return flask.jsonify(**context)
