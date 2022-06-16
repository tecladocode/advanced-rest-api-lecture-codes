from flask_restful import Resource, url_for
from flask import url_for
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel
from oa import oauth
import json


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        redirect_uri = url_for("github.authorize", _external=True)
        return oauth.github.authorize_redirect(redirect_uri)


class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        token = oauth.github.authorize_access_token()
        if token is None:
            error_response = {
                "error": "Error getting token",
                "error_description": "Error getting token",
            }
            return error_response, 401

        resp = oauth.github.get("user")
        profile = json.loads(resp.text)
        username = profile["login"]
        user = UserModel.find_by_username(username)
        if not user:
            user = UserModel(username=username, password=None)
            user.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}, 200
