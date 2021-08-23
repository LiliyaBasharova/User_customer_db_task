from db_utils import DbUtils
from data import UserCustomer, Users, Customer
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update

class Catalog:
    db_utils: DbUtils = None
    users: list[Users] = None
    customers: list[Customer] = None
    
    user_customer: dict[int, list[Customer]] = None
    
    def __init__(self, engine):
        db_utils = DbUtils(engine=engine)
        self.db_utils = db_utils

        self.users = list(db_utils.get_all_users())
        self.customers = list(db_utils.get_all_customer())
        
        self.user_customer = {}
        for user in self.users:
            self.user_customer[user.id] = db_utils.get_customers_by_user(user.id)


    def insert_user(self, **kwargs) -> Users:
        new_user = self.db_utils.insert_user(**kwargs)
        self.users.append(new_user)
        return new_user

    def insert_customer(self, **kwargs) -> Customer:
        new_customer = self.db_utils.insert_customer(**kwargs)
        self.customers.append(new_customer)
        return new_customer

    def update_user(self, **kwargs):
        self.db_utils.update_user(**kwargs)

    def update_customer(self, **kwargs):
        self.db_utils.update_customer(**kwargs)

    def add_customer_to_user(self, user_id, customer_id):
        new_user_customer = self.db_utils.add_customer_to_user(user_id, customer_id)
        self.user_customer[user_id] = self.db_utils.get_customers_by_user(user_id)

    def delete_customer_from_user(self, user_id, customer_id):
        self.db_utils.delete_customer_from_user(user_id, customer_id)
        self.user_customer[user_id] = [customer for customer in self.user_customer[user_id] if customer.id != customer_id]

    def read_users(self):
        return self.db_utils.get_all_users()

    def read_customer(self):
        return self.db_utils.get_all_customer()

