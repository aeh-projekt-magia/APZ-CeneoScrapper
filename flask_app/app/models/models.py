from app.extensions import db


##class Product(db.Model):
##    id = db.Column(db.Integer, primary_key=True)
##   product_id = db.Column(db.Text)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Text)
    author = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    stars = db.Column(db.Text)
    content = db.Column(db.Text)
    publish_date = db.Column(db.Text)
    purchase_date = db.Column(db.Text)
    useful = db.Column(db.Text)
    useless = db.Column(db.Text)
    pros = db.Column(db.Text)
    cons = db.Column(db.Text)
    review_id = db.Column(db.Text)

    def __repr__(self):
        return f'<Review no {self.review_id}: {self.author} - {self.content}>'
