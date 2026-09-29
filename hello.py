from datetime import datetime, timezone

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        name='Christina',
        current_time=datetime.now(timezone.utc),
    )

@app.route('/user/<name>')
def user(name):
    return render_template(
        'index.html',
        name=name,
        current_time=datetime.now(timezone.utc),
    )

bootstrap = Bootstrap(app)
moment = Moment(app)
