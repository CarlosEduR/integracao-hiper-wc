import requests, json

def enviar(pedido_data, token_hiper):
    print('Recebendo solicitação de pedido, realizando envio')
    print(pedido_data)
    pedido_hiper = {}
    pedido_hiper['cliente'] = {}
    pedido_hiper['enderecoDeCobranca'] = {}
    pedido_hiper['enderecoDeEntrega'] = {}
    pedido_hiper['itens'] = {}



    pedido_hiper['cliente']['nomeDoCliente'] = formatar_nome_cliente(pedido_data)
    pedido_hiper['cliente']['email'] = pedido_data['billing']['email']
    pedido_hiper['cliente']['inscricaoEstadual'] = ''
    pedido_hiper['cliente']['nomeFantasia'] = ''
    
    pedido_hiper['enderecoDeCobranca']['cep'] = (pedido_data['shipping']['postcode']).replace('-', '') if pedido_data['shipping']['postcode'] else (pedido_data['billing']['postcode']).replace('-', '') 
    pedido_hiper['enderecoDeCobranca']['logradouro'] = pedido_data['shipping']['address_1'] if pedido_data['shipping']['address_1'] else pedido_data['billing']['address_1']   
    pedido_hiper['enderecoDeCobranca']['codigoIbge'] = buscar_codigo_ibge(pedido_data, 'shipping') if pedido_data['shipping']['city'] else buscar_codigo_ibge(pedido_data, 'billing')
    pedido_hiper['enderecoDeCobranca']['complemento'] = ''

    pedido_hiper['enderecoDeEntrega']['cep'] = (pedido_data['billing']['postcode']).replace('-', '')
    pedido_hiper['enderecoDeEntrega']['logradouro'] = pedido_data['billing']['address_1']
    pedido_hiper['enderecoDeEntrega']['codigoIbge'] = buscar_codigo_ibge(pedido_data, 'billing')
    pedido_hiper['enderecoDeEntrega']['complemento'] = ''

    pedido_hiper['itens'] = buscar_produtos(pedido_data)
    pedido_hiper['meiosDePagamento'] = [{ 'idMeioDePagamento' : 1, 'parcelas' : 1, 'valor' :  buscar_valor_total(pedido_hiper['itens']) }]
    pedido_hiper['numeroPedidoDeVenda'] = ''
    pedido_hiper['observacaoDoPedidoDeVenda'] = ''
    pedido_hiper['valorDoFrete'] = buscar_meios_pagamento(pedido_data)

    for data in pedido_data['meta_data']:
        if data['key'] == '_billing_wooccm11':
            pedido_hiper['cliente']['documento'] = data['value']
        if data['key'] == '_billing_wooccm12':
            pedido_hiper['enderecoDeEntrega']['bairro'] = data['value']
            pedido_hiper['enderecoDeCobranca']['bairro'] = data['value']
        if data['key'] == '_billing_wooccm13':
            pedido_hiper['enderecoDeEntrega']['numero'] = data['value']
            pedido_hiper['enderecoDeCobranca']['numero'] = data['value']
    
    response = requests.post('https://ms-ecommerce.hiper.com.br/api/v1/pedido-de-venda', headers={ 'Authorization' : 'Bearer {}'.format(gerar_token(token_hiper)), 'Content-type': 'application/json' }, data=json.dumps(pedido_hiper))
    print('Status code: {}'.format(response.status_code))
    print('Response: {}'.format(response.text))

def formatar_nome_cliente(pedido):
    nome_cliente = ''
    pedido['billing']['first_name']
    if pedido['billing']['first_name'] is not None and pedido['billing']['last_name'] is not None:
        nome_cliente = pedido['billing']['first_name'].capitalize() + ' ' + pedido['billing']['last_name'].capitalize()
    else:
        nome_cliente = pedido['billing']['first_name'].capitalize()

    return nome_cliente
    

def gerar_token(token):
    print('Gerando token...')
    auth_data = requests.get('https://ms-ecommerce.hiper.com.br/api/v1/auth/gerar-token/{}'.format(token)).json()
    return auth_data['token']

def buscar_meios_pagamento(pedido):
    valor = 0
    for ship_line in pedido['shipping_lines']:
        valor = float(ship_line['total'])
    
    return valor

def buscar_produtos(pedido):
    print('Buscando produtos...')
    produtos = []
    for line_item in pedido['line_items']:
        produto = {}
        produto['produtoId'] = line_item['sku']
        produto['quantidade'] = line_item['quantity']
        produto['precoUnitarioBruto'] = float(line_item['total'])
        produto['precoUnitarioLiquido'] = float(line_item['total'])
        produtos.append(produto)
    return produtos

def buscar_valor_total(produtos):
    valor = 0
    for produto in produtos:
        valor += produto['precoUnitarioLiquido']
    
    return valor

def buscar_codigo_ibge(pedido, endereco_tipo):
    print('Buscando código do IBGE...')
    codigo = 0
    codigos_distritos = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/distritos').json()
    for cod_distrito in codigos_distritos:
        if cod_distrito['nome'].lower() == pedido[endereco_tipo]['city'].lower():
            codigo = cod_distrito['municipio']['id']
    print("Codigo encontrado: {}".format(codigo) )
    return codigo
    