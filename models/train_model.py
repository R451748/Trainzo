from database import db

class Train(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    train_no = db.Column(
        db.String(20)
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    speed = db.Column(
        db.Integer
    )

    last_updated = db.Column(
        db.String(100)
    )

    def to_dict(self):

        return {
            'id': self.id,
            'trainNo': self.train_no,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'speed': self.speed,
            'lastUpdated': self.last_updated
        }