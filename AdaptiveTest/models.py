from AdaptiveTest import db , login_manager
from flask_login import login_user , current_user , logout_user , login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask import redirect , url_for
from flask_admin.contrib.sqla import ModelView

@login_manager.user_loader
def load_user(user_id) :
    return User.query.get(int(user_id))

class User(db.Model , UserMixin) :

    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(40) , nullable = False , default = 'Unnamed')
    username = db.Column(db.String(20) , unique = True , nullable = False)
    gender = db.Column(db.String(10)  , nullable = False)
    password = db.Column(db.String(60) , nullable = False)
    no_of_test = db.Column(db.Integer , nullable = False , default = 0)
    results = db.relationship('Result' , backref='candidate' , lazy = True)

    def __repr__(self) :
        return f"User('{self.name}','{self.username}')"

class Result(db.Model) :
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(40) , nullable = False , default = 'Unnamed')
    username = db.Column(db.String(20) , unique = True , nullable = False)
    date_posted = db.Column(db.DateTime , nullable = False , default = datetime.utcnow())
    marks = db.Column(db.Integer , nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)

    def __repr__(self) :
        return f"User('{self.name}','{self.username}' , '{self.marks}' , '{self.date_posted}')"

class Question(db.Model) :
    id = db.Column(db.Integer , primary_key = True)
    subject = db.Column(db.String(30) , nullable = False)
    difficulty = db.Column(db.Integer , nullable = False)
    ques = db.Column(db.Text , nullable = False)
    option_1 = db.Column(db.String(100) , nullable = False)
    option_2 = db.Column(db.String(100) , nullable = False)
    option_3 = db.Column(db.String(100) , nullable = True)
    option_4 = db.Column(db.String(100) , nullable = True)
    correct = db.Column(db.Integer , nullable = False)

class MyModelView(ModelView) :
    
    def is_accessible(self) :
        
        return True