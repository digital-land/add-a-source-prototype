from flask import render_template, Blueprint


base = Blueprint("base", __name__)


# do we need this?
@base.context_processor
def set_globals():
    return {"staticPath": "https://digital-land.github.io"}


@base.route("/")
@base.route("/index")
def index():
    return render_template("index.html")
