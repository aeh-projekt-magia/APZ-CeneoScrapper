from app.models.ItemModel import Item
from app.models.PriceHistoryModel import PriceHistory
from app.repository.item.item_repository import ItemRepository
from app.repository.price_history.price_history_repository import PriceHistoryRepository
from app.services.ceneo.ceneo_item_interface import CeneoItemInterface


class ItemService:
    def __init__(
        self,
        ceneo_item_interface: CeneoItemInterface,
        item_repository: ItemRepository,
        price_history_repository: PriceHistoryRepository,
    ):
        self.ceneo_item = ceneo_item_interface
        self.item_repository = item_repository
        self.price_history_repository = price_history_repository

    def get_all_products_to_show(self):
        return self.item_repository.get_all_items()

    def get_product_to_show_by_id(self, item_id: str):
        return self.item_repository.get_item_by_id(item_id)

    def fetch_item(self, item_name: str) -> Item:
        """
        In case a record with matching item name is available
        in the database the record is returned. A new Item record is
        created in other case. The id of a new Item is fetched from ceneo.
        Args:
            item_name: the name of the item

        Returns: the corresponding Item object
        """
        item = self.item_repository.get_item_by_name(item_name)
        if item is None:
            item_id_dict = self.ceneo_item.find_id_by_item_name(item_name)
            new_item = Item(
                item_id=item_id_dict["item_id"],
                name=item_id_dict["item_name"],
            )
            self.item_repository.add_item(new_item)
            return new_item
        return item

    def update_price(self, item_id: str):
        lowest_price_dict = self.ceneo_item.fetch_lowest_price(item_id)
        updated_item = self.item_repository.get_item_by_id(item_id)
        updated_item.price = lowest_price_dict["price"]
        updated_item.offer_url = lowest_price_dict["offer_url"]
        updated_item.is_available = True
        updated_item.last_updated = lowest_price_dict["timestamp"]
        self.item_repository.update_item(updated_item)
        price_hist = PriceHistory(
            price=lowest_price_dict["price"],
            date=lowest_price_dict["timestamp"],
            item_id=updated_item.id,
        )
        self.price_history_repository.add_price_history(price_hist)

    def get_all_products_to_show_paginate(self, page, pages: int):
        return self.item_repository.get_all_items_paginate(page, pages)

    def get_all_products_to_show_by_name(self, item_name: str):
        return self.item_repository.get_items_by_name_contains(item_name)
