from flask import Flask
from flask_cas import CAS
from flask_sqlalchemy import SQLAlchemy
from teambuildingapp import config
app = Flask(__name__)
CAS(app, '/cas') # this adds the prefix '/api/cas/' to the /login and /logout
                 # routes that CAS provides
db = SQLAlchemy(app)

app.config.from_pyfile('config.py')

import teambuildingapp.views