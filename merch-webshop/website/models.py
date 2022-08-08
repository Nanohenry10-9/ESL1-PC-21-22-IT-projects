from sqlalchemy.sql.functions import array_agg
from sqlalchemy.sql.sqltypes import ARRAY
from sqlalchemy.sql.type_api import INTEGERTYPE
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70))
    phone = db.Column(db.String(60))
    associated_students = db.Column(db.String(200))
    associated_carts = db.Column(JSON)
    session_id = db.Column(db.String(10), unique=True)


class Confirmed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70))
    phone = db.Column(db.String(60))
    associated_students = db.Column(db.String(200))
    associated_carts = db.Column(JSON)
    session_id = db.Column(db.String(10), unique=True)


