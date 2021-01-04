from Stats import app
from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for
from Stats.stats import *

from sqlalchemy.orm import scoped_session
from flask import Flask, _app_ctx_stack
from Stats import models
from Stats.database import SessionLocal, engine

import json

models.Base.metadata.create_all(bind=engine)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.route("/API/stats/", methods=['GET'])
def returnStatsJSON():
    return {"stats": listStatsDICT()}

@app.route('/API/stats/', methods = ["POST"])
def create_stats():
    j = request.get_json()
    j = json.loads(j)
    ret = False
    try:    
        ret = newUser_Stats(j["user"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        return "id is already in uses"

@app.route("/API/stats/update/<user>/<data_type>/", methods=['PUT', 'PATCH'])
def newStats(user, data_type):
    try:
        return {"stats": updateUser_Stats(user,data_type)}
    except:
        abort(404)