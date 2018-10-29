from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db,loginManager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = password
        # self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return (self.password_hash == password)
        # return check_password_hash(self.password_hash, password)

# class Building(db.Model):
#     name = db.Column(db.String(31))
#     location = db.Column(db.String(127))
#     num_of_floors = db.Column(db.Integer)
#
# class Room(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     num = db.Column(db.Integer)
#     floor_num = db.Column(db.Integer)
#     type = db.Column(db.String(31))
#     num_ppl = db.Column(db.Integer)
#     default_price = db.Column(db.Integer)
#     occupied = db.Column(db.Boolean)
#     prices = db.relationship('RoomPrice', backref='room', lazy='dynamic')
#     res = db.relationship('RoomRes', backref='room', lazy='dynamic')
#
# class RoomPrice(db.Model):
#     room_id = db.Column(db.Integer, db.ForeignKey('Room.id'))
#     date = db.Column(db.Date)
#     price = db.Column(db.Integer)
#
# class Reservation(db.Model):
#     res_id = db.Column(db.Integer, primary_key=True)
#     cust_name = db.Column(db.String(63))
#     payment_method = db.Column(db.String(31))
#     from_date = db.Column(db.Date)
#     to_date = db.Column(db.Date)
#     room_res = db.relationship('RoomRes', backref='res', lazy='dynamic')
#
# class RoomRes(db.Model):
#     res_id = db.Column(db.Integer, db.ForeignKey('Reservation.res_id'))
#     room_id = db.Column(db.Integer, db.ForeignKey('Room.id'))
#     status = db.Column(db.String(15))

@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))