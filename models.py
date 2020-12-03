from .app import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carplate = db.Column(db.String(10), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    tempcarplate = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.firstname} {self.lastname}>"


class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"


# class Calendar(db.Model):
#     pass


# class Guest(db.Model):
#     pass


# class ParkingSpot(db.Model):
#     pass


# class Reservation(db.Model):
#     pass


# class Staff(db.Model):
#     pass

# create tables
db.create_all()
db.session.commit()
