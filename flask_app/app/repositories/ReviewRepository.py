import abc
from app.models.ItemReviewModel import Review


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: Review):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> Review:
        raise NotImplementedError
    

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def add_all(self, product : list):
        self.session.add_all(product)

    def get(self):
        return self.session.query(Review).first()

    def get_by_id(self, id):
        return self.session.query(Review).where(Review.id == id).first()

    def list(self):
        return self.session.query(Review).all()
