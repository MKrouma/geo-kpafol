import hashlib
from uuid import uuid4
from app.cores import db, login
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # user general attributs
    user_id = db.Column(db.String(), primary_key=True, default=lambda: str(uuid4()), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    is_actived = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now)
    avatar_url = db.Column(db.String(100), default='')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        # init avatar
        if self.avatar_url is None:
            self.avatar_url = self.gravatar()

    def __repr__(self):
        return f'<User {self.email}>'
    
    def get_id(self):
        return str(self.user_id)

    @classmethod
    def get_by_id(user_model, user_id):
        return user_model.query.get_or_404(user_id)
    
    @classmethod
    def get_user_by_email(user_model, email):
        return user_model.query.filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.is_actived = False
        db.session.add(self)
        db.session.commit()

    def ping(self):
        self.updated_at = datetime.now()
        self.save()


    # user password
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    # user avatar
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, is_secured=True, size=100, default='identicon', rating='g'):
        if is_secured:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'https://www.gravatar.com/avatar'

        hash = self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
    

    def to_dict(self, sensible=False):
        data = {
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'last_seen': self.updated_at.replace(
                tzinfo=timezone.utc).isoformat(),
            'is_actived': self.is_actived,
            '_links': {
                'avatar': self.avatar_url
            }
        }

        if sensible:
            data['password'] = self.password_hash

        return data