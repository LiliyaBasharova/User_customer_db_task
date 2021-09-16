from typing import List
from sqlalchemy import delete, literal_column
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from data import Samples, Mutation, engine, Samplemutation


def with_session(engine):
    def decorator(method):
        def inner(*args, **kwargs):
            Session = sessionmaker(bind=engine)
            session = Session()
            result = method(*args, session=session, **kwargs)
            session.close()
            return result
        return inner
    return decorator



class DbUtils:
    session = None

    def __init__(self, engine):
        # print('init')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    @with_session(engine)
    def get_all_samples(self, session):
        return session.query(Samples).order_by(Samples.id)

    @with_session(engine)
    def get_all_mutation(self, session):
        return session.query(Mutation).order_by(Mutation.id)

    @with_session(engine)
    def delete_samples(self, session, id):
        delete_sample = (
            delete(Samples).where(Samples.id == id)
        )
        session.execute(delete_sample)


    @with_session(engine)
    def get_mutations_by_sample(self, sample_id, session) -> List[Mutation]:
        sample_mutations = session.query(Samplemutation).filter_by(sample_id=sample_id)
        mutations_ids = [sample_mutation.mutation_id for sample_mutation in sample_mutations]
        mutations = session.query(Mutation).filter(Mutation.id.in_(mutations_ids))
        return mutations

    @with_session(engine)
    def create_sample_mutation(self, session):
        for sample_id in range(1, 11):
            for mutation_id in range(1, 11):
                sample_mutation = Samplemutation(sample_id=sample_id, mutation_id=mutation_id)
                session.add(sample_mutation)
        session.commit()

    @with_session(engine)
    def insert_sample(self,  session, **kwargs) -> Samples:
        print(kwargs)
        insert_sample = (
            insert(Samples).values(**kwargs).returning(literal_column('*'))
        )
        result = session.execute(insert_sample)
        session.commit()
        fetched = result.fetchone()
        return Samples(**fetched)

    @with_session(engine)
    def insert_mutation(self, session,  **kwargs) -> Mutation:
        insert_mutation = (
            insert(Mutation).values(**kwargs).returning(literal_column('*'))
        )
        result = session.execute(insert_mutation)
        session.commit()
        fetched = result.fetchone()
        return Mutation(**fetched)

    @with_session(engine)
    def update_sample(self, sample_id, session, **kwargs):
        update_table = (
            update(Samples).
                where(Samples.id == sample_id).
                values(**kwargs).returning(literal_column('*'))
        )
        result = session.execute(update_table)
        session.commit()
        fetched = result.fetchone()
        return Samples(**fetched)


    @with_session(engine)
    def update_mutation(self, mutation_id, session, **kwargs):
        update_table = (
            update(Mutation).
                where(Mutation.id == mutation_id).
                values(**kwargs).returning(literal_column('*'))
        )
        result = session.execute(update_table)
        session.commit()
        fetched = result.fetchone()
        return Mutation(**fetched)

    @with_session(engine)
    def add_mutation_to_sample(self, sample_id, mutation_id ,session) -> Samplemutation:
        query = insert(Samplemutation).values(sample_id=sample_id, mutation_id=mutation_id)
        result = session.execute(query)
        session.commit()

        return result

    @with_session(engine)
    def delete_mutation_from_sample(self, sample_id, mutation_id,session):
        query = delete(Samplemutation).where(Samplemutation.sample_id == sample_id,
                                             Samplemutation.mutation_id == mutation_id)
        session.execute(query)
        session.commit()



