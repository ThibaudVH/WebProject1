from flask import Flask, render_template, g, redirect, url_for
from flask_oidc import OpenIDConnect
from okta import UsersClient


# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)
app.debug = True
app.config["OIDC_CLIENT_SECRETS"] = "exclude/client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
#allows you to test out user login and registration in development without using SSL. If you were going to run your site publicly, you would remove this option and use SSL on your site.
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "aa"
oidc = OpenIDConnect(app)
oidc.init_app(app)

okta_client = UsersClient("https://dev-711513.oktapreview.com", "00-96K0PI5EgQUBFwFDwoBn9JObfyu4p6wfmFdlxjO")


@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None

# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route("/")
@oidc.require_login
def index():
    return render_template("index.html")


@app.route("/dashboard")
@oidc.require_login
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))


@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".index"))

if __name__ == '__main__':
    # Run the app server on localhost:8080
    app.run('localhost', 8080)

