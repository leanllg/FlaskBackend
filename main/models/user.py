from main.models import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text(), nullable=False, unique=True)
    phone = db.Column(db.Text(), nullable=False)
    qq = db.Column(db.Text(), nullable=False)
    avatar = db.Column(db.Text(), nullable=False)
    love_level = db.Column(db.Numeric(), nullable=True)

    def __init__(self, password, name, phone, qq, avatar, love_level):
        self.password = password
        self.name = name
        self.phone = phone
        self.qq = qq
        self.avatar = avatar
        self.love_level = love_level

    def __repr__(self):
        return '<user id {0}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def to_json(self):
        json_user = {
            'name': self.name,
            'phone': self.phone,
            'qq': self.qq,
            'avatar': self.avatar,
            'love_level': self.love_level
        }
        return json_user
