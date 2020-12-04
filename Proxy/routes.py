from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for
from Videos import app

@app.route("/")
def index():
   return render_template("index.html")