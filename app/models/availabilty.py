from base_model import BaseModel, db


class Availabilty(BaseModel):
    """Availability of the physiotherapists to be booked at."""
    __tablename__ = 'availability'
    physiotherapist_id = db.Column(db.Integer, db.ForeignKey('physiotherapists.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)   
