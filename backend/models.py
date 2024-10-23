
from . import db # importujemy db z pliku __init__.py z obecnego pakietu
from flask_login import UserMixin # dziedziczymy po UserMixin, żeby móc używać metod związanych z logowaniem
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)# primary key to unikalny identyfikator użytowany do identyfikacji rekordu w bazie danych
    username = db.Column(db.String(100), unique=True)# unique=True oznacza, że wartość w tej kolumnie musi być unikalna
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    time_records = db.relationship('Time_record')# relacja między tabelami

class Time_record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    start_time = db.Column(db.DateTime(timezone=True))# 
    end_time = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))# ForeignKey to relacja między dwoma tabelami
    user = db.relationship('User')# relacja między tabelami, User to nazwa klasy User