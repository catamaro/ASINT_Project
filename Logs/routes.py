from Logs import app
from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for
from Logs.logs import *

from sqlalchemy.orm import scoped_session
from flask import Flask, _app_ctx_stack
from Logs import models
from Logs.database import SessionLocal, engine

import json

models.Base.metadata.create_all(bind=engine)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.route("/API/logs/", methods=['GET'])
def returnLogsJSON():
    lists = listLogsDICT()
    return {"events": lists[0], "data_creation": lists[1]}

@app.route('/API/logs/event/', methods = ["POST"])
def create_log_event():
    j = request.get_json()
    j = json.loads(j)
    ret = False
    try:
        ret = newEvent(j["IP"], j['endpoint'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)

@app.route('/API/logs/data_creation/', methods = ["POST"])
def create_log_data_creation():
    j = request.get_json()
    j = json.loads(j)
    ret = False
    try:
        ret = newDataCreation(j["data_type"], j["content"], j["user"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)