from flask import Flask,  _app_ctx_stack
from flask import abort, render_template, redirect, session, url_for, request, flash
from Proxy import app, models
from Proxy.proxy import check_port, listServicesDICT, verify_user
from Proxy.models import MicroServices
from Proxy.forms import ServiceForm
from Proxy.database import SessionLocal, engine

import requests 
import json

from sqlalchemy.orm import scoped_session

models.Base.metadata.create_all(bind=engine)

app.session = scoped_session(
    SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

#----------------------------------logs and stats-------------------------------------#

# logs handler
@app.before_request
def before_req():
    if(request.method == 'GET'):
        IP = request.host
        endpoint = request.path

        # ignores java sript requests
        if endpoint.split('/', 2)[1] != "static":
            # make REST request to logs micro service
            request_data = {"IP": IP, "endpoint": endpoint}
            try:
                resp = requests.post("http://127.0.0.1:5003/API/logs/event",
                                     json=json.dumps(request_data))
            except:
                flash("Logs service is down")

    elif(request.method == 'POST'):
        if request.url.find("video") != -1:
            data_type = "video"
        elif request.url.find("question") != -1:
            data_type = "question"
        elif request.url.find("answer") != -1:
            data_type = "answer"
        else:
            return

        user = request.json.get("user")
        content = json.dumps(request.json)

        # make REST request to logs micro service
        data = {"data_type": data_type, "content": content, "user": user}
        try:
            requests.post(
                "http://127.0.0.1:5003/API/logs/data_creation", json=json.dumps(data))
            requests.put(
                "http://127.0.0.1:5006/API/stats/update/"+user+"/"+data_type)
        except:
            flash("Logs service is down")

        try:
            requests.post(
                "http://127.0.0.1:5003/API/logs/data_creation", json=json.dumps(data))
        except:
            flash("Logs service is down")

    elif(request.method == 'PUT' or request.method == 'PATCH'):
        url = request.url.split('/')
        video = url[5]
        if request.url.find("view") != -1:
            data_type = "view"

        user = request.json.get("user")
        content = json.dumps(request.json)

        # make REST request to logs micro service
        data = {"data_type": data_type, "content": content, "user": user}
        try:
            requests.post(
                "http://127.0.0.1:5003/API/logs/data_creation", json=json.dumps(data))
            requests.put(
                "http://127.0.0.1:5006/API/stats/update/"+user+"/"+data_type)
        except:
            flash("Logs service is down")

#------------------------------------proxy URI----------------------------------------#

@app.route("/<path:page>")
@app.route("/")
def pages(page="index"):
    name = request.args.get("name", None)
    ist_id = request.args.get("ist_id", None)
    id = request.args.get("id", None)

    html_url = page + ".html"

    url, admin, ist_id, name, auth = verify_user(name, ist_id, html_url)

    return render_template(url, name=name, ist_id=ist_id,
                           auth=auth, admin=admin, id=id)

#------------------------------------login URI----------------------------------------#

@app.route("/redirect_login")
def get_id():
    name = request.args.get("name", None)
    ist_id = request.args.get("id", None)

    request_data = {"user": ist_id}

    try:
        resp_stats = requests.post("http://127.0.0.1:5006/API/stats",
                                     json=json.dumps(request_data))   
        if resp_stats.status_code != 200:
            abort(500)
    except:
        flash("Error retrieving id")

    return redirect("/videos?ist_id=" + ist_id + "&name="+ name)

@app.route("/logout")
def logout():
    ist_id = request.args.get("ist_id", None)
    name = request.args.get("name", None)

    request_data = {"ist_id": ist_id}

    try:
        resp = requests.post("http://127.0.0.1:5004/logout", json=request_data)
    except:
        flash("User Manager service is down")

    return redirect("/index")

@app.route("/login")
def login():
    # see if app is running in the redirect port in a normal app we could use ping
    if check_port("5004") == 1:
        return redirect("http://127.0.0.1:5004/")
    else:
        flash("User Manager service is down")
        return redirect("/index")

#----------------------------------microservices--------------------------------------#

@app.route("/API/<microservice>/<path:path>", methods=['GET', 'POST', 'PUT'])
@app.route("/API/<microservice>/", methods=['GET', 'POST', 'PUT'])
def get_microservice(microservice, path=None):
    if microservice == "services":
        return {"services": listServicesDICT()}
    print(microservice)
    request_data = request.get_json()

    service_info = app.session.query(MicroServices).filter(
        MicroServices.name == microservice).first()

    url = service_info.endpoint
    if service_info is not None:
        if path is not None:
            url = url + path
            print(url)

        try:
            if request.method == 'GET':
                response = requests.get(url=url)
            elif request.method == 'POST':
                response = requests.post(url=url, json=request_data)
            elif request.method == 'PUT':
                response = requests.put(url=url, json=request_data)
        except:
            return "failure"

        if response.status_code != 200:
            abort(500)
    else:
        return "failure"

    return response.json()

@app.route("/microservice", methods=['POST', 'GET'])
def add_microservice():
    name = request.args.get("name", None)
    ist_id = request.args.get("ist_id", None)

    url = verify_user(name, ist_id, "services.html")

    form = ServiceForm()
    if form.validate_on_submit():

        service_info = app.session.query(MicroServices).filter(
            MicroServices.name == form.name.data).first()
        
        endpoint = "http://127.0.0.1:" + form.port.data + "/API/" + form.name.data + "/"

        if service_info is None:
            newService = MicroServices(name=form.name.data, endpoint=endpoint)

            app.session.add(newService)
            app.session.commit()
            app.session.close()

        return redirect("/videos?ist_id=" + ist_id + "&name="+ name)

    return render_template(url, form=form, title="New Microservice", ist_id=ist_id, name=name)
