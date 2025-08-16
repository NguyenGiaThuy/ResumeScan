from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class SectionComparer(BaseModel):
    """Always use this model to structure your response to the user."""
    section_items: str = Field(default="{}", description="A json with soft items as keys, and flags as values to indicate JD matching.")


class ResumeComparer(BaseModel):
    """Always use this model to structure your response to the user."""
    profile_summary: Optional[str] = Field(default="", description="A brief profile summary mentioned by the applicant.")
    hard_skills: Dict[str, int] = Field(default={}, description="Hard skills in resume → match against required/optional hard skills in JD.")
    soft_skills: Dict[str, int] = Field(default={}, description="Soft skills in resume → match against required/optional soft skills in JD.")
    work_experiences: Dict[str, int] = Field(default={}, description="Work experiences in resume → match against required/optional work experiences in JD.")
    educations: Dict[str, int] = Field(default={}, description="Educations in resume → match against required/optional educations in JD.")
    years_of_experience: int = Field(default=0, description="Total years of experience evaluated from work experiences of the applicant.")
    certifications: Dict[str, int] = Field(default={}, description="A list of certifications in resume → match against required/optional hard skills in JD.")
    projects: List[str] = Field(
        default=[],
        description=
        """
        A list of personal projects EXPLICITLY mentioned by the applicant
        (which mean they are not related to industrial experience).
        If work experience is not available or less than 1 year, this field is required.
        Otherwise, leave it empty. Do not guess or infer.
        """
    )
