from app.hiper_wordpress import bp
from flask_login import login_required, current_user
from app.hiper_wordpress.domain.User import User
from app.hiper_wordpress.service import auth_service as auth_service, customer_service as customer_service
from flask import render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

@bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('clientes.html', clientes=customer_service.get_customers())

@bp.route('/trocar-senha', methods=['GET'])
@login_required
def change_pass_page():
    return render_template('trocar-senha.html')
