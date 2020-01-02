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
    # return {'authorized': False}
    return abort(403)


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
    # TODO: Catch this error (enter an invalid family id)
    families = Family.query.filter_by(key=family_key).limit(1).all()
    if len(families) == 0:
        return {"error": "No families with that key"}
    family = families[0]
    current_user.set_family(family.id)
    db.session.commit()
    return {"family": family.serialize()}


@app.route("/family/getfamily")
@login_required
def getFamily():
    """
    Get Family of current user
    """
    family_id = current_user.family_id
    if family_id is None:
        return {"error": "No family available"}
    family = Family.query.filter_by(id=current_user.family_id).limit(1).all()[0]
    return {"family": family.serialize()}


@app.route("/family/removefamily", methods=["DELETE"])
@login_required
def removeFamily():
    """
    Remove family from current user
    """
    current_user.set_family(None)
    db.session.commit()
    user = User.query.filter_by(username=current_user.username).limit(1).all()[0]
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
    return False


###########
#  ADMIN  #
###########


@app.route("/admin/getallusers")
@login_required
def getallusers():
    """
    Get all of current users posts
    """
    if not current_user.is_admin:
        return {"authorized": False}
    users = User.query.all()
    returnUsers = []
    for user in users:
        returnUsers.append(user.serialize())
    return {"users": returnUsers}


@app.route("/admin/getallposts")
@login_required
def getallpost():
    """
    Get all of current users posts
    """
    if not current_user.is_admin:
        return {"authorized": False}
    posts = Post.query.all()
    returnPosts = []
    for post in posts:
        returnPosts.append(post.serialize())
    return {"posts": returnPosts}


@app.route("/admin/getallfamilies")
@login_required
def getallfamilies():
    """
    Get all of current users posts
    """
    if not current_user.is_admin:
        return {"authorized": False}
    families = Family.query.all()
    returnFamilies = []
    for family in families:
        returnFamilies.append(family.serialize())
    return {"families": returnFamilies}


@app.route("/admin/deletefamily", methods=["DELETE"])
@login_required
def deleteFamily():
    """
    Delete family
    """
    family_id = json.loads(request.data)["id"]
    families = Family.query.filter_by(id=family_id).limit(1).all()
    if len(families) == 0:
        return {"error": "No families with that id"}
    db.session.delete(family)
    db.session.commit()
    user = User.query.filter_by(username=current_user.username).limit(1).all()[0]
    return {"acknowledged": True}
