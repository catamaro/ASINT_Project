from flask import Flask
from flask import abort, render_template, redirect, session, url_for, request
from Proxy import app

import requests

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/API/proxy_videos/", methods=['GET'])
def load_videos():
   response = requests.get("http://127.0.0.1:5002/API/videos/")
   return response.json() 

@app.route("/API/proxy_videos/<int:id>/", methods=['GET'])
def load_single_video(id):
   url = "http://127.0.0.1:5002/API/videos/" + str(id)
   response = requests.get(url=url)
   return response.json()

@app.route("/API/proxy_videos/<int:id>/views", methods=['PUT', 'PATCH'])
def add_view(id):
   url = "http://127.0.0.1:5002/API/videos/" + str(id) + "/views"
   response = requests.put(url=url)
   return response.json()
   
@app.route("/API/proxy_videos/", methods=['POST'])
def create_video():
   request_data = request.get_json()
   response = requests.post("http://127.0.0.1:5002/API/videos/", json=request_data)
   return response.json() 
   