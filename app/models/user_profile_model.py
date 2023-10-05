import uuid
from datetime import datetime
from marshmallow import fields, Schema
from app.models import db


class UserProfileModel(db.Model):
    """
    User profile model to store basic info
    of person for whom the profile is being generated
    """

    __tablename__ = "user_profile"

    uuid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    designation = db.Column(db.String, nullable=False)
    profile_name = db.Column(db.String, nullable=False)
    experience = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(6))
    profile_details = db.Column(db.Text)
    certifications = db.Column(db.Text) # array of strings are entered with line breaks
    is_external = db.Column(db.Boolean)
    created_by = db.Column(db.String, db.ForeignKey("users.uuid", ondelete="SET NULL"))
    created_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.uuid = str(uuid.uuid4())
        self.name = data.get("name")
        self.email = data.get("email")
        self.designation = data.get("designation")
        self.profile_name = ((data.get("name")) + "_" + data.get("designation").lower().replace(" ","_")).lower().replace(" ","_")
        self.experience = data.get("experience")
        self.gender = data.get("gender")
        self.profile_details = data.get("profile_details")
        self.is_external = data.get("is_external") or False
        self.certifications = data.get("certifications")
        self.created_by = data.get("created_by")
        self.created_at = datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def fetch_all_user_profiles():
        return UserProfileModel.query.all()

    @staticmethod
    def get_user_profile_by_id(user_profile_id):
        return UserProfileSchema().dump(UserProfileModel.query.filter_by(uuid=user_profile_id).first())
    
    @staticmethod
    def get_user_profile_by_email(email):
        return UserProfileSchema().dump(UserProfileModel.query.filter_by(email=email).first())

class UserProfileSchema(Schema):
    """
    Schema for User profile model
    """
    uuid = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    designation = fields.Str(required=True)
    profile_name = fields.Str()
    experience = fields.Float(required=True)
    gender = fields.Str(required=True)
    profile_details = fields.Str(required=True)
    is_external = fields.Bool(required=True)
    certifications = fields.Str()
    created_by = fields.Str()
    created_at = fields.DateTime()

