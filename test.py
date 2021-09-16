from Catalog import Catalog
from data import engine
from db_utils import DbUtils
import pytest
db_utils = DbUtils(engine)


def test_insert_sample():
    old_samples = list(db_utils.get_all_samples())

    name = 'test_name'
    data = {
        'name': name,
        'id': len(old_samples) + 1,
    }

    db_utils.insert_sample(**data)

    samples = list(db_utils.get_all_samples())

    assert len(samples) == len(old_samples) + 1
    sample = samples[-1]
    assert sample.name == name, 'Неверное имя'


def test_insert_mutation():
    old_mutations = list(db_utils.get_all_mutation())

    count = 10
    data = {
        'count': count,
        'id': len(old_mutations) + 1,
    }

    db_utils.insert_mutation(**data)

    mutations = list(db_utils.get_all_mutation())

    assert len(mutations) == len(old_mutations) + 1
    mutation = mutations[-1]
    assert mutation.count == count, 'Неверное количество'


def test_create_catalog():
    catalog = Catalog(engine)

    samples = list(db_utils.get_all_samples())
    mutations = list(db_utils.get_all_mutation())

    assert len(catalog.samples) == len(samples)
    for i in range(len(samples)):
        assert catalog.samples[i] == samples[i]

    assert len(catalog.mutations) == len(mutations)
    for i in range(len(mutations)):
        assert catalog.mutations[i] == mutations[i]


def test_update_catalog():
    catalog = Catalog(engine)

    samples = list(db_utils.get_all_samples())
    name = 'test_name'
    data = {
        'name': name,
        'id': len(samples) + 1,
    }

    catalog.insert_sample(**data)
    new_samples = list(catalog.read_samples())

    assert len(new_samples) == len(samples) + 1
    sample = new_samples[-1]
    assert sample.name == name, 'Неверное имя'

    old_mutations = list(catalog.read_mutation())
    count = 10
    data = {
        'count': count,
        'id': len(old_mutations) + 1,
    }

    catalog.insert_mutation(**data)
    new_mutations = list(catalog.read_mutation())

    assert len(new_mutations) == len(old_mutations) + 1
    mutation = new_mutations[-1]
    assert mutation.count == count, 'Неверное имя'

    assert len(catalog.samples) == len(new_samples)
    for i in range(len(samples)):
        assert catalog.samples[i] == samples[i]

    assert len(catalog.mutations) == len(new_mutations)
    for i in range(len(new_mutations)):
        assert catalog.mutations[i] == new_mutations[i]


