from flask import Flask
from flask import abort, render_template, redirect, session, url_for, request
from Proxy import app

import requests
import json

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/API/proxy_videos/", methods=['GET'])
def load_videos():
   # make REST request to video micro service
   response = requests.get("http://127.0.0.1:5002/API/videos/")

   # make REST request to logs micro service
   request_data = {"IP": "127.0.0.1", "endpoint": "/API/videos/"}
   requests.post("http://127.0.0.1:5003/API/logs/event", json=json.dumps(request_data))

   return response.json() 

@app.route("/API/proxy_videos/", methods=['POST'])
def create_video():
   # make REST request to video micro service
   request_data = request.get_json()
   response = requests.post("http://127.0.0.1:5002/API/videos/", json=request_data)

   # make REST request to logs micro service
   request2_data = {"data_type": "video", "content": request_data, "user": "me"}
   requests.post("http://127.0.0.1:5003/API/logs/data_creation", json=json.dumps(request2_data))
   return response.json() 

@app.route("/API/proxy_videos/<int:id>/", methods=['GET'])
def load_single_video(id):
   # make REST request to video micro service
   response = requests.get(url="http://127.0.0.1:5002/API/videos/" + str(id))

   # make REST request to logs micro service
   request_data = {"IP": "127.0.0.1", "endpoint": "/API/videos/<int:id>"}
   requests.post("http://127.0.0.1:5003/API/logs/event", json=json.dumps(request_data))

   return response.json()

@app.route("/API/proxy_videos/<int:id>/views", methods=['PUT', 'PATCH'])
def add_view(id):
   # make REST request to video micro service
   response = requests.put(url="http://127.0.0.1:5002/API/videos/" + str(id) + "/views")

   # make REST request to logs micro service
   request2_data = {"data_type": "view", "content": "request_data", "user": "me"}
   requests.post("http://127.0.0.1:5003/API/logs/data_creation", json=json.dumps(request2_data))

   return response.json()