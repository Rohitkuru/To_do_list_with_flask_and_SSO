from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(200))
    is_active = db.Column(db.Boolean)
    tasks = db.relationship('Todolist',backref='task_user')

class Todolist(db.Model):
    id = db.Column(db.Integer ,primary_key=True)
    task = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(50))
    label = db.Column(db.String(50))
    due_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    complete_date = db.Column(db.Date)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
