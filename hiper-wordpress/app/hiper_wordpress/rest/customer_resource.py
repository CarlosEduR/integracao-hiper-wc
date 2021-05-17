from flask import current_app, jsonify, request, Response, redirect, url_for
from flask_login import login_required
from app.hiper_wordpress import bp
from app.hiper_wordpress.service import customer_service as customer_service
from app.hiper_wordpress.domain.Customer import Customer

@bp.route('/api/adicionar-cliente', methods=['POST'])
@login_required
def adicionar_cliente():
    site = request.form.get('site')
    if site.endswith('/') == False:
        site += '/'
    customer = Customer.query.filter_by(site=site).first()
    if customer is None:
        customer = Customer(site=site, consumer_key=request.form.get('consumer_key'), consumer_secret=request.form.get('consumer_secret'), token_hiper=request.form.get('token_hiper'))
        customer_service.create_customer(customer)
    return redirect(url_for('hiper_wordpress.index'))

@bp.route('/api/remover-cliente/<id_customer>', methods=['POST'])
@login_required
def excluir_cliente(id_customer):
    customer = Customer.query.filter_by(id_customer=id_customer).first()
    if customer is not None:
        customer_service.delete_customer(customer)
    return redirect(url_for('hiper_wordpress.index'))
    
@bp.route('/api/atualizar-cliente/<id_customer>', methods=['POST'])
@login_required
def atualizar_cliente(id_customer):
    customer = Customer.query.filter_by(id_customer=id_customer).first()
    if customer is not None:
        customer = Customer(site=request.form.get('site'), consumer_key=request.form.get('consumer_key'), consumer_secret=request.form.get('consumer_secret'), token_hiper=request.form.get('token_hiper'))
        customer_service.update_customer(customer, id_customer)
    return redirect(url_for('hiper_wordpress.index'))
    