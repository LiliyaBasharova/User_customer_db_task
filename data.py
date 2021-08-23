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

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    tel = Column(String(250), nullable=False)
    customers = relationship('Customer')
    sqlalchemy.UniqueConstraint('id', 'name', 'tel')

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"User name={self.name}, tel={self.tel}"

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    sqlalchemy.UniqueConstraint('id', 'name')

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"Customer name={self.name}"

class UserCustomer(Base):
    __tablename__ = "user_customer"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    customer_id = Column(Integer, ForeignKey("customer.id"))

    def __eq__(self, other):
        return self.id == other.id

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
