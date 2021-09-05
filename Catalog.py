from typing import List, Dict
from db_utils import DbUtils
from data import Samplemutation, Samples, Mutation
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update

class Catalog:
    db_utils: DbUtils = None
    samples: List[Samples] = None
    mutations: List[Mutation] = None
    
    sample_mutation: Dict[int, List[Mutation]] = None
    
    def __init__(self, engine):
        db_utils = DbUtils(engine=engine)
        self.db_utils = db_utils

        self.samples = list(db_utils.get_all_samples())
        self.mutations = list(db_utils.get_all_mutation())
        
        self.sample_mutation = {}
        for sample in self.samples:
            self.sample_mutation[sample.id] = db_utils.get_mutations_by_sample(sample.id)


    def insert_sample(self, **kwargs) -> samples:
        new_sample = self.db_utils.insert_sample(**kwargs)
        self.samples.append(new_sample)
        return new_sample

    def insert_mutation(self, **kwargs) -> Mutation:
        new_mutation = self.db_utils.insert_mutation(**kwargs)
        self.mutations.append(new_mutation)
        return new_mutation

    def update_sample(self, **kwargs):
        self.db_utils.update_sample(**kwargs)

    def update_mutation(self, **kwargs):
        self.db_utils.update_mutation(**kwargs)

    def add_mutation_to_sample(self, sample_id, mutation_id):
        new_sample_mutation = self.db_utils.add_mutation_to_sample(sample_id, mutation_id)
        self.sample_mutation[sample_id] = self.db_utils.get_mutations_by_sample(sample_id)

    def delete_mutation_from_sample(self, sample_id, mutation_id):
        self.db_utils.delete_mutation_from_sample(sample_id, mutation_id)
        self.sample_mutation[sample_id] = [mutation for mutation in self.sample_mutation[sample_id] if mutation.id != mutation_id]

    def read_samples(self):
        return self.db_utils.get_all_samples()

    def read_mutation(self):
        return self.db_utils.get_all_mutation()

