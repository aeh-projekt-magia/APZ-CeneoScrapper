import datetime
from typing import Tuple

from app.models.PriceHistoryModel import PriceHistory
from app.repository.price_history.price_history_repository import PriceHistoryRepository
from app.services.item.item_service import ItemService
from app.services.price_history.price_history_missing_exception import PriceHistoryMissingException


class PriceHistoryService:
    def __init__(
            self,
            price_history_repository: PriceHistoryRepository,
            item_service: ItemService,
            date_format: str = "%d-%m-%Y",
            currency: str = "PLN",
    ):
        self.price_history_repository = price_history_repository
        self.item_service = item_service
        self.date_format = date_format
        self.currency = currency

    def create_price_history(
            self,
            price: float,
            date: datetime.datetime,
            item_id: str
    ):
        price_hist = PriceHistory(
            price=price,
            date=date,
            item_id=item_id,
        )
        self.price_history_repository.add_price_history(price_hist)

    def get_latest_price_history(self, item_id: str) -> PriceHistory:
        latest = self.price_history_repository.get_n_latest_price_history_records(
            item_id=item_id,
            n=1
        )
        if not latest:
            raise PriceHistoryMissingException(
                "No Price History records are available for this item"
            )

        return latest[0]

    def compare_two_latest(self, item_id) -> Tuple[str, bool]:
        latest = self.price_history_repository.get_n_latest_price_history_records(
            item_id=item_id,
            n=2
        )
        if not latest:
            raise PriceHistoryMissingException(
                "No Price History records are available for this item."
            )
        elif len(latest) == 1:
            # only one record found - print one
            return self.single_price_history_summary(latest[0]), True

        return self.comparison_summary(*latest)

    def comparison_summary(
            self,
            price_hist_a: PriceHistory,
            price_hist_b: PriceHistory
    ) -> Tuple[str, bool]:
        if price_hist_a.item_id != price_hist_b.item_id:
            raise PriceHistoryMissingException(
                "Cannot compare price history of different items"
            )

        item = self.item_service.get_item_by_id(price_hist_a.item_id)

        if price_hist_a.date > price_hist_b.date:
            # swap so that price_hist_a is the older one
            price_hist_a, price_hist_b = price_hist_b, price_hist_a

        price_difference = price_hist_b.price - price_hist_a.price
        has_changed = price_difference != 0
        price_difference = "{0:.2f}".format(price_difference)

        summary = f"{item.name}:\t" \
                  f"{self._price_hist_date_and_price(price_hist_a)}" \
                  f"\t->\t" \
                  f"{self._price_hist_date_and_price(price_hist_b)}" \
                  f"\tTotal price change: {price_difference} {self.currency}"
        return summary, has_changed

    def single_price_history_summary(self, price_hist: PriceHistory) -> str:
        item = self.item_service.get_item_by_id(price_hist.item_id)
        summary = f"{item.name}:\t" \
                  f"({self._price_hist_date_and_price(price_hist)}"
        return summary

    def _price_hist_date_and_price(self, price_hist: PriceHistory):
        price_formatted = "{0:.2f}".format(price_hist.price)
        return f"({datetime.datetime.strftime(price_hist.date, self.date_format)})" \
               f" {price_formatted} {self.currency}"
