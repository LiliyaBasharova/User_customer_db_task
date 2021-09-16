from flask import Flask
from flask import abort
from flask import jsonify
from flask import request

from Catalog import *
from db_utils import *
from data import *

catalog = Catalog(engine)
app = Flask(__name__)


@app.route("/catalog/")
def request_catalog():
    return catalog.create_dict_catalog()


@app.route('/catalog', methods=['POST'])
def create_catalog():
    data = request.form
    sample_id = int(data['sample_id'])
    mutation_id = int(data['mutation_id'])
    result = catalog.add_mutation_to_sample(sample_id=sample_id, mutation_id=mutation_id)
    return jsonify([mutation.create_dict_mutation() for mutation in result])


@app.route("/samples/<int:sample_id>")
def request_catalog_sample(sample_id):
    read_samples = catalog.read_samples()
    for sample in read_samples:
        if sample.id == sample_id:
            return sample.create_dict_samples()
    abort(404)


@app.route("/samples/")
def request_catalog_samples():
    read_samples = catalog.read_samples()
    samples_list = []
    for sample in read_samples:
        dict_samples = sample.create_dict_samples()
        samples_list.append(dict_samples)
    return jsonify(samples_list)


@app.route("/mutation/<int:mutation_id>")
def request_catalog_mutation(mutation_id):
    read_mutation = catalog.read_mutation()
    for mutation in read_mutation:
        if mutation.id == mutation_id:
            return mutation.create_dict_mutation()
    abort(404)


@app.route("/mutations/")
def request_catalog_mutations():
    read_mutations = catalog.read_mutation()
    mutations_list = []
    for mutation in read_mutations:
        dict_mutation = mutation.create_dict_mutation()
        mutations_list.append(dict_mutation)
    return jsonify(mutations_list)


@app.route('/samples', methods=['POST'])
def create_sample():
    sample_data = request.form
    samples = catalog.insert_sample(**sample_data)
    return samples.create_dict_samples()


@app.route('/mutations', methods=['POST'])
def create_mutation():
    mutation_data = request.form
    mutations = catalog.insert_mutation(**mutation_data)
    return mutations.create_dict_mutation()


@app.route('/samples/<int:sample_id>', methods=['POST'])
def update_sample_post(sample_id: int):
    sample_data = request.form
    sample = catalog.update_sample(sample_id=sample_id, **sample_data)
    return sample.create_dict_samples()


@app.route('/mutations/<int:mutation_id>', methods=['POST'])
def update_mutation_post(mutation_id: int):
    mutation_data = request.form
    mutation = catalog.update_mutation(mutation_id=mutation_id, **mutation_data)
    return mutation.create_dict_mutation()


app.run(debug=True, use_debugger=False, use_reloader=False)
