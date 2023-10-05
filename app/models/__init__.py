from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user_model import UserModel, UserSchema
from .user_profile_model import UserProfileModel, UserProfileSchema
from .user_projects_model import ProjectModel, ProjectSchema
from .education_model import EducationModel, EducationSchema
from .experience_model import ExperienceModel, ExperienceSchema
from .skills_model import SkillsModel, UserSkill