from app import db

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    payment_date = db.Column(db.DateTime)
    valid_thru = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id" : self.user_id,
            "program_id": self.program_id,
            "payment_date": self.payment_date,
            "valid_thru": self.valid_thru
        }