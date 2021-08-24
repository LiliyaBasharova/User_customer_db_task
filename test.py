import pytest

from Catalog import Catalog
from data import engine
from db_utils import DbUtils

db_utils = DbUtils(engine)


def test_insert_user():
    old_users = list(db_utils.get_all_users())

    name = 'test_name'
    address = 'qwerty'
    tel = '123456789'
    data = {
        'name': name,
        'address': address,
        'tel': tel,
        'id': len(old_users) + 1,
    }

    db_utils.insert_user(**data)

    users = list(db_utils.get_all_users())

    assert len(users) == len(old_users) + 1
    user = users[-1]
    assert user.name == name, 'Неверное имя'
    assert user.address == address
    assert user.tel == tel

def test_insert_customer():
        old_customers = list(db_utils.get_all_customer())

        name = 'test_name'
        data = {
            'name': name,
            'id': len(old_customers) + 1,
        }

        db_utils.insert_customer(**data)

        customers = list(db_utils.get_all_customer())

        assert len(customers) == len(old_customers) + 1
        customer = customers[-1]
        assert customer.name == name, 'Неверное имя'


def test_create_catalog():
    catalog = Catalog(engine)

    users = list(db_utils.get_all_users())
    customers = list(db_utils.get_all_customer())

    assert len(catalog.users) == len(users)
    for i in range(len(users)):
        assert catalog.users[i] == users[i]

    assert len(catalog.customers) == len(customers)
    for i in range(len(customers)):
        assert catalog.customers[i] == customers[i]


