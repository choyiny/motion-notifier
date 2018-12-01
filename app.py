from flask import Flask, render_template
from . import config

# initialize app with config params
app = Flask(__name__)
app.config.from_object(config)


@app.route("/")
def index():
    """ Server index """
    return render_template("index.html")
