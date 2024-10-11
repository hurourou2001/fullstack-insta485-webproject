import flask
import insta485
from insta485.views.accounts import hash_password

@insta485.app.route('/api/v1/likes/', methods=["POST"])
def create_like():
    connection = insta485.model.get_db()
    if not insta485.api.posts.is_authenticated(connection):
        return flask.jsonify({"message": "Unauthorized", "status_code": 403}),403
    
    #postid = flask.request.args.get('postid', type=int)
    url = flask.request.path
    username = ""
    if "username" in flask.session:
        username = flask.session["username"]
    else:
        username = flask.request.authorization.username
    postid = flask.request.args.get('postid', type=int)
    # if postid is None:
    #     postid = flask.request.json.get('postid', type=int)
    if postid is None:
        return flask.jsonify({"message": "no postid", "status_code": 400}), 400
    
    check_exist_like = """
        SELECT likeid
        FROM likes
        WHERE postid = ? AND owner = ?
    """
    cur = connection.execute(check_exist_like, (postid, username))
    rst = cur.fetchone()
    if rst is not None:
        return flask.jsonify({"likeid": rst["likeid"],
                              "url": f"{url}{rst['likeid']}/"}), 200
    
    add_like = """
        INSERT INTO likes (owner, postid)
        VALUES (?, ?)
    """
    cur = connection.execute(add_like, (username, postid))
    likeid = cur.lastrowid

    return flask.jsonify({
        "likeid": likeid,
        "url": f"{url}{likeid}/"
    }), 201


@insta485.app.route('/api/v1/likes/<int:likeid>/', methods=["DELETE"])
def delete_like(likeid):
    connection = insta485.model.get_db()
    if not insta485.api.posts.is_authenticated(connection):
        return flask.jsonify({"message": "Unauthorized", "status_code": 403}),403
    
    if "username" in flask.session:
        user = flask.session["username"]
    else:
        user = flask.request.authorization.get("username")
    check_q = """
        SELECT likeid, owner
        FROM likes
        WHERE likeid = ?
    """

    rst = connection.execute(check_q, (likeid,)).fetchone()
    if rst is None:
        return flask.jsonify({
                            "message": "Like not found",
                            "status_code": 404
                            }), 404

    if rst["owner"] != user:
        return flask.jsonify({
                            "message": "Forbidden",
                            "status_code": 403
                            }), 403
    
    delete_q = """
        DELETE FROM likes
        WHERE likeid = ?
    """
    connection.execute(delete_q, (likeid,))
    return "", 204

