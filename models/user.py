from app import db
from models.userrole import UserRole
from models.attendance import Attendance
from models.subscription import Subscription

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable = False)
    surname = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80), nullable = False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)
    # Define a one-to-many relationship with the Post model
    subs = db.relationship(Subscription, backref='user', lazy=True)
    attendance = db.relationship(Attendance, backref='user', lazy=True)

    def is_valid(self):
        return all([self.username, self.firstname, self.surname, self.email, self.password])
    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "surname": self.surname,
            "age": self.age,
            "role": self.role,
            "email": self.email
        }