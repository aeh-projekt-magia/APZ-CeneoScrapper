from app.services.ceneo.item_interface import ItemInterface


class CeneoItem(ItemInterface):
    def fetch_lowest_price(self, item_id: str) -> dict:
        return {}

    def find_id_by_item_name(self, item_name: str) -> str:
        return ''
