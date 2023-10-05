import uuid
from typing import Dict
from marshmallow import fields, Schema
from app.models import db


class ExperienceModel(db.Model):
    """Experience model to store the experience
    related data of the person for whom the resume is being created
    """

    __tablename__ = "experience"

    uuid = db.Column(db.String, primary_key=True)
    user_profile_id = db.Column(db.String, db.ForeignKey("user_profile.uuid",ondelete="CASCADE"))
    designation = db.Column(db.String, nullable=False)
    organization_name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    def __init__(self, data: Dict) -> None:
        self.uuid = str(uuid.uuid4())
        self.user_profile_id = data.get("user_profile")
        self.designation = data.get("designation")
        self.organization_name = data.get("organization_name")
        self.start_date = data.get("start_date")
        self.end_date = data.get("end_date")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def fetch_experience_by_user_profile(user_profile_id):
        return ExperienceSchema().dump(ExperienceModel.query.filter_by(user_profile_id=user_profile_id), many=True)


class ExperienceSchema(Schema):
    """
    Schema for Experience model
    """

    uuid = fields.Str(dump_only=True)
    user_profile_id = fields.Str()
    designation = fields.Str(required=True)
    organization_name = fields.Str(required=True)
    start_date = fields.Date()
    end_date = fields.Date()