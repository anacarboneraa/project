import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if user:
        return User(user[0]["id"])
    return None


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_USE_SIGNER"] = True
app.config["SECRET_KEY"] = os.urandom(24)
Session(app)

db = SQL("sqlite:///health.db")

def login_required(f):
    # https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    print("Session Data:", session)
    if "user_id" in session:
        return redirect("/log_health")
    else:
        return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if not request.form.get("username"):
            flash("must provide username", "danger")

        elif not request.form.get("password"):
            flash("must provide password", "danger")

        elif request.form.get("password") != request.form.get("confirmation"):
            flash("passwords must be the same", "danger")

        rows = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )

        if len(rows) != 0:
            flash("username already taken", "danger")

        hashed_password = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", request.form.get("username"), hashed_password)

        flash("You are registered!", "success")
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("must provide username", "danger")

        elif not password:
            flash("must provide password", "danger")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            flash("invalid username and/or password", "danger")
            return redirect("/login")

        user = User(rows[0]["id"])
        login_user(user)

        session["user_id"] = rows[0]["id"]
        print("user logged in, session:", session)

        return redirect("/log_health")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect("/login")


@app.route("/log_health", methods=["GET", "POST"])
@login_required
def log_health():
    if request.method == "POST":
        workout = request.form.get("workout")
        healthy_meals = request.form.get("healthy_meals")
        total_meals = request.form.get("total_meals")
        water_intake = request.form.get("water_intake")

        if not healthy_meals or not total_meals or int(total_meals) == 0:
            flash("muts provide meal numbers", "danger")
            return redirect("/log_health")

        db.execute(
            "INSERT INTO health_logs (user_id, workout, healthy_meals, total_meals, water_intake) VALUES (?, ?, ?, ?, ?)",
            session["user_id"], workout, healthy_meals, total_meals, water_intake
        )

        flash("data logged successfully!", "success")
        return redirect("/log_health")

    print("Session User ID:", session.get("user_id"))
    return render_template('log_health.html')


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
