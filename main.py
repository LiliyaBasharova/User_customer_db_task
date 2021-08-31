from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from data import Users, Customer, UserCustomer, engine
from Catalog import *
from db_utils import *
import requests
import json
import flask
from flask import Flask
from flask import jsonify
from flask import abort
from flask import request


session = None
catalog = Catalog(engine)
app = Flask(__name__)

@app.route("/users/<int:user_id>")
def request_catalog_user(user_id):
    read_users = catalog.read_users()
    for user in read_users:
        if user.id == user_id:
            return {
                "id": user.id,
                "name": user.name,
                "address": user.address,
                "tel": user.tel

            }
    abort(404)

@app.route("/customers/<int:customer_id>")
def request_catalog_customer(customer_id):
    read_customer = catalog.read_customer()
    for customers in read_customer:
        if customers.id == customer_id:
            return {
                "id": customers.id,
                "name": customers.name,
            }
    abort(404)

@app.route("/users/")
def request_catalog_users():
    read_users = catalog.read_users()
    users_list = []
    for users in read_users:
        dict_users = {
            "id": users.id,
            "name": users.name,
            "address": users.address,
            "tel": users.tel

        }
        List.append(dict_users)
    return jsonify(users_list)
@app.route("/customers/")
def request_catalog_customers():
    read_customers = catalog.read_customer()
    customers_list = []
    for customers in read_customers:
        dict_customer = {
            "id": customers.id,
            "name": customers.name,
            "address": customers.address,
            "tel": customers.tel

        }
        List.append(dict_customer)
    return jsonify(customers_list)


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.form
    users = catalog.insert_user(**user_data)
    return {
            "id": users.id,
            "name": users.name,
            "address": users.address,
            "tel": users.tel

        }
@app.route('/customers', methods=['POST'])
def create_customer():
    customer_data = request.form
    customers = catalog.insert_customer(**customer_data)
    return {
            "id": customers.id,
            "name": customers.name,
            "address": customers.address,
            "tel": customers.tel

        }
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.form
    customers = catalog.insert_user(**user_data)
    return {
            "id": user.id,
            "name": user.name,
            "address": user.address,
            "tel": user.tel

        }

# def __init__(self, engine):
#     print('init')
#     Session = sessionmaker(bind=engine)
#     self.session = Session()

#
#
# db_utils.create_test_users()
# db_utils.create_test_customers()
#

# catalog.insert_user(id='12', name='Vanya', tel='89174764762', address='Moscow')
# catalog.insert_customer(id='15', name='Petr')
# catalog.update_user(user_id='5', name='Misha', tel='89174764762', address='Ufa')
# catalog.update_customer(customer_id='7', name="Anna")
# catalog.add_customer_to_user(user_id='1', customer_id='15')
# # catalog.delete_customer_from_user(user_id='1', customer_id='15')
# catalog.read_users()
# catalog.read_customer()
