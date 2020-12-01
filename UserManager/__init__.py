from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer import OAuth2ConsumerBlueprint

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

fenix_blueprint = OAuth2ConsumerBlueprint(
    "fenix-example", __name__,
    # this value should be retrived from the FENIX OAuth page
    client_id="1695915081466073",
    # this value should be retrived from the FENIX OAuth page
    client_secret="QRoQJy4t2uXFJgyV53X0P6ItK/5dXMXqbi9MS4C2n+Eas77cDvO8rjk5Pz3KezO9E6H2Ov1m/aHjqfUehQf9Mg==",
    # do not change next lines
    base_url="https://fenix.tecnico.ulisboa.pt/",
    token_url="https://fenix.tecnico.ulisboa.pt/oauth/access_token",
    authorization_url="https://fenix.tecnico.ulisboa.pt/oauth/userdialog",
)

app.register_blueprint(fenix_blueprint)

from UserManager import user_manager, routes