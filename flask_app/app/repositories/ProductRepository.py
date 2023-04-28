import abc
from app.models.ProductModel import Products


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: Products):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> Products:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self):
        return self.session.query(Products).first()

    def get_by_id(self, id):
        return self.session.query(Products).where(Products.id == id).first()

    def get_by_id_list(self, id):
        return self.session.query(Products).where(Products.id == id).all()

    def get_by_name(self, name):
        return self.session.query(Products).where(Products.name == name).first()

    def list(self):
        return self.session.query(Products).all()
