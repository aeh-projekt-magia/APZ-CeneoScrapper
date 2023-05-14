from app.models.ItemModel import Item
from app.extensions import db
import datetime

from app.repository.item.item_repository import ItemRepository


class ImplItemRepository(ItemRepository):

    def add_item(self, item: Item):
        if item.last_updated is None:
            item.last_updated = datetime.datetime.now()
        db.session.add(item)
        db.session.commit()
        return item

    def get_item_by_id(self, item_id: str):
        item = db.session.execute(
            db.select(Item).filter_by(id=item_id)
        ).scalar_one()
        return item

    def get_item_by_name(self, name: str):
        item = db.session.execute(
            db.select(Item).filter_by(name=name)
        ).scalar_one_or_none()
        return item

    def get_all_items(self):
        items = db.session.execute(db.select(Item)).all()
        return items

    def delete_item_by_id(self, item_id: str):
        item = db.session.execute(
            db.select(Item).filter_by(id=item_id)
        ).scalar_one()
        db.session.delete(item)
        db.session.commit()

    def delete_all_items(self):
        db.session.query(Item).delete()
        db.session.commit()

    def update_item(self, item: Item):
        old_item = db.session.execute(
            db.select(Item).filter_by(id=item.id)
        ).scalar_one()
        if item.is_available is not None:
            old_item.is_available = item.is_available
        if item.lowest_price is not None:
            old_item.lowest_price = item.lowest_price
        if item.price is not None:
            old_item.price = item.price
        if item.offer_url is not None:
            old_item.offer_url = item.offer_url
        if item.last_updated is not None:
            old_item.last_updated = item.last_updated
        else:
            old_item.last_updated = datetime.datetime.now()

        db.session.commit()
