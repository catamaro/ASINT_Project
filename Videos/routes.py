from flask import Flask
from flask import _app_ctx_stack, abort, render_template, redirect, request, session, url_for
from Videos import models, app
from Videos.videos_db import *
from Videos.database import SessionLocal, engine
from sqlalchemy.orm import scoped_session

models.Base.metadata.create_all(bind=engine)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
app.session.expire_on_commit = False

@app.route("/")
def index():
   return render_template("index.html")

from sqlalchemy.orm import scoped_session
from flask import Flask, _app_ctx_stack
from Videos import models
from Videos.database import SessionLocal, engine
import json

models.Base.metadata.create_all(bind=engine)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.route("/API/videos/", methods=['GET'])
def returnsVideosJSON():
    return {"videos": listVideosDICT()}

@app.route("/API/videos/", methods=['POST'])
def createNewVideo():
    j = request.get_json()
    ret = False
    try:
        print(j)
        print(j["description"])
        ret = newVideo(j["description"], j['url'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

@app.route("/API/videos/<int:id>/", methods=['GET'])
def returnSingleVideoJSON(id):
    try:
        v = getVideoDICT(id)
        return v
    except:
        abort(404)

@app.route("/API/videos/<int:id>/views", methods=['PUT', 'PATCH'])
def newView(id):
    try:
        return {"id":id, "views": newVideoView(id)}
    except:
        abort(404)


