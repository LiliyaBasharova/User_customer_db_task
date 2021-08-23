from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker

from data import Users, Customer, engine
from Catalog import *
from db_utils import *

session = None

def __init__(self, engine):
        print('init')
        Session = sessionmaker(bind=engine)
        self.session = Session()


catalog = Catalog(engine)
catalog.insert_user(id='12', name='Vanya', tel='89174764762', address='Moscow')
catalog.insert_customer(id='15', name='Petr')
catalog.update_user(user_id='5', name='Misha', tel='89174764762', address='Ufa')
catalog.update_customer(customer_id='7', name="Anna")
catalog.add_customer_to_user(user_id='1', customer_id='15')
#catalog.delete_customer_from_user(user_id='1', customer_id='15')
catalog.read_users()
catalog.read_customer()

