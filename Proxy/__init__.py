from flask import Flask, request
from flask_bootstrap import Bootstrap

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

from Proxy import proxy, routes