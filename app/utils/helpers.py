import logging
from app.models import (
    UserModel,
    UserProfileModel,
    ProjectModel,
    ExperienceModel,
    EducationModel,
    SkillsModel,
    UserSkill
)


def create_slug(inp_string: str):
    return inp_string.lower().replace(" ", "_")


def fetch_all_existing_skills():
    return SkillsModel.query.all()


def add_skills_to_db(skills):
    try:
        for skill in skills:
            skill = SkillsModel({"skill": skill})
            skill.save()
        return {"status": "success"}
    except Exception as err:
        logging.info(f"skill adding failed due to the following error:{err}")
        return {"error": err}


def fetch_admin_user() -> UserModel:
    return UserModel.query.filter_by(email="admin@joshsoftware.com").first()


def profile_meta_data(user_profile_id):
    meta_data = {}
    user_profile_data = UserProfileModel.get_user_profile_by_id(user_profile_id)
    user_project_data = ProjectModel.fetch_projects_by_user_profile(user_profile_id)
    user_education_data = EducationModel.fetch_education_by_user_profile(user_profile_id)
    user_experience_data = ExperienceModel.fetch_experience_by_user_profile(user_profile_id)
    user_skills = UserSkill.query.filter_by(user_profile_id=user_profile_id)
    user_skills = [skill.skill_id for skill in user_skills]
    user_skills = [SkillsModel.query.get(skill).skill for skill in user_skills]
    certifications = user_profile_data["certifications"].split("\n")
    del user_profile_data["certifications"]
    meta_data["Basic Info"] = {"details": user_profile_data}
    meta_data["Projects"] = {"details": user_project_data}
    meta_data["Education"] = {"details": user_education_data}
    meta_data["Experience"] = {"details": user_experience_data}
    meta_data["Certification"] = {"points": certifications}
    meta_data["Skills"] = {"points": user_skills}
    print(meta_data)
    return meta_data
