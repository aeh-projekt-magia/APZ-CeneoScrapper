from typing import List

from app.models.PriceHistoryModel import PriceHistory
from app.extensions import db
from sqlalchemy import select
from app.models import PriceHistoryModel
from app.repository.price_history.price_history_repository import PriceHistoryRepository


class ImplPriceHistoryRepository(PriceHistoryRepository):
    def add_price_history(self, price_history: PriceHistoryModel):
        db.session.add(price_history)
        db.session.commit()

    def get_price_history_by_id(self, price_hist_id):
        price_hist = db.session.execute(
            db.select(PriceHistory).filter_by(price_id=id)
        ).scalar_one()
        return price_hist

    def get_n_latest_price_history_records(
        self, item_id: str, n: int
    ) -> List[PriceHistory]:
        price_hist_list = db.session.execute(
            select(PriceHistory)
            .filter_by(item_id=item_id)
            .order_by(PriceHistory.date)
            .limit(n)
        )
        return price_hist_list

    def get_all_price_history(self):
        records = db.session.execute(db.select(PriceHistory)).scalars()
        return records

    def delete_price_history_by_id(self, price_hist_id: str):
        record = db.session.execute(
            db.select(PriceHistory).filter_by(price_id=id)
        ).scalar_one()
        db.session.delete(record)
        db.session.commit()

    def delete_all_price_history(self):
        db.session.query(PriceHistory).delete()
        db.session.commit()
