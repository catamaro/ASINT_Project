from flask import Flask, request
#from sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

#db = SQLAlchemy(app)

from Logs import logs, routes