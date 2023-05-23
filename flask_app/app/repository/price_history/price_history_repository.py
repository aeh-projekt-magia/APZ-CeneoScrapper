from abc import ABC, abstractmethod
from typing import List

from app.models.PriceHistoryModel import PriceHistory
from app.repository.base_repository import BaseRepository


class PriceHistoryRepository(BaseRepository, ABC):
    @abstractmethod
    def add_price_history(self, price_history: PriceHistory):
        ...

    @abstractmethod
    def get_price_history_by_id(self, price_hist_id):
        ...

    @abstractmethod
    def get_n_latest_price_history_records(
        self, item_id: str, n: int
    ) -> List[PriceHistory]:
        ...

    @abstractmethod
    def get_all_price_history(self):
        ...

    @abstractmethod
    def delete_price_history_by_id(self, price_hist_id: str):
        ...

    @abstractmethod
    def delete_all_price_history(self):
        ...
