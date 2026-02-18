# views/page_views.py
# Handles all HTML page rendering routes.
# These routes just render templates — no business logic here.

from flask import Blueprint, render_template, request

pages = Blueprint("pages", __name__)


@pages.route("/")
def landing():
    return render_template("landing.html")


@pages.route("/homepage")
def homepage():
    return render_template("homepage.html")


@pages.route("/login")
def login():
    return render_template("login.html")


@pages.route("/about")
def about():
    return render_template("about.html")


@pages.route("/homepage/AddUsersToAccount")
def add_users():
    # Placeholder — will require auth before this is wired up properly
    return render_template("add_users.html")
