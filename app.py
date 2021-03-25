import json

import requests as python_request
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import FastAPI
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

config = Config(".env")
oauth = OAuth(config)

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid email profile https://www.googleapis.com/auth/cloud-platform"
    },
)


@app.route("/")
async def homepage(request: Request):
    user = request.session.get("user")
    if user:
        data = json.dumps(user)
        html = f"<pre>{data}</pre>" '<a href="/logout">logout</a>'
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@app.route("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route("/auth")
async def auth(request: Request):
    # El usuario se autentica con su cuenta de Google
    try:
        token = await oauth.google.authorize_access_token(request)
        for k, v in token.items():
            print(k.ljust(20), v)
    except OAuthError as error:
        return HTMLResponse(f"<h1>{error.error}</h1>")
    # Se valida que el usuario tenga permisos suficientes para consumir el API
    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    print(headers)
    payload = json.dumps({"permissions": ["iap.webServiceVersions.accessViaIAP"]})
    response = python_request.post(
        "https://iap.googleapis.com/v1/projects/875010993322/iap_web/appengine-frontend/services/frontend/versions/logintest:testIamPermissions",
        headers=headers,
        data=payload,
    )
    permissions = json.loads(response.text)
    if permissions:
        print(permissions)
        user = await oauth.google.parse_id_token(request, token)
        request.session["user"] = dict(user)
        return RedirectResponse(url="/")
    else:
        return HTMLResponse(f"<h1>Usuario no autenticado</h1><a href='/login'>login</a>")


@app.route("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")
