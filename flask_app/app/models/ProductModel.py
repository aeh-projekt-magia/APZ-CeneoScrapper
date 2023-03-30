from app.extensions import db

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)
    is_available = db.Column(db.Boolean)

    def __str__(self):
        return (str(self.id) + " " + self.product_id + " " + self.product_name)
