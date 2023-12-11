import os
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

from src.views.home import home
from src.views.auth import auth
from src.views.bookmarks import bookmarks
from config import config

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY=config.SECRET_KEY,
    JWT_SECRET_KEY=config.JWT_SECRET_KEY,
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
)

jwt = JWTManager(app)

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(bookmarks)
