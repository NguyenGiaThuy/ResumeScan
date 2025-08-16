from pydantic import BaseModel, Field
from typing import List, Optional
from common_modules.schemas.backgrounds import Education, Experience


class Resume(BaseModel):
    """Always use this model to structure your response to the user."""
    profile_summary: Optional[str] = Field(default="", description="A brief profile summary mentioned by the applicant. Do not guess or infer.")
    hard_skills: List[str] = Field(default=[], description="A list of hard skills EXPLICITLY mentioned by the applicant. Do not guess or infer. Ignore profile/summary text.")
    soft_skills: List[str] = Field(default=[], description="A list of the soft skills EXPLICITLY mentioned by the applicant. Do not guess or infer. Ignore profile/summary text.")
    work_experiences: List[Experience] = Field(default=[], description="A list of work experiences EXPLICITLY mentioned by the applicant. Do not guess or infer. Ignore profile/summary text.")
    educations: List[Education] = Field(default=[], description="The list of educational backgrounds EXPLICITLY mentioned by the applicant. Do not guess or infer. Ignore profile/summary text.")
    years_of_experience: int = Field(default=0, description="Total years of experience in the field if work experience is available. Otherwise, leave it zero.")
    certifications: List[str] = Field(default=[], description="A list of certifications EXPLICITLY mentioned by the applicant. Do not guess or infer. Ignore profile/summary text.")
    projects: List[str] = Field(
        default=[],
        description=
        """A list of personal projects EXPLICITLY mentioned by the applicant
        (which mean they are not related to industrial experience).
        If work experience is not available or less than 1 year, this field is required.
        Otherwise, leave it empty. Do not guess or infer. Ignore profile/summary text.
        """
    )