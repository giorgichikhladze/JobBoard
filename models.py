from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
from main import db, login_manager


def get_georgian_time():
    return datetime.utcnow() + timedelta(hours=4)


@login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    jobs = db.relationship('Job', backref='author', lazy=True)
    image_file = db.Column(db.String(200), nullable=False,
                           default='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1280px-Python-logo-notext.svg.png')


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String, nullable=False)  # Integer შევცვალე სტრინგით
    location = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=get_georgian_time)

    def __repr__(self):
        return f"Job('{self.title}', '{self.date_posted}')"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
