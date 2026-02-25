from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from rich.logging import RichHandler
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
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True),
        logging.FileHandler("app_log.log")
    ]
)

log = logging.getLogger("rich")
logging.getLogger('werkzeug').setLevel(logging.ERROR)
log.setLevel(logging.ERROR)

from routes import *  # Routes.py-დან იძახებს ყველაფერს

with app.app_context():  # ბაზის წასაკითხად
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
