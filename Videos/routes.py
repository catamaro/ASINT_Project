from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for
from Videos import app
from Videos.videos_db import *

from sqlalchemy.orm import scoped_session
from flask import Flask, _app_ctx_stack
from Videos import models
from Videos.database import SessionLocal, engine


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
        ret = newVideo(j["description"], j['url'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

@app.route("/API/videos/<int:id>/")
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


