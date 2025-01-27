from .base_model import BaseModel, db


class Patient(BaseModel):
    """Patient class which will contains
    the patient's or the user's info."""
    __tablename__ = 'patients'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    google_id = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128))


    @classmethod
    def from_google(cls, google_data):
        return cls(
            first_name=google_data["given_name"],
            last_name=google_data["family_name"],
            email=google_data["email"],
            google_id=google_data["sub"],
            role='patient',
        )
