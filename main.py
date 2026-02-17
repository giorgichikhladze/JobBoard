from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import logging

app = Flask(__name__)

# Security
app.config['SECRET_KEY'] = '8f42a73b06471de2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialization
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ლოგირება
logging.basicConfig(
    filename='app_log.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

from routes import * # Routes.py-დან იძახებს ყველაფერს

with app.app_context(): # ბაზის წასაკითხად
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)