# from sqlalchemy import Column, String

# from app.extensions import db


# # user_product_subscription2 = db.Table(
# #     "user_product_subscription2",
# #     Column("user_id", Integer, ForeignKey("users.id")),
# #     Column("product_id", Integer, ForeignKey("products_table.id")),
# # )


# class Products(db.Model):
#     __tablename__ = "products_table"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     category = Column(String)
#     price = Column(String)
#     available_shops_count = Column(String)
#     reviews_count = Column(String)
#     description = Column(String)
#     image_url = Column(String)

#     # children = relationship('Reviews', back_populates='parent')

#     # subscribers = relationship(
#     #     "User", secondary=user_product_subscription2, back_populates="subscriptions"
#     # )

#     def __repr__(self):
#         return f"<id {self.id}> <name {self.name}> <subscribers {self.name}>"
