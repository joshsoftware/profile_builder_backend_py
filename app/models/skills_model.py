import uuid
from typing import Dict
from app.models import db

skill_tags = db.Table(
    "user_skills",
    db.Model.metadata,
    db.Column(
        "user_profile_id",
        db.ForeignKey("user_profile.uuid", ondelete="CASCADE"),
        primary_key=True
    ),
    db.Column(
        "skill_id",
        db.ForeignKey("skills.uuid", ondelete="CASCADE"),
        primary_key=True
    )
)



class SkillsModel(db.Model):
    """
    Skills model to store the skills
    which have been logged by the users
    """

    __tablename__ = "skills"

    uuid = db.Column(db.String, primary_key=True)
    skill = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, data: Dict) -> None:
        self.uuid = str(uuid.uuid4())
        self.skill = data.get("skill")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class UserSkill(db.Model):
    __table__ = skill_tags
