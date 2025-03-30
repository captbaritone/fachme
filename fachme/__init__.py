from flask import Flask
from flask_session import Session
from db import db


app = Flask(__name__)
app.config.from_object('fachme.config.base')
app.config.from_envvar('FACHME_CONFIG')
app.config.from_object(__name__)
db.init_app(app)
Session(app)

import fachme.api
import fachme.views
