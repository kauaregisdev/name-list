from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'DATABASE_URL',
    'postgresql://admin:admin123@localhost:5000/name_list'
)
db = SQLAlchemy(app)

from scripts.models import Name

with app.app_context():
    db.create_all()

from scripts.views import *

if __name__ == '__main__':
    app.run(debug=True)