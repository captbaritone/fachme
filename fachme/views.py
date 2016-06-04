from datetime import date
from flask import render_template
from fachme import app


@app.route('/')
def home():
    return render_template('index.html', year=date.today().year)
