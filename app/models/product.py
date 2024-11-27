from datetime import datetime

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class InventoryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    entry_type = db.Column(db.String(10), nullable=False)  # 'in' or 'out'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref=db.backref('inventory_entries', lazy=True))

    @property
    def status(self):
        today = datetime.utcnow()
        if self.expiration_date < today:
            return "vencido"
        elif self.expiration_date <= today + relativedelta(days=3):
            return "por_vencer"
        return "vigente"