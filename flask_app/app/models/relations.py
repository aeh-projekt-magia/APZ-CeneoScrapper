from sqlalchemy import Column, ForeignKey, Integer
from app import db

user_product_subscription = db.Table(
    "user_product_subscription",
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("item_id", Integer, ForeignKey("items.id")),
)
