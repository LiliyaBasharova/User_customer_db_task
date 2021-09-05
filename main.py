from Catalog import *
from db_utils import *

catalog = Catalog(engine)
session = None


def __init__(self, engine):
    print('init')
    Session = sessionmaker(bind=engine)
    self.session = Session()


