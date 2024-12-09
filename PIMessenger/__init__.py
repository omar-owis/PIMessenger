from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TACK_MODIFCATIONS'] = False
db = SQLAlchemy(app)

from PIMessenger import views
from PIMessenger import models

#with app.app_context():
#    db.create_all()