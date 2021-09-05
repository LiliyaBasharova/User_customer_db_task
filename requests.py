from flask import Flask
from flask import abort
from flask import jsonify
from flask import request

from Catalog import *
from db_utils import *

catalog = Catalog(engine)
app = Flask(__name__)


@app.route("/samples/<int:sample_id>")
def request_catalog_sample(sample_id):
    read_samples = catalog.read_samples()
    for sample in read_samples:
        if sample.id == sample_id:
            return (create_dict_samples(sample))
    abort(404)


@app.route("/samples/")
def request_catalog_samples():
    read_samples = catalog.read_samples()
    samples_list = []
    for sample in read_samples:
        dict_samples = create_dict_samples(sample)
        samples_list.append(dict_samples)
    return jsonify(samples_list)


def create_dict_samples(sample):
    dict_sample = {
        "id": sample.id,
        "name": sample.name
    }
    return dict_sample


def create_dict_mutation(mutation):
    dict_mutation = {
        "id": mutation.id,
        "name": mutation.name
    }
    return dict_mutation


@app.route("/mutation/<int:mutation_id>")
def request_catalog_mutation(mutation_id):
    read_mutation = catalog.read_mutation()
    for mutation in read_mutation:
        if mutation.id == mutation_id:
            return create_dict_mutation(mutation)
    abort(404)


@app.route("/mutations/")
def request_catalog_mutations():
    read_mutations = catalog.read_mutation()
    mutations_list = []
    for mutation in read_mutations:
        dict_mutation = create_dict_mutation(mutation)
        mutations_list.append(dict_mutation)
    return jsonify(mutations_list)


@app.route('/samples', methods=['POST'])
def create_sample():
    sample_data = request.form
    samples = catalog.insert_sample(**sample_data)
    return {
        "id": samples.id,
        "name": samples.name
    }


@app.route('/mutations', methods=['POST'])
def create_mutation_post():
    mutation_data = request.form
    mutations = catalog.insert_mutation(**mutation_data)
    return create_dict_mutation(mutations)


@app.route('/samples', methods=['POST'])
def create_sample_post():
    sample_data = request.form
    sample = catalog.insert_sample(**sample_data)
    return create_dict_samples(sample)


@app.route('/samples/<int:sample_id>', methods=['POST'])
def update_sample_post(sample_id: int):
    sample_data = request.form
    sample = catalog.update_sample(sample_id=sample_id, **sample_data)
    return create_dict_samples(sample)

@app.route('/samples/<int:mutation_id>', methods=['POST'])
def update_mutation_post(mutation_id: int):
    mutation_data = request.form
    mutation = catalog.update_mutation(mutation_id=mutation_id, **mutation_data)
    return create_dict_mutation(mutation)