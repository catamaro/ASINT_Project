from flask import Flask
from flask import _app_ctx_stack, abort, render_template, redirect, request, session, url_for, jsonify
from UserManager import app, fenix_blueprint, models

from UserManager.user_manager import *
from UserManager.database import SessionLocal, engine
from sqlalchemy.orm import scoped_session

models.Base.metadata.create_all(bind=engine)

app.session = scoped_session(
    SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
app.session.expire_on_commit = False


@app.route('/')
def login():
    
    if fenix_blueprint.session.authorized:
        try:
            resp = fenix_blueprint.session.get("/api/fenix/v1/person/")

            data = resp.json()
            try:
                print(data)
                newUser(data['username'], data['name'])
            except:
                abort(400)
                # the arguments were incorrect
        except:
            return redirect(url_for('fenix-example.login'))
        return redirect("http://127.0.0.1:5005/redirect_login?id="+data['username']+'&name='+data['name'])
    return redirect(url_for('fenix-example.login'))


@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()

    user = app.session.query(User).filter(
        User.ist_id == data["ist_id"]).first()
    
    user.auth = False

    app.session.commit()
    app.session.close()

    return {"auth": False}


@app.route('/API/user/<ist_id>/<name>/', methods=['GET'])
def getUser(ist_id, name):
    print("im here?")
    try:
        v = getUserDICT(ist_id, name)
        return v
    except:
        abort(404)

