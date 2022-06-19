from datetime import datetime
from xml.dom import ValidationErr
from flask import jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from dataclasses import dataclass
from sqlalchemy import false, true
from werkzeug.security import generate_password_hash, check_password_hash
from App import db, app

@dataclass
class User(db.Model, UserMixin):
    id : int = db.Column(db.Integer, primary_key = True)
    email : str = db.Column(db.String(150), unique = True, nullable = False)
    username : str = db.Column(db.String(50), unique = True, nullable = False)
    password : str = db.Column(db.String(150), nullable = False)
    image_file : str = db.Column(db.String(30), nullable = False, default = 'default.jpg')
    general_information : str = db.Column(db.String(200), nullable = True)

    def get_reset_token(self, expires_sec=300):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def set_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length = 32)


    def check_password(self, password):
        return check_password_hash(self.password, password)


    def past_passwrod_check(self, password):
        if(check_password_hash(self.password, password)):
            raise ValidationErr('Sorry, but your previous password is the same as your current one, please try again')


@dataclass
class NFT(db.Model):
    id : int = db.Column(db.Integer, primary_key = True)
    productImage : str = db.Column(db.String(50), nullable = True)
    productName : str = db.Column(db.String(50), nullable = False, unique = True)
    description : str = db.Column(db.Text, nullable = False)
    price : float = db.Column(db.Float(30), nullable = False)
    date_creator : int = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    authorName_id : int = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    ownerName_id : int = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    authorName = db.relationship("User", foreign_keys = [authorName_id], backref = 'creator', lazy = True)
    ownerName = db.relationship("User", foreign_keys = [ownerName_id], backref = 'owner', lazy = True)

