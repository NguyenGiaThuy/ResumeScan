from pydantic import BaseModel, Field
from typing import List, Optional


class Experience(BaseModel):
    """Model representing a work experience entry in a resume."""
    job_title: str = Field(description="The job title.")
    company: str = Field(description="The company where the experience applied.")
    dates: str = Field(description="The dates of employment.")
    responsibilities: List[str] = Field(default=[], description="A list of responsibilities held in the position.")
    tech_stack: List[str] = Field(default=[], description="A list of technologies, programming languages, frameworks, or tools explicitly used in this role.")
    summary: str = Field(description="A concise summary highlighting the main role, key achievements, core responsibilities, and the technologies from the tech stack used in the position.")


class Education(BaseModel):
    """Model representing an education entry in a resume."""
    degree: str = Field(description="The degree or qualification obtained (e.g., Bachelor of Science in Computer Science).")
    institution: str = Field(description="The name of the school, college, or university.")
    dates: Optional[str] = Field(default=None, description="The dates attended or graduation year (if applicable).")
    field_of_study: str = Field(description="The major or field of study.")
    grade: Optional[str] = Field(default=None, description="The GPA or grade achieved (if applicable).")
    summary: str = Field(description="A concise summary of the education background, highlighting key achievements, coursework, or distinctions.")
