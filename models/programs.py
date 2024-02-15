from app import db

class Programs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer)
    description = db.Column(db.Integer)
    # Student can only attend lessons on his time interval
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    subs = db.relationship('subscription', backref='programs', lazy=True)
    attendance = db.relationship('attendance', backref='programs', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time
        }