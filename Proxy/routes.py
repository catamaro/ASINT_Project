from flask import Flask
from flask import abort, render_template, redirect, session, url_for, request, flash
from Proxy import app
from flask_login import current_user, login_user, login_required, logout_user
from flask_login import UserMixin
from Proxy.proxy import check_port

import requests
import json

#----------------------------------logs--------------------------------------#

# logs handler
@app.before_request
def before_req():
    if(request.method == 'GET'):
        url = request.url.split('//')
        url = url[1].split(':')
        endpoint = url[1].split('/', 1)[1]
        IP = url[0]

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
            data_type = "unknown"

        user = request.json.get("user")

        # make REST request to logs micro service
        data = {"data_type": data_type, "content": request.json, "user": user}
        try:
            requests.post(
                "http://127.0.0.1:5003/API/logs/data_creation", json=json.dumps(data))
        except:
            flash("Logs service is down")

    elif(request.method == 'PUT' or request.method == 'PATCH'):
        url = request.url.split('/')
        content = url[5]
        if request.url.find("view") != -1:
            data_type = "view"

        # make REST request to logs micro service
        data = {"data_type": data_type, "content": content, "user": "me"}
        try:
            requests.post(
                "http://127.0.0.1:5003/API/logs/data_creation", json=json.dumps(data))
        except:
            flash("Logs service is down")

#----------------------------------proxy--------------------------------------#


@app.route("/")
def index():
    name = request.args.get("name", None)
    ist_id = request.args.get("ist_id", None)

    if ist_id is not None: auth = True
    else: auth = None

    admin = None

    if ist_id is not None:
        try:
            response = requests.get("http://127.0.0.1:5004/API/user/"+ist_id)
            print(response.status_code)
            if response.status_code != 200:
                abort(500)

            print(response.json())
            
            if response.json().get("admin") == 1: admin = True
        except:
            flash("Error retrieving data")


    return render_template("index.html", name=name, ist_id=ist_id,
                           auth=auth, admin=admin)

# admin page
@app.route("/logs")
def logs():
    name = request.args.get("name", None)
    ist_id = request.args.get("ist_id", None)

    return render_template("logs.html", ist_id=ist_id, name=name)
# admin page
@app.route("/stats")
def stats():
    name = request.args.get("name", None)
    ist_id = request.args.get("ist_id", None)

    return render_template("statistics.html", ist_id=ist_id, name=name)

#----------------------------------user--------------------------------------#


@app.route("/redirect_login")
def get_id():
    name = request.args.get("name", None)
    ist_id = request.args.get("id", None)

    response = requests.get("http://127.0.0.1:5004/API/user/"+ist_id)
    if response.status_code != 200:
        abort(500)

    return redirect(url_for("index", name=name, ist_id=ist_id))

@app.route("/logout")
def logout():
    ist_id = request.args.get("ist_id", None)
    name = request.args.get("name", None)

    request_data = {"ist_id": ist_id}

    try:
        resp = requests.post("http://127.0.0.1:5004/logout", json=request_data)
    except:
        flash("User Manager service is down")

    return redirect(url_for("index"))


@app.route("/login")
def login():
    if check_port("5004") == 1: return redirect("http://127.0.0.1:5004/login")
    else:
        flash("User Manager service is down")
        return redirect(url_for("index"))


#----------------------------------videos--------------------------------------#


@app.route("/API/proxy_videos/", methods=['GET'])
def load_videos():
    # make REST request to video micro service
    try:
        response=requests.get("http://127.0.0.1:5002/API/videos/")
        if response.status_code != 200:
            abort(500)
    except:
        return "failure"

    return response.json()


@app.route("/API/proxy_videos/", methods=['POST'])
def create_video():
    # make REST request to video micro service
    request_data=request.get_json()
    try:
        response=requests.post(
            "http://127.0.0.1:5002/API/videos/", json=request_data)
        if response.status_code != 200:
            abort(500)
    except:
        return "failure"

    return response.json()


@app.route("/API/proxy_videos/<int:id>/", methods=['GET'])
def load_single_video(id):
    # make REST request to video micro service
    try:
        response=requests.get(
            url="http://127.0.0.1:5002/API/videos/" + str(id)+"/")
        if response.status_code != 200:
            abort(500)
    except:
        return "failure"

    return response.json()


@app.route("/API/proxy_videos/<int:id>/views", methods=['PUT', 'PATCH'])
def add_view(id):
    # make REST request to video micro service
    try:
        response=requests.put(
            url="http://127.0.0.1:5002/API/videos/" + str(id) + "/views")
        if response.status_code != 200:
            abort(500)
    except:
        return "failure"

    return response.json()

#----------------------------------qa--------------------------------------#


@app.route("/API/proxy_question/<int:id>/", methods=['POST'])
def create_question(id):
    # make REST request to video micro service
    request_data=request.get_json()
    try:
        response=requests.post(
            "http://127.0.0.1:5001/API/question/"+str(id)+"/", json=request_data)
        if response.status_code != 200:
            abort(500)
    except:
        return "failure"

    return response.json()


@app.route("/API/proxy_question/", methods=['GET'])
def load_questions():
    # make REST request to video micro service
    try:
        response=requests.get("http://127.0.0.1:5001/API/question/")
        if response.status_code != 200:
            abort(500)
    except:
        return "failure"
    return response.json()


@app.route("/API/proxy_answer/<int:id>/", methods=['POST'])
def create_answer(id):
    # make REST request to video micro service
    request_data=request.get_json()
    try:
        response=requests.post(
            "http://127.0.0.1:5001/API/answer/"+str(id)+"/", json=request_data)
        if response.status_code != 200:
            abort(500)
    except:
        return "failure"
    return response.json()


@app.route("/API/proxy_answer/<int:id>/", methods=['GET'])
def load_answers(id):
    # make REST request to video micro service
    try:
        response=requests.get(
            "http://127.0.0.1:5001/API/answer/"+str(id)+"/")
        if response.status_code != 200:
            abort(500)
    except:
        return "failure"
    return response.json()

@app.route("/QA/<int:id>/<ist_id>/<name>")
def qa_endpoint(id, ist_id, name):
    return render_template("qa.html", id=id, ist_id=ist_id, name=name)

