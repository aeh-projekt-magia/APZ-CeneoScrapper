from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column
from flask_login import UserMixin

from app import db

class Review(db.Model):
    __tablename__ = "reviews"    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    stars = Column(String)
    description = Column(String)
    zalety = Column(String)
    wady = Column(String)
    recommendation = Column(String)
    date = Column(String)

    # parent_id = mapped_column(ForeignKey('products_table.id'))
    # parent = relationship('Products', back_populates='children')

    def __init__(self,name,stars, description, zalety : list, wady :list, recommendation, date, parent_id = None, parent = None) -> None:
        self.name = name
        self.stars = stars
        self.description = description
        self.zalety = ';'.join(zalety)
        self.wady = ';'.join(wady)
        self.reccomendation = recommendation
        self.date = date
        self.parent_id = parent_id
        self.parent = parent

    def __repr__(self):
        return f'{self.id} {self.name} {self.stars}'