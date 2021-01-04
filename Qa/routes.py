from flask import Flask
from flask import _app_ctx_stack, abort, render_template, redirect, request, session, url_for
from Qa import models, app
from Qa.qa_db import *
from Qa.database import SessionLocal, engine
from sqlalchemy.orm import scoped_session

models.Base.metadata.create_all(bind=engine)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

@app.route("/API/qa/question/<int:id>/", methods=['GET'])
def returnSingleQuestionJSON(id):
    try:
        q = {"question": getQuestionDICT(id)}
        return q
    except:
        abort(404)

@app.route("/API/qa/answer/<int:id>/", methods=['GET'])
def returnsAnswerJSON(id):
    try:
        answer = {"answer": getAnswerDICT(id)}
        return answer
    except Exception as e:
        print(e)
        abort(404)


@app.route("/API/qa/question/<int:id>/", methods=['POST'])
def createNewQuestion(id):
    j = request.get_json()
    ret = False
    try:
        ret = newQuestion(id, j['curr_time'], j['user'], j['uname'], j['text'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

@app.route("/API/qa/answer/<int:id>/", methods=['POST'])
def createNewAnswer(id):
    j = request.get_json()
    ret = False
    try:
        ret = newAnswer(id, j['a_user'], j['a_uname'], j['a_text'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409