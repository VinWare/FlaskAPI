import datetime

from flask import url_for, redirect, request, jsonify

from app import app, db
from flask_login import current_user, login_user, logout_user

from app.models import User, Dish, Supply, Room, Employee, RestaurantOrder


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/check-login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'flag':1})
    data = request.json
    user = User.query.filter_by(username=data.get('username').first())
    if user is None or not user.check_password(data.get('password')):
        return jsonify({'flag':0})
    login_user(user)
    return jsonify({'flag':1})

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'flag':0})

@app.route('/room-check')
def room_check():
    data = request.json()
    if(data['room'] is not 'None'):
        return jsonify(Room.query.all.filter())
    pass

@app.route('/order-index')
def order_index():
    return jsonify(Dish.query.all.filter(Dish.begin_time <= datetime.datetime.now().time()).filter(datetime.datetime.now().time() < Dish.to_time))

@app.route('/supply-index')
def supply_index():
    return jsonify(Supply.query.all.filter(Supply.quantity > 0))

@app.route('/actual-order')
def actual_order():
    pass
    # data = request.get_json()
    # restaurant = RestaurantOrder(order_id=data['order_id'], room_id=data['room_id'], order_time=datetime.datetime.now().time())
    # db.session.add(restaurant)
    # for order in data['orders']:
    #     orderDish = OrderDish(order_id=data['order_id'], dish_id=order['dish_id'], quantity=order['quantity'])
    #     db.session.add(orderDish)
    # db.commit()
    # return jsonify({"Result":"OK"})

@app.route('/reserve')
def reserve():
    data = request.get_json()
    pass

@app.route('/emp-details')
def emp_details():
    if current_user.is_anonymous:
        return jsonify({'flag':0})
    return jsonify(Employee.query.all())
