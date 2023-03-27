from abc import ABC, abstractmethod


class ProductStatusInterface(ABC):
    """
    Provides an interface for checking detailed information about a particular product
    """

    @abstractmethod
    def get_lowest_price(self, product_id: str, location: str) -> dict:
        """
        @param product_id:
        @param location:
        @return:
        """
        ...

    @abstractmethod
    def get_product_availability(self, product_id: str, location: str) -> dict:
        """

        @param product_id:
        @param location:
        @return:
        """
        ...
