from base_model import BaseModel, db


class Patient(BaseModel):
    """Patient class which will contains
    the patient's or the user's info."""
    __tablename__ = 'patients'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    google_id = db.Column(db.String(200), nullable=True)
