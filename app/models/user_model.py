import uuid
from datetime import datetime
from marshmallow import fields, Schema
from app.models import db


class UserModel(db.Model):
    """User model for the system"""

    __tablename__ = "users"

    uuid = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50))
    oauth_token = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean)

    def __init__(self, data):
        """constructor for object creation

        :param data: dictionary containing Usermodel class fields
        :type data: dict
        """
        self.uuid = str(uuid.uuid4())
        self.email = data.get("email")
        self.oauth_token = data.get("oauth_token")
        self.password = data.get("password")
        self.created_at = datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def fetch_super_admin():
        return UserModel.query.filter_by(email="admin@joshsoftware.com")

class UserSchema(Schema):
    """
    User Model Schema
    """
    uuid = fields.Str(dump_only=True)
    email = fields.Email()
    password = fields.Str()
    oauth_token = fields.Str(required=True)
    created_at = fields.DateTime()
