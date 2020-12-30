from flask import Flask
from flask import abort, render_template, redirect, session, url_for, request, flash
from Proxy import app
from flask_login import current_user, login_user, login_required, logout_user
from flask_login import UserMixin

import requests
import json


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

        # make REST request to logs micro service
        data = {"data_type": data_type, "content": request.json, "user": "me"}
        requests.post(
            "http://127.0.0.1:5003/API/logs/data_creation", json=json.dumps(data))

    elif(request.method == 'PUT' or request.method == 'PATCH'):
        url = request.url.split('/')
        content = url[5]
        if request.url.find("view") != -1:
            data_type = "view"

        # make REST request to logs micro service
        data = {"data_type": data_type, "content": content, "user": "me"}
        requests.post(
            "http://127.0.0.1:5003/API/logs/data_creation", json=json.dumps(data))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/redirect_login")
def get_id():
    name = request.args.get("name", None)
    ist_id = request.args.get("id", None)

    response = requests.get("http://127.0.0.1:5004/API/user/"+ist_id)
    if response.status_code != 200:
        abort(500) 

    is_authenticated = response.json().get("auth")

    return render_template("index.html", name=name, ist_id=ist_id,
                                is_authenticated=is_authenticated)

@app.route("/logout")
def logout():
    ist_id = request.args.get("ist_id", None)
    name = request.args.get("name", None)

    request_data = {"ist_id": ist_id}

    resp = requests.post("http://127.0.0.1:5004/logout", json=request_data)

    return render_template("index.html", name=name, ist_id=ist_id,
                                is_authenticated=resp.json()["auth"])



@app.route("/login")
def login():
    return redirect("http://127.0.0.1:5004/login")


@app.route("/QA/<int:id>/<ist_id>")
def qa_endpoint(id, ist_id):
    return render_template("qa.html", id=id, ist_id=ist_id)


@app.route("/API/proxy_videos/", methods=['GET'])
def load_videos():
    # make REST request to video micro service
    response = requests.get("http://127.0.0.1:5002/API/videos/")
    if response.status_code != 200:
        abort(500)
    return response.json()


@app.route("/API/proxy_videos/", methods=['POST'])
def create_video():
    # make REST request to video micro service
    request_data = request.get_json()
    response = requests.post(
        "http://127.0.0.1:5002/API/videos/", json=request_data)
    if response.status_code != 200:
        abort(500)

    return response.json()


@app.route("/API/proxy_videos/<int:id>/", methods=['GET'])
def load_single_video(id):
    # make REST request to video micro service
    response = requests.get(
        url="http://127.0.0.1:5002/API/videos/" + str(id)+"/")
    if response.status_code != 200:
        abort(500)
    return response.json()


@app.route("/API/proxy_videos/<int:id>/views", methods=['PUT', 'PATCH'])
def add_view(id):
    # make REST request to video micro service
    response = requests.put(
        url="http://127.0.0.1:5002/API/videos/" + str(id) + "/views")
    if response.status_code != 200:
        abort(500)
    return response.json()

#----------------------------------qa--------------------------------------#


@app.route("/API/proxy_question/<int:id>/", methods=['POST'])
def create_question(id):
    # make REST request to video micro service
    request_data = request.get_json()
    response = requests.post(
        "http://127.0.0.1:5001/API/question/"+str(id)+"/", json=request_data)
    if response.status_code != 200:
        abort(500)
    return response.json()


@app.route("/API/proxy_question/", methods=['GET'])
def load_questions():
    # make REST request to video micro service
    response = requests.get("http://127.0.0.1:5001/API/question/")
    if response.status_code != 200:
        abort(500)
    return response.json()


@app.route("/API/proxy_answer/<int:id>/", methods=['POST'])
def create_answer(id):
    # make REST request to video micro service
    request_data = request.get_json()
    response = requests.post(
        "http://127.0.0.1:5001/API/answer/"+str(id)+"/", json=request_data)
    if response.status_code != 200:
        abort(500)

    return response.json()


@app.route("/API/proxy_answer/<int:id>/", methods=['GET'])
def load_answers(id):
    # make REST request to video micro service
    response = requests.get("http://127.0.0.1:5001/API/answer/"+str(id)+"/")
    if response.status_code != 200:
        abort(500)
    return response.json()
