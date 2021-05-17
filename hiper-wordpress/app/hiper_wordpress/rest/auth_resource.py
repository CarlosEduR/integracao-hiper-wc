from app.hiper_wordpress import bp
from flask_login import login_user, logout_user, login_required
from app.hiper_wordpress.domain.User import User
from app.hiper_wordpress.service import user_service as user_service
from flask import render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import flask

@bp.route('/signup', methods=['POST'])
def signup_post():
    login = 'kleyber'
    password = '12345678'
    user = User.query.filter_by(login=login).first()
    if user is None:
        new_user = User(login=login, password=generate_password_hash(password, method='sha256'))
        user_service.create_user(new_user)

    return { 'status' : 'ok' }, 201

@bp.route('/login', methods = ['GET'])
def login():
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login_post():
    login =  request.form.get('login')
    password =  request.form.get('senha')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(login=login).first()
    if not user or not check_password_hash(user.password, password):
        flash('Usuário informado inexistente')
        return redirect(url_for('hiper_wordpress.login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('hiper_wordpress.index'))

@bp.route('/change-pass', methods=['POST'])
@login_required
def change_pass():
    new_pass =  request.form.get('nova-senha')
    print(new_pass)
    user_service.update_pass(new_pass)
    return redirect(url_for('hiper_wordpress.index'))

@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hiper_wordpress.index'))