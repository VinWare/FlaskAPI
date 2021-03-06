from flask_login import UserMixin
from marshmallow import fields
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, loginManager, ma


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

class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(31))
    location = db.Column(db.String(127))
    num_of_floors = db.Column(db.Integer)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    floor_num = db.Column(db.Integer)
    type = db.Column(db.String(31))
    num_ppl = db.Column(db.Integer)
    default_price = db.Column(db.Integer)
    occupied = db.Column(db.Boolean)
    prices = db.relationship('RoomPrice', backref='room', lazy='dynamic')
    res = db.relationship('RoomRes', backref='room', lazy='dynamic')
    supply_orders = db.relationship('SupplyOrder', backref='room', lazy='dynamic')

class RoomPrice(db.Model):
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    price = db.Column(db.Integer)

class Reservation(db.Model):
    res_id = db.Column(db.Integer, primary_key=True)
    cust_name = db.Column(db.String(63))
    payment_method = db.Column(db.String(31))
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    room_res = db.relationship('RoomRes', backref='res', lazy='dynamic')

class RoomRes(db.Model):
    res_id = db.Column(db.Integer, db.ForeignKey('reservation.res_id'), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
    status = db.Column(db.String(15))

class Supply(db.Model):
    supply_id = db.Column(db.Integer, primary_key=True)
    supply_name = db.Column(db.String(127))
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Integer)
    supply_parts = db.relationship('SupplyPart', backref='supply', lazy='dynamic')

class SupplyOrder(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    supply_parts = db.relationship('SupplyPart', backref='order', lazy='dynamic')

class SupplyPart(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('supply_order.order_id'), primary_key=True)
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.supply_id'), primary_key=True)
    quantity = db.Column(db.Integer)

class Employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(127))
    emp_pos = db.Column(db.String(63))
    emp_addr = db.Column(db.String(255))
    emp_phone = db.Column(db.String(15))
    emp_email = db.Column(db.String(255))

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class EmployeeSchema(ma.ModelSchema):
    class Meta:
        model = Employee

class OrderDish(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('restaurant_order.order_id'), primary_key=True)
    dish_name = db.Column(db.String(127), db.ForeignKey('dish.dish_name'), primary_key=True)
    quantity = db.Column(db.Integer)

class Dish(db.Model):
    dish_name = db.Column(db.String(127), primary_key=True)
    dish_cost = db.Column(db.Integer)
    from_time = db.Column(db.Time)
    to_time = db.Column(db.Time)
    type = db.Column(db.String(15))
    orders = db.relationship('OrderDish', backref='Dish', lazy='dynamic')

class RestaurantOrder(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer)
    order_time = db.Column(db.Time)
    orders = db.relationship('OrderDish', backref='orderdet', lazy='dynamic')

class RestaurantOrderSchema(ma.ModelSchema):
    class Meta:
        model = RestaurantOrder

class DishSchema(ma.ModelSchema):
    class Meta:
        model = Dish

class OrderDishSchema(ma.ModelSchema):
    class Meta:
        model = OrderDish
        fields = ('order_id', 'quantity', 'nested')
        nested = ma.Nested(DishSchema)

class BuildingSchema(ma.ModelSchema):
    class Meta:
        model = Building

class RoomSchema(ma.ModelSchema):
    class Meta:
        model = Room

class RoomPriceSchema(ma.ModelSchema):
    class Meta:
        model = RoomPrice

class SupplySchema(ma.ModelSchema):
    class Meta:
        model = Supply

class SupplyOrderSchema(ma.ModelSchema):
    class Meta:
        model = SupplyOrder

class SupplyPartSchema(ma.ModelSchema):
    class Meta:
        model = SupplyPart

@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))