import requests
from app.hiper_wordpress.domain.Customer import Customer
from app.hiper_wordpress.service import customer_service
from woocommerce import API
from app import app


def autenticar_woocommerce(cliente):
    wcapi = API(
        url= cliente.get('site'),
        consumer_key=cliente.get('consumer_key'),
        consumer_secret=cliente.get('consumer_secret'),
        version="wc/v3",
        timeout=30
    )

    return wcapi

def exportar_todos_clientes():
    print('Realizando migração de todos os clientes da Hiper para o Woocommerce...')
    with app.app_context():
        for cliente in customer_service.get_customers():
            print('Cliente [{}]'.format(cliente['site']))
            try:
                produtos = requests.get('https://ms-ecommerce.hiper.com.br/api/v1/produtos/pontoDeSincronizacao', headers={'Authorization' : 'Bearer {}'.format(gerar_token(cliente['token_hiper']))}).json()['produtos']
                print('{} produtos encontrados.'.format(len(produtos)))
                for produto_hiper in produtos:
                    autenticacao = autenticar_woocommerce(cliente)
                    produto = gerar_produto_objeto(produto_hiper, autenticacao)
                    try:
                        adicionar_produto(produto, produto_hiper, autenticacao)
                        print(f'Produtos enviados para o cliente [{cliente.get("site")}].')
                    except Exception as exc:
                        print(f'Erro ao enviar produto para o cliente [{cliente.get("site")}].')
            except Exception as exp:
                print('Não foi possível buscar os produtos no Hiper. Exceção: {}'.format(exp))

def gerar_produto_objeto(produto_hiper, autenticacao):
    print("Nome do produto no Hiper: {}".format(produto_hiper['nome']))

    produto = {
        'sku' : produto_hiper['id'], 
        'name' : produto_hiper['nome'],
        'regular_price' : str(produto_hiper['preco']),
        'short_description' : produto_hiper['descricao'],
        'stock_quantity' : produto_hiper['quantidadeEmEstoque'],
        'categories' : buscar_categorias(autenticacao, produto_hiper) if produto_hiper['categoria'] is not None else [],
        'stock_status' : gerar_status_estoque(produto_hiper),
        'weight' : str(produto_hiper['peso']),
        'dimensions' : { 'length' : str(produto_hiper['comprimento']) , 'width' : str(produto_hiper['largura']), 'height' : str(produto_hiper['altura']) }
    }

    if produto_hiper['imagem'] is not None:
        produto['images'] = [ { 'src' : produto_hiper['imagem'] } ] 

    return produto        

def buscar_categorias(wcapi, produto):
    categorias = wcapi.get("products/categories").json()
    categorias_produto = []
    categoria_existente = False
    for categoria in categorias:
        if categoria['name'] == produto['categoria'] and produto['categoria'] is not None:
            categoria_existente = True
            categorias_produto.append(categoria)
    
    if categoria_existente == False:
        print("Categoria [{}] não existente, realizando criação.".format(produto['categoria']))
        categoria_obj = {
            "name" : produto['categoria']
        }

        response = wcapi.post("products/categories", categoria_obj).json()
        categorias_produto.append( wcapi.get("products/categories/{}".format(response['id'])).json())
        print("Categoria [{}] criada.".format(produto['categoria']))
    
    return categorias_produto

def gerar_status_estoque(produto):
    status = 'instock'
    if produto['quantidadeEmEstoque'] < 1:
        status = 'outofstock'
    return status

def adicionar_produto(produto, produto_hiper, wcapi):
    print('Realizando adição no WooCommerce do produto.')
    produtos = wcapi.get("products").json()
    for produto_woocommerce in produtos:
        if produto_woocommerce['sku'] == produto_hiper['id']:
            print('Produto [{}] existente. Apagando produto para posteriormente criá-lo novamente.'.format(produto_woocommerce['name']))
            print(wcapi.delete("products/{}".format(produto_woocommerce['id']), params={"force": True}).json())
            print('Produto [{}] apagado.'.format(produto_woocommerce['name']))

    print('Criando produto [{}].'.format(produto['name']))
    print(wcapi.post("products", produto).json())
    print('Produto [{}] criado.'.format(produto['name']))

def gerar_token(token):
    token_response = requests.get('https://ms-ecommerce.hiper.com.br/api/v1/auth/gerar-token/{}'.format(token))
    print(token_response)
    return token_response.json()['token']
