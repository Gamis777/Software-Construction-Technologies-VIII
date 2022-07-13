import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask("Google Login App")  
app.secret_key = "GeekyHuman.com" # es necesario establecer una contraseña --> OAuth 2.0
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  #esto es para configurar nuestro entorno en https porque OAuth 2.0 solo admite entornos https

GOOGLE_CLIENT_ID = "745717042243-o6n5khbc7hks7i6b2gse5ndft4kb9508.apps.googleusercontent.com"  #ingrese su ID de cliente que obtuvo de la consola de Google
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")  # establezca la ruta a donde está el archivo .json que obtuvo en la consola de Google

flow = Flow.from_client_secrets_file(  #Flow es OAuth 2.0 una clase que almacena toda la información de cómo queremos autorizar a nuestros usuarios
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #aqui estamos especificando que obtenemos despues de la autorizacion
    redirect_uri="http://127.0.0.1:5000/callback"  # el URI de redireccionamiento es el punto donde el usuario terminará después de la autorización
)

def login_is_required(function):  #f. para verificar si el usuario está autorizado o no
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  #  Autorización requerida
            return abort(401)
        else:
            return function()

    return wrapper


@app.route("/login")  ##la página donde el usuario puede iniciar sesión
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")  #autorizacion
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")  #define los resultados para mostrar en la página
    session["name"] = id_info.get("name")
    return redirect("/protected_area")  #pagina final


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"


if __name__ == "__main__":
    app.run(debug=True)