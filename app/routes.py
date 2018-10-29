from flask import url_for, redirect, request, jsonify

from app import app, db
from flask_login import current_user, login_user, logout_user

from app.models import User


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/check-login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.args['username']).first()
    if user is None or not user.check_password(request.args['password']):
        return redirect(url_for('/'))
    login_user(user)
    return jsonify({'flag':1})

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
