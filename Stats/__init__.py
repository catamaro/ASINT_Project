from flask import Flask, request

from config import Config

app = Flask(__name__)
app.config.from_object(Config)


from Stats import stats, routes, models, database