from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    fullname= db.Column(db.String(255))
    bio = db.Column(db.String(1000))
    profile_pic_path = db.Column(db.String)
    pass_secure = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    reviews = db.relationship('Review',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'


class Pitch(db.Model):
    __tablename__ = "pitches"

    id = db.Column(db.Integer,primary_key = True)
    p_title = db.Column(db.String)
    p_body = db.Column(db.String(1000))
    category = db.Column(db.String)
    posted_date = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    upvote = db.Column(db.Integer)
    downvote = db.Column(db.Integer)
    reviews = db.relationship('Review',backref = 'p_id',lazy = "dynamic")


    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls,category):
        pitches = Pitch.query.filter_by(category=category).all()
        return pitches

    @classmethod
    def get_pitch(cls,id):
        pitch = Pitch.query.filter_by(id=id).first()

        return pitch
    @classmethod
    def count_pitches(cls,uname):

        user = User.query.filter_by(username=uname).first()
        pitches = Pitch.query.filter_by(user_id=user.id).all()


        pitches_count = 0
        for pitch in pitches:
            pitches_count += 1

        return pitches_count

class Review(db.Model):

    __tablename__ = 'reviews'
    id = db.Column(db.Integer,primary_key = True)
    review = db.Column(db.String(500))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pitch = db.Column(db.Integer,db.ForeignKey("pitches.id"))

  

    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_reviews(cls,pitch):
        reviews = Review.query.filter_by(p_id=pitch).all()
        return reviews


