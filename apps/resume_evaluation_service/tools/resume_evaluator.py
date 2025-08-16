from langchain_core.tools import tool
from common_modules.schemas.jd import JD
from common_modules.schemas.resume_comparer import ResumeComparer


@tool("resume_evaluator", description="Evaluate resume based on JD requirements")
def resume_evaluator(jd: JD, resume_comparer: ResumeComparer) -> float:
    # TODO: Export these base weights to a linear regression model to store in DB (for future feedback loop)
    # TODO: Handle overqualified candidate

    # Avoid division by zero
    def safe_div(x, y): return x / y if y else 0

    # Required weights
    required_hard_skills_base_weight = 0.3
    required_soft_skills_base_weight = 0.1
    required_work_experiences_base_weight = 0.45
    required_educations_base_weight = 0.1
    required_years_of_experience_base_weight = 0.05

    # Optional weights
    optional_hard_skills_base_weight = 0.06
    optional_soft_skills_base_weight = 0.02
    optional_work_experiences_base_weight = 0.1
    optional_educations_base_weight = 0.02

    required_hard_skill_points = safe_div(required_hard_skills_base_weight, len(jd.required_hard_skills))
    required_soft_skill_points = safe_div(required_soft_skills_base_weight, len(jd.required_soft_skills))
    required_work_experience_points = safe_div(required_work_experiences_base_weight, len(jd.required_work_experiences))
    required_education_points = safe_div(required_educations_base_weight, len(jd.required_educations))
    required_year_of_experience_points = safe_div(required_years_of_experience_base_weight, jd.required_years_of_experience)

    optional_hard_skill_points = safe_div(optional_hard_skills_base_weight, len(jd.optional_hard_skills))
    optional_soft_skill_points = safe_div(optional_soft_skills_base_weight, len(jd.optional_soft_skills))
    optional_work_experience_points = safe_div(optional_work_experiences_base_weight, len(jd.optional_work_experiences))
    optional_education_points = safe_div(optional_educations_base_weight, len(jd.optional_educations))

    # Hard skills
    hard_skills_points = 0
    for flag in resume_comparer.hard_skills.values():
        required_exists = 1 if flag == 1 else 0
        optional_exists = 1 if flag == 0 else 0
        hard_skills_points += (
            required_exists * required_hard_skill_points +
            optional_exists * optional_hard_skill_points
        )

    # Soft skills
    soft_skills_points = 0
    for flag in resume_comparer.soft_skills.values():
        required_exists = 1 if flag == 1 else 0
        optional_exists = 1 if flag == 0 else 0
        soft_skills_points += (
            required_exists * required_soft_skill_points +
            optional_exists * optional_soft_skill_points
        )

    # Work experiences
    work_experiences_points = 0
    for flag in resume_comparer.work_experiences.values():
        required_exists = 1 if flag == 1 else 0
        optional_exists = 1 if flag == 0 else 0
        work_experiences_points += (
            required_exists * required_work_experience_points +
            optional_exists * optional_work_experience_points
        )

    # Education
    educations_points = 0
    for flag in resume_comparer.educations.values():
        required_exists = 1 if flag == 1 else 0
        optional_exists = 1 if flag == 0 else 0
        educations_points += (
            required_exists * required_education_points +
            optional_exists * optional_education_points
        )

    # Years of experience
    yoe_multiplier = \
        0.5 * resume_comparer.years_of_experience + resume_comparer.years_of_experience \
        if jd.required_years_of_experience < 1 and resume_comparer.years_of_experience < 1 \
        else resume_comparer.years_of_experience
    year_of_experiences_points = required_year_of_experience_points * yoe_multiplier

    # Final score
    total_score = (
        hard_skills_points +
        soft_skills_points +
        work_experiences_points +
        educations_points +
        year_of_experiences_points
    )

    return round(total_score, 4)  # Keep score as percentage weight sum
