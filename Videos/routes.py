from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for
from Videos import app
from Videos.videos_db import *

@app.route("/API/videos/", methods=['GET'])
def returnsVideosJSON():
    return {"videos": listVideosDICT()}


@app.route("/API/videos/<int:id>/")
def returnSingleVideoJSON(id):
    try:
        v = getVideoDICT(id)
        return v
    except:
        abort(404)


@app.route("/API/videos/", methods=['POST'])
def createNewVideo():
    j = request.get_json()
    ret = False
    try:
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


@app.route("/API/videos/<int:id>/views", methods=['PUT', 'PATCH'])
def newView(id):
    try:
        return {"id":id, "views": newVideoView(id)}
    except:
        abort(404)


