from typing import List

from sqlalchemy import delete, literal_column
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker

from data import Samples, Mutation, engine, Samplemutation


class DbUtils:
    session = None

    def __init__(self, engine):
        # print('init')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_samples(self):
        return self.session.query(Samples).order_by(Samples.id)

    def get_all_mutation(self):
        return self.session.query(Mutation).order_by(Mutation.id)

    def delete_samples(self, id):
        delete_sample = (
            delete(Samples).where(Samples.id == id)
        )
        self.session.execute(delete_sample)

    def get_mutations_by_sample(self, sample_id) -> List[Mutation]:
        sample_mutations = self.session.query(Samplemutation).filter_by(sample_id=sample_id)
        mutations_ids = [sample_mutation.mutation_id for sample_mutation in sample_mutations]
        mutations = self.session.query(Mutation).filter(Mutation.id.in_(mutations_ids))
        return mutations

    def create_sample_mutation(self):
        for sample_id in range(1, 11):
            for mutation_id in range(1, 11):
                sample_mutation = Samplemutation(sample_id=sample_id, mutation_id=mutation_id)
                self.session.add(sample_mutation)
        self.session.commit()

    def insert_sample(self, **kwargs) -> Samples:
        insert_sample = (
            insert(Samples).values(**kwargs).returning(literal_column('*'))
        )
        result = self.session.execute(insert_sample)
        self.session.commit()
        fetched = result.fetchone()
        return Samples(**fetched)

    def insert_mutation(self, **kwargs) -> Mutation:
        insert_mutation = (
            insert(Mutation).values(**kwargs).returning(literal_column('*'))
        )
        result = self.session.execute(insert_mutation)
        self.session.commit()
        fetched = result.fetchone()
        return Mutation(**fetched)

    def update_sample(self, sample_id, **kwargs):
        update_table = (
            update(Samples).
                where(Samples.id == sample_id).
                values(**kwargs)
        )
        self.session.execute(update_table)
        self.session.commit()

    def update_mutation(self, mutation_id, **kwargs):
        update_table = (
            update(Mutation).
                where(Mutation.id == mutation_id).
                values(**kwargs)
        )
        self.session.execute(update_table)
        self.session.commit()

    def add_mutation_to_sample(self, sample_id, mutation_id) -> Samplemutation:
        query = insert(Samplemutation).values(sample_id=sample_id, mutation_id=mutation_id)
        result = self.session.execute(query)
        self.session.commit()
        return result

    def delete_mutation_from_sample(self, sample_id, mutation_id):
        query = delete(Samplemutation).where(Samplemutation.sample_id == sample_id,
                                             Samplemutation.mutation_id == mutation_id)
        self.session.execute(query)
        self.session.commit()



