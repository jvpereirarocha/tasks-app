from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import uuid


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, index=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='user')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_fullname(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __repr__(self):
        return "<User:{}>".format(self.email)


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date_task = db.Column(db.String(10), nullable=False)
    update_task_date = db.Column(db.DateTime(timezone=True), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

    def get_today_date(self):
        return datetime.datetime.now().strftime('%d/%m/%Y')

    def __init__(self, description, update_task_date, user_id, completed):
        self.description = description
        self.code = uuid.uuid4().hex
        self.date_task = self.get_today_date()
        self.update_task_date = update_task_date
        self.user_id = user_id
        self.completed = completed

    def __repr__(self):
        return "<Task:{}>".format(self.description)
