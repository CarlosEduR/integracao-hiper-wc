from app import db
from app.hiper_wordpress.domain.Customer import Customer

def create_customer(customer):
    db.session.add(customer)
    db.session.commit()
    print('Cliente criado.')

def get_customers():
    return [customer.__dict__ for customer in Customer.query.all()]

def delete_customer(customer):
    query = Customer.query.filter(Customer.site==customer.site).delete()
    db.session.commit()
    print('cliente deletado...')

def get_customer_by_site(site):
    return Customer.query.filter_by(site=site).first()
   

def update_customer(customer, id_customer):
    query = Customer.query.filter(Customer.id_customer==id_customer).update({ "site" : customer.site, "consumer_key" : customer.consumer_key, "consumer_secret" : customer.consumer_secret, "token_hiper" : customer.token_hiper })
    db.session.commit()
    print('cliente atualizado...')

