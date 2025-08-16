from pydantic import BaseModel, Field
from typing import List
from common_modules.schemas.backgrounds import Education, Experience


class JD(BaseModel):
    """Always use this model to structure your response to the user."""
    job_summary: str = Field(description="A brief summary of the job description. Do not guess or infer.")
    required_hard_skills: List[str] = Field(default=[], description="A list of required hard skills the job EXPLICITLY mentioned. Do not guess or infer. Ignore description/summary text.")
    optional_hard_skills: List[str] = Field(default=[], description="A list of optional hard skills the job EXPLICITLY mentioned. Do not guess or infer. Ignore description/summary text.")
    required_soft_skills: List[str] = Field(default=[], description="A list of required soft skills the job EXPLICITLY mentioned. Do not guess or infer. Ignore description/summary text.")
    optional_soft_skills: List[str] = Field(default=[], description="A list of optional soft skills the job EXPLICITLY mentioned. Do not guess or infer. Ignore description/summary text.")
    required_work_experiences: List[Experience] = Field(default=[], description="A list of required work experiences the job EXPLICITLY mentioned. Do not guess or infer. Ignore description/summary text.")
    optional_work_experiences: List[Experience] = Field(default=[], description="A list of optional work experiences the job EXPLICITLY mentioned. Do not guess or infer. Ignore description/summary text.")
    required_educations: List[Education] = Field(default=[], description="The list of required educational backgrounds the job EXPLICITLY mentioned. Do not guess or infer. Ignore description/summary text.")
    optional_educations: List[Education] = Field(default=[], description="The list of optional educational backgrounds the job EXPLICITLY mentioned. Do not guess or infer. Ignore description/summary text.")
    required_years_of_experience: int = Field(default=0, description="Total required years of experience the job EXPLICITLY mentioned. Do not guess or infer. Ignore description/summary text.")