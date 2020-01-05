from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    jsonify,
    abort,
    send_from_directory,
)
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from . import login
from app.models import User, Post, Family
import json
from sqlalchemy import exc
import random


@login.unauthorized_handler
def unauthorized():
    return abort(403)


@app.route("/")
def home():
    return render_template('index.html')


####################
#  AUTHENTICATION  #
####################


@app.route("/auth/register", methods=["POST"])
def apiRegister():
    """
    Register a new user
    """
    if current_user.is_authenticated:
        return {"acknowledged": False, "error": "Already Logged In"}
    try:
        body = json.loads(request.data)
        if len(User.query.filter_by(username=body["username"]).all()) > 0:
            return {"acknowledged": False, "error": "Use a different username"}
        if len(User.query.filter_by(email=body["email"]).all()) > 0:
            return {"acknowledged": False, "error": "Use a different email"}
        user = User(username=body["username"], email=body["email"], name=body["name"])
        user.set_password(body["password"])
        db.session.add(user)
        db.session.commit()
        return {"acknowledged": True}
    except exc.SQLAlchemyError as e:
        e = e.__dict__["orig"]
        print(e)
        return {"acknowledged": False, "error": "Unable to register"}


@app.route("/auth/login", methods=["POST"])
def apiLogin():
    """
    User login
    """
    body = json.loads(request.data)
    user = User.query.filter_by(username=body["username"]).first()
    if user is None or not user.check_password(body["password"]):
        return {"authenticated": False, "error": "Invalid username or password"}
    login_user(user, remember=False)
    return {"authenticated": True, "user": current_user.username}


@app.route("/auth/checklogin")
def checkLogin():
    """
    Check if user is logged in
    """
    if current_user.is_authenticated:
        return {"authenticated": True, "user": current_user.username}
    else:
        return {"authenticated": False}


@app.route("/auth/isAdmin")
@login_required
def checkAdmin():
    """
    Check if user is an admin
    """
    if current_user.is_admin:
        return {"is_admin": True}
    else:
        return {"is_admin": False}


@app.route("/auth/getuser")
def getUser():
    """
    Get the current users information
    """
    if current_user.is_authenticated:
        return {"authenticated": True, "user": current_user.serialize()}
    else:
        return {"authenticated": False}


@app.route("/auth/logout", methods=["POST"])
def apiLogout():
    """
    Log current user out
    """
    logout_user()
    return {"acknowledged": True}


##########
#  TEST  #
##########


@app.route("/test")
@login_required
def test():
    """
    Basic server test
    """
    return {"acknowledged": True, "msg": "Success"}


##########
#  POST  #
##########


@app.route("/post/addpost", methods=["POST"])
@login_required
def addpost():
    """
    Add a post
    """
    body = json.loads(request.data)
    post = Post(
        title=body["title"],
        notes=body["notes"],
        img_url=body["img_url"],
        item_url=body["item_url"],
        user_id=current_user.id,
    )
    db.session.add(post)
    db.session.commit()
    return {"acknowledged": True, "post": post.serialize()}


@app.route("/post/getposts")
@login_required
def getUserPosts():
    """
    Get all of current users posts
    """
    posts = current_user.get_posts()
    returnPosts = []
    for post in posts:
        returnPosts.append(post.serialize())
    return {"posts": returnPosts}


@app.route("/post/removepost", methods=["POST"])
@login_required
def removepost():
    """
    Remove a post from the current user
    """
    body = json.loads(request.data)
    deletePost = Post.query.filter_by(id=body["id"]).first()
    if deletePost.user_id == current_user.id:
        db.session.delete(deletePost)
        db.session.commit()
        return {"post": deletePost.serialize()}
    else:
        return {"authorized": False}


############
#  FAMILY  #
############


@app.route("/family/createfamily", methods=["POST"])
@login_required
def createFamily():
    """
    Create a Family
    """
    body = json.loads(request.data)
    key = random.randint(0, 999999999999)
    while Family.query.filter_by(key=key).first() is not None:
        key = random.randint(0, 999999999999)
    family = Family(name=body["name"], key=key, creator=current_user.username)
    db.session.add(family)
    db.session.commit()
    return {"family": family.serialize()}


@app.route("/family/addfamily", methods=["POST"])
@login_required
def addFamily():
    """
    Add a Family to current user
    """
    family_key = json.loads(request.data)["key"]
    family = Family.query.filter_by(key=family_key).first()
    if family is None:
        return {"error": "No families with that key"}
    current_user.set_family(family.id)
    db.session.commit()
    return {"family": family.serialize()}


@app.route("/family/getAllFamilies")
@login_required
def getAllFamilies():
    """
    Get a list of all available families
    """
    families = Family.query.all()
    familyList = []
    for family in families:
        familyList.append(family.serialize())
    return {"families": familyList}


@app.route("/family/getfamily")
@login_required
def getFamily():
    """
    Get Family of current user
    """
    family_id = current_user.family_id
    if family_id is None:
        return {"error": "No family available"}
    family = Family.query.filter_by(id=current_user.family_id).first()
    return {"family": family.serialize()}


@app.route("/family/removeFamily", methods=["DELETE"])
@login_required
def removeFamily():
    """
    Remove family from current user
    """
    current_user.set_family(None)
    db.session.commit()
    user = User.query.filter_by(username=current_user.username).first()
    if user.family_id is None:
        return {"family_id": current_user.family_id}
    else:
        return {"error": "Unable to remove family"}


@app.route("/family/familyPosts")
@login_required
def familyPosts():
    """
    Get family posts
    """
    family_id = current_user.family_id
    users = User.query.filter_by(family_id=family_id).all()
    posts = []
    postList = []
    userList = []
    for user in users:
        posts.append({"user": user.name, "posts": user.get_serialized_posts()})
        userList.append(user.serialize())
        postList = postList + user.get_serialized_posts()
    return {"users": userList, "posts": posts}


###########
#  ADMIN  #
###########


@app.route("/admin/users/get", methods=["GET"])
@login_required
def adminUsersGet():
    """
    Admin - get users
    """
    if current_user.is_admin:
        users = User.query.all()
        userList = []
        for user in users:
            userList.append(user.serialize())
        return {"users": userList}
    return abort(403)


@app.route("/admin/users/create", methods=["POST"])
@login_required
def adminUsersCreate():
    """
    Admin - create user
    """
    if current_user.is_admin:
        try:
            body = json.loads(request.data)
            if len(User.query.filter_by(username=body["username"]).all()) > 0:
                return {"acknowledged": False, "error": "Use a different username"}
            if len(User.query.filter_by(email=body["email"]).all()) > 0:
                return {"acknowledged": False, "error": "Use a different email"}
            user = User(username=body["username"], email=body["email"], name=body["name"], is_admin=body["is_admin"])
            user.set_password(body["password"])
            db.session.add(user)
            db.session.commit()
            return {"acknowledged": True}
        except exc.SQLAlchemyError as e:
            e = e.__dict__["orig"]
            print(e)
            return {"acknowledged": False, "error": "Unable to register, check logs for error"}
    return abort(403)


@app.route("/admin/users/edit", methods=["POST"])
@login_required
def adminUsersEdit():
    """
    Admin - edit user
    """
    if current_user.is_admin:
        body = json.loads(request.data)
        id = body["id"]
        user = User.query.filter_by(id=id).first()
        if user is None:
            user = User.query.filter_by(username=body["username"]).first()
            if user is None:
                return {"acknowledged": False, "error": "No user with id or username is detected"}
        user.name = body["name"]
        user.email = body["email"]
        user.is_admin = body["is_admin"]
        db.session.commit()
        return {"acknowledged": True}
    return abort(403)


@app.route("/admin/users/delete", methods=["POST"])
@login_required
def adminUsersDelete():
    """
    Admin - delete user
    """
    if current_user.is_admin:
        body = json.loads(request.data)
        id = body["id"]
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return {"acknowledged": True}
    return abort(403)


@app.route("/admin/posts/get", methods=["GET"])
@login_required
def adminPostsGet():
    """
    Admin - get posts
    """
    if current_user.is_admin:
        posts = Post.query.all()
        postList = []
        for post in posts:
            newPost = post.serialize()
            username = User.query.filter_by(id=post.user_id).first().username
            newPost["username"] = username
            postList.append(newPost)
        return {"posts": postList}
    return abort(403)


@app.route("/admin/posts/edit", methods=["POST"])
@login_required
def adminPostsEdit():
    """
    Admin - edit post
    """
    if current_user.is_admin:
        body = json.loads(request.data)
        id = body["id"]
        post = Post.query.filter_by(id=id).first()
        if post is None:
            return {"acknowledged": False, "error": "No post with that id is detected"}
        post.title = body["title"]
        post.notes = body["notes"]
        post.item_url = body["item_url"]
        post.img_url = body["img_url"]
        db.session.commit()
        return {"acknowledged": True}
    return abort(403)


@app.route("/admin/posts/delete", methods=["POST"])
@login_required
def adminPostsDelete():
    """
    Admin - delete post
    """
    if current_user.is_admin:
        body = json.loads(request.data)
        id = body["id"]
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        return {"acknowledged": True}
    return abort(403)


@app.route("/admin/families/get", methods=["GET"])
@login_required
def adminFamiliesGet():
    """
    Admin - get posts
    """
    if current_user.is_admin:
        families = Family.query.all()
        familyList = []
        for family in families:
            familyList.append(family.serialize())
        return {"families": familyList}
    return abort(403)


@app.route("/admin/families/edit", methods=["POST"])
@login_required
def adminFamiliesEdit():
    """
    Admin - edit post
    """
    if current_user.is_admin:
        body = json.loads(request.data)
        id = body["id"]
        family = Family.query.filter_by(id=id).first()
        if family is None:
            return {"acknowledged": False, "error": "No family with that id is detected"}
        family.name = body["name"]
        db.session.commit()
        return {"acknowledged": True}
    return abort(403)


@app.route("/admin/families/delete", methods=["POST"])
@login_required
def adminFamiliesDelete():
    """
    Admin - delete post
    """
    if current_user.is_admin:
        body = json.loads(request.data)
        id = body["id"]
        family = Family.query.filter_by(id=id).first()
        db.session.delete(family)
        db.session.commit()
        return {"acknowledged": True}
    return abort(403)
