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


@app.route('/login')
def login():
    if fenix_blueprint.session.authorized:
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")

        data = resp.json()
        try:
            newUser(data['username'], data['name'])
        except:
            abort(400)
            # the arguments were incorrect

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


@app.route('/API/user/<ist_id>', methods=['GET'])
def getUser(ist_id):
    try:
        v = getUserDICT(ist_id)
        return v
    except:
        abort(404)


""" @app.route('/API/get_user/', methods=['GET'])
def getUser():

    loggedIn = fenix_blueprint.session.authorized
    if loggedIn:
        # if the user is authenticated then a request to FENIX is made
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        # res contains the responde made to /api/fenix/vi/person (information about current user)
        data = resp.json()
        print(resp.json())
    else:
        abort(400)


@app.route('/logout')
def logout():
    # this clears all server information about the access token of this connection
    res = str(session.items())
    print(res)
    session.clear()
    res = str(session.items())
    print(res)
    # when the browser is redirected to home page it is not logged in anymore
    return redirect(url_for("home_page"))


@app.route('/private')
def private_page():
    # this page can only be accessed by a authenticated user

    # verification of the user is  logged in
    if fenix_blueprint.session.authorized == False:
        # if not logged in browser is redirected to login page (in this case FENIX handled the login)
        return redirect(url_for("fenix-example.login"))
    else:
        # if the user is authenticated then a request to FENIX is made
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        # res contains the responde made to /api/fenix/vi/person (information about current user)
        data = resp.json()
        print(resp.json())
        return render_template("privPage.html", username=data['username'], name=data['name'])
 """
