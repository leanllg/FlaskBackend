from main.models import db

class Location(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    longtitude = db.Column(db.Numeric(10, 6), nullable=False)
    latitude = db.Column(db.Numeric(10, 6), nullable=False)
    detail = db.Column(db.Text(), nullable=True)

    def __init__(self, user_id, longtitude, latitude, detail=None):
        self.user_id = user_id
        self.longtitude = longtitude
        self.latitude = latitude
        self.detail = detail

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def to_json(self):
        json_location = {
            'longtitude': self.longtitude,
            'latitude': self.latitude,
            'detail': self.detail
        }
        return json_location
