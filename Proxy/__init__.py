from flask import Flask, request
#from sqlalchemy import SQLAlchemy
#from flask_bootstrap import Bootstrap

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

#db = SQLAlchemy(app)

#bootstrap = Bootstrap(app)

from Proxy import proxy, routes