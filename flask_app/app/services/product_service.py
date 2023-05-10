from app.models.ItemModel import Item


class ProductService:
    @staticmethod
    def get_all_products_to_show():
        return Item.query.all()
    @staticmethod
    def get_all_products_to_show_paginate(page, pages:int):
        return Item.query.paginate(page=page ,per_page=pages)

    @staticmethod 
    def get_all_products_to_show_by_name(product_name : str):
        q = Item.query.filter(Item.name.like(f"%{product_name}%"))
        return q
    @staticmethod
    def get_product_to_show_by_id(id):
        return Item.query.where(Item.id == id).first()
