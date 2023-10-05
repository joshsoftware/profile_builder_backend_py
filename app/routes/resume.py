import logging
import sys, os
from datetime import datetime
from marshmallow import ValidationError
from flask import Blueprint, jsonify, request
from app.models import (
    db,
    UserModel,
    ProjectModel,
    EducationModel,
    ExperienceModel,
    UserProfileModel,
    UserSchema,
    ProjectSchema,
    UserProfileSchema,
    EducationSchema,
    ExperienceSchema,
    UserSkill,
    SkillsModel,
)
from app.utils.helpers import (
    fetch_all_existing_skills,
    add_skills_to_db,
    fetch_admin_user,
    profile_meta_data,
)

resume_blueprint = Blueprint("resume", __name__)


@resume_blueprint.route("/", methods=["POST"])
def store_resume():
    """POST API for storing profile details"""
    try:
        skills = None
        try:
            request_data = request.json
            profile_data = request_data["Basic Info"]["details"]
            certifications = request_data.get("Certification").get("points")
            project_data = request_data["Projects"]["details"]
            education_data = request_data["Education"]["details"]
            skills = request_data["Skills"]["points"]  # array
            experience_data = request_data["Experience"]["details"]  # array

        except (KeyError, AttributeError) as err:
            logging.info(
                "POST request to generate resume failed due to invalid json format"
            )
            return jsonify({"error": "Invalid request JSON"}), 400

        if certifications:
            profile_data["certifications"] = "\n".join(
                certification for certification in certifications
            )

        if skills:
            available_skills = fetch_all_existing_skills()
            available_skills = set(skill.skill for skill in available_skills)
            skills = set(skills)
            status = add_skills_to_db(skills.difference(available_skills))
            if "error" in status:
                logging.info(
                    "POST request to generate resume failed due to error in skill adding"
                )
                return jsonify({"error": status})

        user = fetch_admin_user()
        profile_data["created_by"] = user.uuid

        try:
            profile_data = UserProfileSchema().load(profile_data)
        except ValidationError as err:
            logging.info(
                f"POST request to create resume failed due to the following error:{err}"
            )
            return jsonify({"error": str(err)}), 400

        try:
            user_profile = UserProfileModel(profile_data)
            user_profile.save()
        except Exception as err:
            logging.info(
                f"POST request to create resume failed due to the following error:{err}"
            )
            return jsonify({"error": str(err)}), 400

        user_profile_id = user_profile.uuid

        try:
            for project in project_data:
                project["user_profile_id"] = user_profile_id
                project["name"] = project["projectName"]
                project["roles_and_resp"] = "\n".join(
                    point for point in project["points"]
                )
                project["project_tech"] = project["technology"]
                project["tech_worked_on"] = project["workedProjectTech"]
                start_year, start_month = map(
                    int, project["projectStartDate"].split("-")
                )
                end_year, end_month = map(int, project["projectEndDate"].split("-"))
                project["start_date"] = (
                    datetime(start_year, start_month, 1).date().isoformat()
                )
                project["end_date"] = (
                    datetime(end_year, end_month, 1).date().isoformat()
                )
                project["duration"] = project["projectDuration"]
                del project["points"]
                del project["technology"]
                del project["workedProjectTech"]
                del project["projectName"]
                del project["projectStartDate"]
                del project["projectEndDate"]
                del project["projectDuration"]
                # print(project)
                project = ProjectSchema().load(project)

        except ValidationError as err:
            user_profile.delete()
            return jsonify({"error": str(err)}), 400

        try:
            for education in education_data:
                education["user_profile_id"] = user_profile_id
                education["university_name"] = education["college"]
                education["education_degree"] = education["educationTitle"]
                education["passout_year"] = (
                    datetime(int(education["passOutDate"]), 1, 1).date().isoformat()
                )  # year
                education["grade_cum_percentage"] = education["grade"]
                del education["college"]
                del education["educationTitle"]
                del education["passOutDate"]
                del education["grade"]
                education = EducationSchema().load(education)
        except ValidationError as err:
            user_profile.delete()
            return jsonify({"error": str(err)}), 400

        if experience_data:
            try:
                for experience in experience_data:
                    start_year, start_month = map(
                        int, experience["startDate"].split("-")
                    )
                    end_year, end_month = map(int, experience["endDate"].split("-"))
                    experience["user_profile_id"] = user_profile_id
                    experience["designation"] = experience["role"]
                    experience["organization_name"] = experience["companyName"]
                    experience["start_date"] = (
                        datetime(start_year, start_month, 1).date().isoformat()
                    )
                    experience["end_date"] = (
                        datetime(end_year, end_month, 1).date().isoformat()
                    )
                    del experience["role"]
                    del experience["companyName"]
                    del experience["startDate"]
                    del experience["endDate"]
                    experience = ExperienceSchema().load(experience)
            except ValidationError as err:
                user_profile.delete()
                return jsonify({"error": str(err)}), 400

        try:
            experience = None
            for project in project_data:
                project = ProjectModel(project)
                project.save()

            for education in education_data:
                print("\n\n THIS IS EDUCATION \n", education, "\n\n")
                education = EducationModel(education)
                education.save()

            if experience_data:
                for experience in experience_data:
                    experience = ExperienceModel(experience)
                    education.save()

        except Exception as err:
            logging.info(
                f"POST request to create resume failed due to the following error:{err}"
            )
            return jsonify({"error": err}), 400

        for skill in skills:
            skill_id = SkillsModel.query.filter_by(skill=skill).first().uuid
            user_skill = UserSkill(user_profile_id=user_profile_id, skill_id=skill_id)
            db.session.add(user_skill)

        db.session.commit()

        return jsonify({"message": "resume stored successfully"}), 200
    except Exception as err:
        if user_profile:
            user_profile.delete()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"Error type->{exc_type}, file-> {fname}, line no:{exc_tb.tb_lineno}")
        return jsonify({"error": str(err)}), 400


@resume_blueprint.route("/", methods=["GET"])
@resume_blueprint.route("/<string:id>", methods=["GET"])
def fetch_profiles(profile_id=""):
    try:
        if profile_id:
            user_profile = UserProfileModel.get_user_profile_by_id(profile_id)
            user_profile_meta_data = profile_meta_data(user_profile["uuid"])
            return jsonify({"data": user_profile_meta_data}), 200

        request_data = request.args.get("email")
        user_profile = UserProfileModel.get_user_profile_by_email(request_data)
        user_profile_meta_data = profile_meta_data(user_profile["uuid"])
        return jsonify({"data": user_profile_meta_data}), 200

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"Error type->{exc_type}, file-> {fname}, line no:{exc_tb.tb_lineno}")
        return jsonify({"error": str(err)}), 400
