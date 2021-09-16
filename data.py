import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


Base = declarative_base()

engine = create_engine('postgresql://postgres:postgres@localhost:5432/test')


class Samples(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    mutations = relationship('Mutation')
    sqlalchemy.UniqueConstraint('id', 'name')

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"Sample name={self.name}"

    def create_dict_samples(sample):
        dict_sample = {
            "id": sample.id,
            "name": sample.name
        }
        return dict_sample



class Mutation(Base):
    __tablename__ = "mutation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"))
    sqlalchemy.UniqueConstraint('id', 'count')

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"Mutation name={self.count}"
    def create_dict_mutation(mutation):
        dict_mutation = {
            "id": mutation.id,
            "count": mutation.count
        }
        return dict_mutation

class Samplemutation(Base):
    __tablename__ = "sample_mutation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey("samples.id"))
    mutation_id = Column(Integer, ForeignKey("mutation.id"))

    def __eq__(self, other):
        return self.id == other.id


#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
