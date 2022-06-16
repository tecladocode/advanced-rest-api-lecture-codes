from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv

load_dotenv(".env")

from db import db
from ma import ma
from oa import oauth
from resources.user import UserRegister, UserLogin, User, SetPassword
from resources.github_login import GithubLogin, GithubAuthorize


app = Flask(__name__)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(GithubLogin, "/login/github")
api.add_resource(GithubAuthorize, "/login/github/authorized", endpoint="github.authorize")
api.add_resource(SetPassword, "/user/password")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)
    app.run(port=5000)
