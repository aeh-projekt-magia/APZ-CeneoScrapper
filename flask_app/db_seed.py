from flask.cli import FlaskGroup
import pytest
from app import create_app, db
from app.models.UserModel import User
from app.models.ItemModel import Item
from app.models.PriceHistoryModel import PriceHistory

import datetime

import csv
def get_example_data():
    with open("electronics_dataset.csv", 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        line_count = 0
        
        result =[]

        for row in csv_reader:
            if line_count == 0:
                line_count +=1
            else:
                result.append(row)
                line_count+=1
        return result

def towar():
    """Add some towar to database"""
    new_data = get_example_data()

    new_product_list = list()  
    for item in new_data:
        new_product = Item(
            name=item["name"],
            category="Smartphone",
            # price= float(item["actual_price"][1:]
            #     .replace(',','')),
            price = (lambda x: float(x.replace(",", "")) if x != "" else float(0))(item["actual_price"][1:]),
            available_shops_count="Available in 50 shops",
            reviews_count=item["no_of_ratings"],
            description="Description...",
            image_url=item["image"],
        )
        new_product_list.append(new_product)




    user = User.query.filter_by(id=1).first()
    new_product = Item(
        name="Iphone 17",
        category="Smartphone",
        price="5000 zł",
        available_shops_count="Available in 50 shops",
        reviews_count="12 reviews",
        description="Smartfon Apple z ekranem 6,1 cala, wyświetlacz OLED.\
             Aparat 12 Mpix, pamięć 4 GB RAM. Obsługuje sieć: 5G",
        image_url="https://image.ceneostatic.pl/data/products/115107321/i-apple-iphone-14-128gb-polnoc.jpg",
    )

    new_price_history = []
    for index, x in enumerate(range(25)):
        new_price_history.append(
            PriceHistory(
                item=new_product,
                price=6000 - index * 200,
                date=datetime.datetime.now() - datetime.timedelta(days=index),
            )
        )

    user.subscriptions.append(new_product)

    try:
        db.session.add(new_product)
        db.session.add_all(new_price_history)
        db.session.add_all(new_product_list)
        db.session.commit()
    except Exception:
        db.session.rollback()