from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
from app import create_app, db
from app.models.UserModel import User
from app.models.ItemModel import Item
from config import TestingConfig

app = create_app()
app_context = app.app_context()
app_context.push()
db.create_all()

user = User.query.first()
item = Item(
    name="Iphone 14",
    category="Smartphone",
    price="90000 zł",
    available_shops_count="Available in 50 shops",
    reviews_count="12 reviews",
    description="Smartfon Apple z ekranem 6,1 cala, wyświetlacz OLED. Aparat 12 Mpix, pamięć 4 GB RAM. Obsługuje sieć: 5G",
    image_url="https://image.ceneostatic.pl/data/products/115107321/i-apple-iphone-14-128gb-polnoc.jpg",
)
try:
    db.session.add(item)
    db.session.commit()
except:
    db.session.rollback()