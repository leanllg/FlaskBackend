from main.models import db
from datetime import datetime

class Case(db.Model):
    __tablename__  = 'cases'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    other_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_borrow = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=datetime.now().timestamp())
    duration = db.Column(db.Interval, default=0)
    longtitude = db.Column(db.Numeric(10, 6), nullable=False)
    latitude = db.Column(db.Numeric(10, 6), nullable=False)
    description = db.Column(db.Text(), nullable=False)

    def __init__(self, user_id, other_id, is_borrow, status, sex, time, \
        duration, longtitude, latitude, description):
        self.user_id = user_id
        self.other_id = other_id
        self.is_borrow = is_borrow
        self.status = status
        self.sex = sex
        self.time = time
        self.duration = duration
        self.longtitude = longtitude
        self.latitude = latitude
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def to_json(self):
        return {
            'id': self.id,
            'is_borrow': self.is_borrow,
            'status': self.status,
            'sex': self.sex,
            'time': self.time,
            'duration': self.duration,
            'longtitude': self.longtitude,
            'latitude': self.latitude,
            'description': self.description
            }
