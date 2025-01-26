from .base_model import BaseModel, db


class Physiotherapists(BaseModel):
    """Physiotherapists is the class that
    will contain the physiotherapist info."""
    __tablename__ = 'physiotherapists'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    google_id = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(20), nullable=False)


    @classmethod
    def from_google(cls, google_data):
        return cls(
            first_name=google_data["given_name"],
            last_name=google_data["family_name"],
            email=google_data["email"],
            google_id=google_data["sub"],
            location="",
            rating=0.0,
            role="physiotherapist"
        )
