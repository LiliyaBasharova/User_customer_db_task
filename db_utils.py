from typing import List

from sqlalchemy import delete, literal_column
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker

from data import Users, Customer, engine, UserCustomer


class DbUtils:
    session = None

    def __init__(self, engine):
        # print('init')
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def create_test_users(self):
        for user_id in range(1, 11):
            user = Users(id=user_id, name=f"test_{user_id}", address="test address", tel="test tel")
            self.session.add(user)
        self.session.commit()

    def create_test_customers(self):
        for customer_id in range(1, 11):
            customer = Customer(id=customer_id, name=f"customer_{customer_id}")
            self.session.add(customer)
        self.session.commit()

    def get_all_users(self):
        return self.session.query(Users).order_by(Users.id)

    def get_all_customer(self):
        return self.session.query(Customer).order_by(Customer.id)

    # def read_all_users(self):
    #     for instance in self.get_all_users():
    #         print(instance.name)
    #
    # def read_all_customers(self):
    #     for instance in self.get_all_customer():
    #         print(instance.name)

    def delete_users(self, id):
        delete_user = (
            delete(Users).where(Users.id == id)
        )
        self.session.execute(delete_user)

    # def test_insert_user(self):
    #     insert_user = (
    #         insert(Users).values(name='username', address='')
    #     )
    #     self.session.execute(insert_user)
    #
    # def test_update_user(self):
    #     update_table = (
    #         update(Users).
    #             where(Users.id == 5).
    #             values(name='user #5')
    #     )
    #     self.session.execute(update_table)

    def get_customers_by_user(self, user_id) -> List[Customer]:
        user_customers = self.session.query(UserCustomer).filter_by(user_id=user_id)
        customers_ids = [user_customer.customer_id for user_customer in user_customers]
        customers = self.session.query(Customer).filter(Customer.id.in_(customers_ids))
        return customers

    def create_user_customer(self):
        for user_id in range(1, 11):
            for customer_id in range(1, 11):
                user_customer = UserCustomer(user_id=user_id, customer_id=customer_id)
                self.session.add(user_customer)
        self.session.commit()

    def insert_user(self, **kwargs) -> Users:
        insert_user = (
            insert(Users).values(**kwargs).returning(literal_column('*'))
        )
        result = self.session.execute(insert_user)
        self.session.commit()
        fetched = result.fetchone()
        return Users(**fetched)

    def insert_customer(self, **kwargs) -> Customer:
        insert_customer = (
        insert(Customer).values(**kwargs).returning(literal_column('*'))
    )
        result = self.session.execute(insert_customer)
        self.session.commit()
        fetched = result.fetchone()
        return Customer(**fetched)

    def update_user(self, user_id, **kwargs ):
        update_table = (
            update(Users).
                where(Users.id ==user_id ).
                values(**kwargs)
        )
        self.session.execute(update_table)
        self.session.commit()

    def update_customer(self, customer_id, **kwargs):
        update_table = (
            update(Customer).
                where(Customer.id == customer_id).
                values(**kwargs)
        )
        self.session.execute(update_table)
        self.session.commit()

    def add_customer_to_user(self, user_id, customer_id) -> UserCustomer:
        query = insert(UserCustomer).values(user_id=user_id, customer_id=customer_id)
        result = self.session.execute(query)
        self.session.commit()
        return result

    def delete_customer_from_user(self, user_id, customer_id):
        query = delete(UserCustomer).where(UserCustomer.user_id==user_id, UserCustomer.customer_id==customer_id)
        self.session.execute(query)
        self.session.commit()


db_utils = DbUtils(engine=engine)
db_utils.create_test_users()
db_utils.create_test_customers()
db_utils.create_user_customer()
for user in db_utils.get_all_users():
    b = db_utils.get_customers_by_user(user.id)
    print(b)
    for _b in b:
        print(_b)

