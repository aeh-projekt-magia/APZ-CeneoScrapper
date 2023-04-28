from app.models.ItemModel import Item


class ProductService:
    @staticmethod
    def get_all_products_to_show():
        return Item.query.all()

    @staticmethod
    def get_product_to_show_by_id(id):
        return Item.query.where(Item.id == id).first()
