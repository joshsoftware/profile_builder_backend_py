import uuid
from datetime import datetime
from marshmallow import fields, Schema
from app.models import db


class ProjectModel(db.Model):
    """Flask-SqlALchmey Model class for projects for whom the project is being created"""

    __tablename__ = "projects"

    uuid = db.Column(db.String, primary_key=True)
    user_profile_id = db.Column(db.String, db.ForeignKey("user_profile.uuid",ondelete="CASCADE"))
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)  # requires datetime.date object
    end_date = db.Column(db.Date)
    duration = db.Column(db.String(50))
    overview = db.Column(db.Text)
    roles_and_resp = db.Column(db.Text)
    project_tech = db.Column(db.String, nullable=False)
    tech_worked_on = db.Column(db.String, nullable=False)

    def __init__(self, data) -> None:
        self.uuid = str(uuid.uuid4())
        self.user_profile_id = data.get("user_profile_id")
        self.name = data.get("name")
        self.start_date = data.get("start_date")
        self.end_date = data.get("end_date")
        self.overview = data.get("overview")
        self.duration = data.get("duration")
        self.roles_and_resp = data.get("roles_and_resp")
        self.project_tech = data.get("project_tech")
        self.tech_worked_on = data.get("tech_worked_on")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def fetch_projects_by_user_profile(user_profile_id):
        return ProjectSchema().dump(ProjectModel.query.filter_by(user_profile_id=user_profile_id), many=True)

class ProjectSchema(Schema):
    uuid = fields.Str(dump_only=True)
    user_profile_id = fields.Str(required=True)
    name = fields.Str(required=True)
    start_date = fields.Date()
    end_date = fields.Date()
    duration = fields.Str()
    overview = fields.Str(required=True)
    roles_and_resp = fields.Str(required=True)
    project_tech = fields.Str(required=True)
    tech_worked_on = fields.Str(required=True)