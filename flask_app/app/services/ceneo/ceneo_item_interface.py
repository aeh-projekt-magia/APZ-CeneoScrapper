from abc import ABC, abstractmethod


class CeneoItemInterface(ABC):
    @abstractmethod
    def fetch_lowest_price(self, item_id: str) -> dict:
        """
        Finds the lowest price of the item and the link to the offer.
        Args:
            item_id: webservice id of the item

        Returns:
            dict containing item id, the lowest price, url of the offer and the timestamp

            dict format:
            >>> dict_ = {
            >>> 'item_id': '017761',
            >>> 'item_name': 'Iphone 13',
            >>> 'price': 1722.90,
            >>> 'offer': 'https://offer.com',
            >>> 'timestamp': '2023-03-30 00:15:18.919107'
            >>> }
        """
        ...

    @abstractmethod
    def find_id_by_item_name(self, item_name: str) -> dict:
        """
        Args:
            item_name: human-readable name of the item

        Returns:
            dict containing item id, the searched name, actual name.
        """
        ...
