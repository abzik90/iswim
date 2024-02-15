from app import db

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    visit_date = db.Column(db.DateTime)
    exit_date = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id" : self.user_id,
            "program_id": self.program_id,
            "visit_date": self.visit_date,
            "exit_date": self.exit_date
        }