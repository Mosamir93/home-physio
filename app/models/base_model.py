from datetime import datetime
from .. import db


class BaseModel(db.model):
    """BaseModel class that will be used as a
    parent class in all the other classes."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
