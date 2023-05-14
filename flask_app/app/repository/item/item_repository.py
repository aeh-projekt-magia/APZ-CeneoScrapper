from abc import ABC, abstractmethod
from typing import List

from app.models.ItemModel import Item
from app.repository.base_repository import BaseRepository


class ItemRepository(BaseRepository, ABC):
    @abstractmethod
    def add_item(self, item: Item):
        ...

    @abstractmethod
    def get_item_by_id(self, item_id: str) -> Item:
        ...

    @abstractmethod
    def get_item_by_name(self, name: str) -> Item:
        ...

    @abstractmethod
    def get_items_by_name_contains(self, name: str) -> List[Item]:
        ...

    @abstractmethod
    def get_all_items_paginate(self, page, pages: int):
        ...

    @abstractmethod
    def get_all_items(self) -> List[Item]:
        ...

    @abstractmethod
    def delete_item_by_id(self, item_id: str):
        ...

    @abstractmethod
    def delete_all_items(self):
        ...

    @abstractmethod
    def update_item(self, item: Item) -> Item:
        ...
