import datetime

from flask import url_for, redirect, request, jsonify

from app import app, db
from flask_login import current_user, login_user, logout_user

from app.models import User, Dish, Supply


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/check-login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.form['username']).first()
    if user is None or not user.check_password(request.form['password']):
        return redirect(url_for('/'))
    login_user(user)
    return jsonify({'flag':1})

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'flag':0})

@app.route('/room-check')
def room_check():
    pass

@app.route('/order-index')
def order_index():
    return jsonify(Dish.query.all.filter(Dish.begin_time <= datetime.datetime.now().time()).filter(datetime.datetime.now().time() < Dish.to_time))

@app.route('/supply-index')
def supply_index():
    return jsonify(Supply.query.all.filter(Supply.quantity > 0))

@app.route('/actual-order')
def actual_order():
    data = request.get_json()
    for order in data:
        pass

@app.route('/reserve')
def reserve():
    data = request.get_json()
    check_valid_reserve()
    pass

