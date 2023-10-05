import uuid
from typing import Dict
from marshmallow import fields, Schema
from app.models import db


class EducationModel(db.Model):
    """Education Model to store the
    education details for whom the resume is being created
    """

    __tablename__ = "education"

    uuid = db.Column(db.String, primary_key=True)
    user_profile_id = db.Column(db.String, db.ForeignKey("user_profile.uuid", ondelete="CASCADE"))
    education_degree = db.Column(db.String, nullable=False)
    university_name = db.Column(db.String, nullable=False)
    grade_cum_percentage = db.Column(db.String, nullable=False)
    passout_year = db.Column(db.Date, nullable=False)

    def __init__(self, data: Dict) -> None:
        self.uuid = str(uuid.uuid4())
        self.user_profile_id = data.get("user_profile_id")
        self.education_degree = data.get("education_degree")
        self.university_name = data.get("university_name")
        self.grade_cum_percentage = data.get("grade_cum_percentage")
        self.passout_year = data.get("passout_year")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def fetch_education_by_user_profile(user_profile_id):
        return EducationSchema().dump(EducationModel.query.filter_by(user_profile_id=user_profile_id), many=True)


class EducationSchema(Schema):
    """
    Education model schema
    """

    uuid = fields.Str(dump_only=True)
    user_profile_id = fields.Str()
    education_degree = fields.Str(required=True)
    university_name = fields.Str(required=True)
    grade_cum_percentage = fields.Str(required=True)
    passout_year = fields.Date()
