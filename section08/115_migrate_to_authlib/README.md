# Migrating from Flask-OAuthlib to Authlib

This course uses Flask-OAuthlib, but this is now deprecated. Instead, the [Flask-OAuthlib documentation](https://flask-oauthlib.readthedocs.io/en/latest/) suggests using another similar library, [Authlib](https://github.com/lepture/authlib), instead.

Fortunately, migrating between Flask-OAuthlib and Authlib is very easy.

A strong thanks to Theron Kousek for his [written guide](https://tbsoftware.wordpress.com/2020/04/23/advanced-rest-python-flask-oauth-change/) and [video](https://www.youtube.com/watch?v=3-dH-hxk658) with the migration.

Below are the changes needed to migrate between Flask-OAuthlib and Authlib.

## Change your requirements and install

If using `requirements.txt`, delete `Flask-OAuthlib` and add `authlib` instead:

```diff
-flask-oauthlib
+authlib
```

Then, uninstall Flask-OAuthlib and install from the requirements file:

```
pip uninstall flask-oauthlib
pip install -r requirements.txt
```

## Changes to the OAuth client

This is the new `oa.py`:

```python
import os
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

oauth.register(
    name="github",
    client_id=os.getenv("GITHUB_CONSUMER_KEY", default=None),
    client_secret=os.getenv("GITHUB_CONSUMER_SECRET", default=None),
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)
```

A couple things to note:

- Authlib comes with a Flask client, which means we don't need to define a `tokengetter` or use the `g` object ourselves.
- The imports have changed.

## Changes to the GitHubLogin Resource

This is the new `resources/github_login.py`:

```python
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
```

The main changes are to do with how the `oauth` variable is used, such as:

- `oauth.github.authorize_redirect(redirect_uri)`
- `token = oauth.github.authorize_access_token()`
- `oauth.github.get("user")`

But other than that, changes are minimal.