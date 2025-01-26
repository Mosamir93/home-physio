from .base_model import BaseModel, db


class Availability(BaseModel):
    """Availability of the physiotherapists to be booked at."""
    __tablename__ = 'availability'
    id = db.Column(db.Integer, primary_key=True)
    physiotherapist_id = db.Column(db.Integer, db.ForeignKey('physiotherapists.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
