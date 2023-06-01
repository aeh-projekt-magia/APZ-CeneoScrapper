from app.services.ceneo.web_scrapper.data_objects.ceneo_data_object import (
    CeneoDataObject,
)


class ItemData(CeneoDataObject):
    def __init__(
            self,
            item_id: str = "",
            item_name: str = "",
            item_search_name: str = "",
            image_url: str = ""

    ):
        self.item_id = item_id
        self.item_name = item_name
        self.item_search_name = item_search_name
        self.image_url = image_url

    def as_string(self):
        return (
            f"item name = {self.item_name}\n"
            f"item id = {self.item_id}\n"
            f"item search name = {self.item_search_name}\n"
            f"image url = {self.image_url}"
        )

    def as_dict(self):
        return dict(
            item_name=self.item_name,
            item_id=self.item_id,
            item_search_name=self.item_search_name,
            image_url=self.image_url
        )
