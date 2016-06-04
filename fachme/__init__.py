from flask import Flask
from flask.ext.session import Session


app = Flask(__name__)
app.config.from_object('fachme.config.base')
app.config.from_envvar('FACHME_CONFIG')
app.config.from_object(__name__)
Session(app)

import fachme.api
import fachme.views
