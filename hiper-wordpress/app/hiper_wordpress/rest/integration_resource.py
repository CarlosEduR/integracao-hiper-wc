from flask import current_app, jsonify, request, Response
from app.hiper_wordpress.service import pedido_service, customer_service
from app.hiper_wordpress import bp
import json

@bp.route('/api/pedido', methods=['POST'])
def pedido_trigger():
    if 'x-wc-webhook-source' in request.headers:
        site = request.headers['x-wc-webhook-source']
        print("Site encontrado: {}".format(site))
        cliente = customer_service.get_customer_by_site(site)
        if cliente is not None:    
            pedido_service.enviar(request.json, cliente.__dict__['token_hiper'])
    return Response('Ok', status=202)
