from base_model import BaseModel, db


class Booking(BaseModel):
    """Booking table of a certain time slot."""
    __tablename__ = 'booking'
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    physiotherapist_id = db.Column(db.Integer, db.ForeignKey('physiotherapists.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="pending")
