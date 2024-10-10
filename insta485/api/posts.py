"""REST API for posts."""
import flask
import insta485
from insta485.views.accounts import hash_password
import uuid
import logging


def verify_auth(connection, username, password):
    query = """
        SELECT password
        FROM users
        WHERE username = ?
    """
    result = connection.execute(query, (username,)).fetchone()
    if result is None:
        return False

    alg, salt, hash = result["password"].split('$')

    if result["password"] == hash_password(password, salt):
        return True
    return False

# 

def is_authenticated(connection):
    auth = flask.request.authorization
    #print(auth.password)
    # 1. HTTP Basic Auth
    username = ""
    password = ""
    if auth:
        username = auth['username']
        password = auth['password']
        return verify_auth(connection, username, password)

    # 2. Session-based Authentication
    if 'username' in flask.session:
        username = flask.session['username']
        # password = flask.request.form['password']
        return True

    return False

    

@insta485.app.route("/api/v1/posts/")
def get_posts():
    logging.info("Received a GET request for posts")
    connection = insta485.model.get_db()

    if not is_authenticated(connection):
        return flask.jsonify({"message": "Forbidden", "status_code": 403}),403
    
    if 'username' in flask.session:
        username = flask.session['username']
    else:
        auth = flask.request.authorization
        username = auth.username

    #Check login user username and password
    #if not verify_auth(connection, username, password):
      #  return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    size = flask.request.args.get('size', default = 10, type=int)

    if size < 0:
        return flask.jsonify({"message":"Bad Request", "status_code": 400}),400
    page = flask.request.args.get('page', default = 0, type=int)
 

    # most_recent_post_id = """
    #     SELECT postid
    #     FROM posts
    #     ORDER by postid DESC
    #     LIMIT 1
    # """
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


@insta485.app.route("/api/v1/posts/<int:postid_url_slug>/")
def get_post_id(postid_url_slug): 
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
    connection = insta485.model.get_db()

    if not is_authenticated(connection):
        return flask.jsonify({"message": "Forbidden", "status_code": 403}),403
    
    if 'username' in flask.session:
        username = flask.session['username']
    else:
        auth = flask.request.authorization
        username = auth.username
    
    postid = postid_url_slug

    queryPosts = connection.execute("""
        SELECT created, filename, owner                        
        FROM posts
        WHERE postid = ?
        """
    ,(postid,)).fetchone()

    if queryPosts is None:
        return flask.jsonify({"message":"Not Found","Status_code":404}),404

    queryComments = connection.execute("""
          SELECT commentid, owner, text, created
          FROM comments
          WHERE postid = ?
        """
        , (postid,)).fetchall()
    
    queryLike = connection.execute("""
        SELECT likeid
        FROM likes
        WHERE postid = ? AND owner = ?
        """, (postid, username)).fetchone()
    
    queryLikeNum = connection.execute("""
        SELECT likeid
        FROM likes
        WHERE postid = ?
        """, (postid,)).fetchall()
    
    if queryLike is not None:
        Likes = {
            "lognameLikesThis": True,
            "numLikes": len(queryLikeNum),
            "url":f"/api/v1/likes/{queryLike['likeid']}/"
        }
    else:
        Likes = {
            "lognameLikesThis": False,
             "numLikes": len(queryLikeNum),
            "url":None
        }
    
    queryUser = connection.execute(
        """
        SELECT filename
        FROM users
        WHERE username = ?
        """,(queryPosts['owner'],)).fetchone()
    
    response = {
        "comments" :[
            {
                "commentid": comment['commentid'],
                "lognameOwnsThis":True if username == comment['owner'] else False,
                "owner":comment['owner'],
                "ownerShowUrl":f"/users/{comment['owner']}/",
                "text":comment['text'],
            "url":f"/api/v1/comments/{comment['commentid']}/"
            }
            for comment in queryComments 
        ],
        "comments_url": f"/api/v1/comments/?postid={postid}",
        "created": queryPosts['created'],
        "imgUrl": f"/uploads/{queryPosts['filename']}",
        "likes" : Likes,
        "owner": queryPosts['owner'],
        "ownerImgUrl": f"/uploads/{queryUser['filename']}",
        "ownerShowUrl": f"/users/{queryPosts['owner']}/",
        "postShowUrl": f"/posts/{postid}/",
        "postid":postid,
        "url": f"/api/v1/posts/{postid}/"
    }
    
    return flask.jsonify(response),200

@insta485.app.route("/api/v1/comments/", methods=["POST"])
def addComment():
    """
    Update a post with a comment.
    """
    connection = insta485.model.get_db()

    if not is_authenticated(connection):
        return flask.jsonify({"message": "Unauthorized", "status_code": 403}),403
    
    if 'username' in flask.session:
        username = flask.session['username']
    else:
        auth = flask.request.authorization
        username = auth.username

    text = flask.request.json.get("text")
    postid = flask.request.args.get('postid')
    queryPosts = connection.execute("""
        SELECT * FROM posts WHERE postid = ?""",    
        (postid,)).fetchone()
    
    if not queryPosts:
        return flask.jsonify({"message":"Not Found", "Status Code": 404}),404                      
                                    
    connection.execute(
        """
        INSERT INTO comments(postid, owner, text)
        VALUES(?,?,?)
        """, (postid, username, text))
    
    newComment = connection.execute(
        """
        SELECT last_insert_rowid() AS commentid
        """
    ).fetchone()['commentid']

    

    response = {
         "commentid": newComment,
        "lognameOwnsThis": True,
         "owner": username,
        "ownerShowUrl": f"/users/{username}/",
        "text": text,
        "url": f"/api/v1/comments/{newComment}/"
    }

    return flask.jsonify(response),201

@insta485.app.route("/api/v1/comments/<commentid>/", methods = ["DELETE"])
def deleteComment(commentid):
    connection = insta485.model.get_db()

    if not is_authenticated(connection):
        return flask.jsonify({"message": "Unauthorized", "status_code": 
                              403}),403
    
    if 'username' in flask.session:
        username = flask.session['username']
    else:
        auth = flask.request.authorization
        username = auth.username
    
    if not commentid:
        return flask.jsonify({"message":"Not Found", "Status Code": 
                              404}),404
    
    comment = connection.execute("""
        SELECT * FROM comments WHERE commentid = ?""",
        (commentid,)).fetchone()
    
    if not comment:
        return flask.jsonify({"message":"Not Found", "Status Code": 404}),404
   
    commentOwner = connection.execute("""
    SELECT owner FROM comments WHERE commentid = ?""",
    (commentid,)).fetchone()['owner']
    
    if username != commentOwner:
        return flask.jsonify({"message": "Unauthorized", "status_code": 
                              403}),403

    connection.execute(
        """
        DELETE FROM comments WHERE commentid = ?
        """, (commentid,))
    
    connection.commit()

    return '', 204
