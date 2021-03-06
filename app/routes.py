import datetime

from flask import url_for, redirect, request, jsonify
import json

from app import app, db
from flask_login import current_user, login_user, logout_user

from app.models import *


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/check-login', methods=['POST'])
def login():
    if request == None:
        return jsonify({'value':'nonetyperequest'})
    if current_user.is_authenticated:
        return jsonify({'flag':1})
    data = json.loads(request.data)
    user = User.query.filter(User.username==data['username']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'flag':0})
    login_user(user)
    return jsonify({'flag':1})

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'flag':0})

@app.route('/room-check', methods=['GET', 'POST'])
def room_check():
    json_data = json.loads(request.data)
    from_date_day = json_data['fromDateDay']
    from_date_month = json_data['fromDateMonth']
    from_date_year = json_data['fromDateYear']
    from_date = datetime.datetime.strptime(from_date_day + '/' + from_date_month + '/' + from_date_year, '%d/%m/%Y')
    to_date_day = json_data['toDateDay']
    to_date_month = json_data['toDateMonth']
    to_date_year = json_data['toDateYear']
    to_date = datetime.datetime.strptime(to_date_day + '/' + to_date_month + '/' + to_date_year, '%d/%m/%Y')
    room_type = json_data['type']
    print(from_date)
    print(to_date)
    # type = request.form['type']
    # abcd = "SELECT room.type, room.room_num, building.build_name, room.num_ppl, room.default_price FROM room NATURAL JOIN building WHERE NOT EXISTS(SELECT * FROM room_res NATURAL JOIN reservation WHERE room_id = room.room_id AND  to_date >= from_date AND from_date <= to_date )"_
    act_result_query = db.session.query(Room).join(Building).filter(~db.session.query(Reservation).join(RoomRes).filter(RoomRes.room_id==Room.id, Reservation.to_date >= from_date, Reservation.from_date < to_date).exists()).filter(Room.type==room_type)
    act_result = act_result_query.all()
    print(act_result_query)
    print(act_result)
    print(type(act_result))
    roomSchema = RoomSchema(many=True)
    output = roomSchema.dump(act_result).data
    return jsonify(output)
    # return jsonify({'hey' : 'there'})

@app.route('/reserve-room', methods=['GET', 'POST'])
def reserve_room():
    # data = json.loads(request.data)
    r = Reservation(cust_name="Hello", payment_method="CC", from_date=datetime.datetime.now().date(), to_date=datetime.datetime.now().date() + datetime.timedelta(days=2))
    db.session.add(r)
    db.session.flush()
    print(r.res_id)
    for i in range(2):
        res = RoomRes(res_id=r.res_id, room_id=i)
        db.session.add(res)
        db.session.flush()
    db.session.commit()
    return jsonify({})

@app.route('/order-index')
def order_index():
    data = RestaurantOrder.query.all()
    print(type(data))
    for datum in data:
        for order in datum.orders:
            print(order)
    # data = OrderDish.query.all()
    # orderDishSchema = OrderDishSchema(many=True)
    # output = orderDishSchema.dump(data).data
    restaurantOrderSchema = RestaurantOrderSchema(many=True)
    output = restaurantOrderSchema.dump(data).data
    return jsonify(output)
    # return jsonify(Dish.query.all.filter(Dish.begin_time <= datetime.datetime.now().time()).filter(datetime.datetime.now().time() < Dish.to_time))

@app.route('/supply-index', methods=['GET', 'POST'])
def supply_index():
    data = SupplyOrder.query.all()
    print(type(data))
    # data = OrderDish.query.all()
    # orderDishSchema = OrderDishSchema(many=True)
    # output = orderDishSchema.dump(data).data
    supplyOrderSchema = SupplyOrderSchema(many=True)
    output = supplyOrderSchema.dump(data).data
    return jsonify(output)

@app.route('/supplies', methods=['GET', 'POST'])
def supply():
    data = Supply.query.all()
    supplySchema = SupplySchema(many=True)
    output = supplySchema.dump(data).data
    return jsonify(output)

@app.route('/actual-order', methods=['POST'])
def actual_order():
    pass
    restaurant = RestaurantOrder(room_id=request.form['room_id'], order_time=datetime.datetime.now().time())
    db.session.add(restaurant)
    for order in request.form['orders']:
        orderDish = OrderDish(order_id=request.form['order_id'], dish_id=order['dish_id'], quantity=order['quantity'])
        db.session.add(orderDish)
    db.commit()
    return jsonify({"Result":"OK"})

@app.route('/supply-order', methods=['POST'])
def supply_order():
    pass
    supply = SupplyOrder(room_id=request.form['room_id'])
    db.session.add(supply)
    for order in request.form['orders']:
        orderPart = SupplyPart(order_id=request.form['order_id'], supply_id=order['supply_id'], quantity=order['quantity'])
        db.session.add(orderPart)
    db.commit()
    return jsonify({"Result":"OK"})

@app.route('/emp-details', methods=['GET', 'POST'])
def emp_details():
    # if current_user.is_anonymous:
    #     return jsonify({'flag':0})
    emp_data = Employee.query.all()
    employeeSchema = EmployeeSchema(many=True)
    output = employeeSchema.dump(emp_data).data
    return jsonify(output)
