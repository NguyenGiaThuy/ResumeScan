from typing import Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from common_modules.agents.base_agent import BaseAgent
from core.agents.states import ResumeEvaluationGraphState
from common_modules.schemas.resume import Resume
from tools.document_loader import docx_loader, pdf_loader, minio_pdf_loader, minio_pdf_loader_by_key

text_prompt = [
    ("system", """
You are a Resume Extraction Assistant tasked with analyzing the resume text provided between triple backticks.

Instructions:
1. **Anonymize Personal Information:** Remove all personal details, including but not limited to:
   - Full name
   - Address
   - Phone number
   - Email address
   - Social media profiles (LinkedIn, GitHub, etc.)
   - Any other personally identifiable information

2. **Extract Key Resume Components:** Identify and structure the following sections:
   - **Professional Summary:** Career highlights overview
   - **Work Experience:** List positions held, including job title, company name, duration, responsibilities, achievements
   - **Education:** Degree, institution, graduation year
   - **Skills:** Explicitly listed skills only (technical and soft skills)
   - **Certifications:** Relevant certifications/licenses
   - **Projects:** Notable projects (name, description, role, technologies used)

3. **Formatting Guidelines:**
   - Use clear, consistent headings
   - Present information in structured bullet points
   - Return output as JSON with sections clearly labeled

4. **Handling Missing Information:** If a section is absent in the resume, indicate explicitly in the JSON.

5. **Edge Cases:** If the resume text is empty or missing, return exactly: `EMPTY`.
"""),
    ("human", "Please analyze the following resume: ```{resume_content}```"),
]


class ResumeExtractionAgent(BaseAgent):
    def __init__(self, name: str, llm: BaseChatModel, tools: list[Callable]):
        super().__init__(name, llm, tools)
        self.prompt = self.get_resume_extraction_prompt_template()

    def get_resume_extraction_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate(text_prompt)   
        # return ChatPromptTemplate([
        #     (
        #         "system",
        #         """
        #         You are a Resume Extraction Assistant tasked with analyzing the resume text provided between triple backticks.

        #         Instructions:
        #         1. Extract and anonymize the resume by removing all personal information, including but not limited to names, addresses, phone numbers, emails, and social media links.
        #         2. Extract skills only if they are explicitly listed in dedicated sections (e.g., "Skills", "Technical Skills", "Core Competencies") or clearly mentioned within their work experiences.
        #         3. Do not infer, assume, or include skills or qualifications not explicitly stated in the resume.
        #         4. If the resume text is empty or missing, return exactly: `EMPTY`.
        #         """
        #     ),
        #     ("human", "Please analyze the following resume: ```{resume_content}```"),
        # ])

    def extract_resume(self, state: ResumeEvaluationGraphState) -> ResumeEvaluationGraphState:
        try:
            resume_path = state["resume_path"]

            # Check if it's an S3 URI
            if resume_path.startswith("s3://"):
                if resume_path.endswith(".pdf"):
                    self.logger.info(f"Processing S3 URI: {resume_path}")
                    resume_content = minio_pdf_loader.invoke(resume_path)
            # Check if it's a local file
            else:
                if resume_path.endswith(".pdf"):
                    self.logger.info(f"Processing local PDF: {resume_path}")
                    resume_content = pdf_loader.invoke(resume_path)
                elif resume_path.endswith(".docx"):
                    self.logger.info(f"Processing local DOCX: {resume_path}")
                    resume_content = docx_loader.invoke(resume_path)

            chain = self.prompt | self.llm.with_structured_output(Resume)
            resume = chain.invoke({"resume_content": resume_content})

            for work_experience in resume.work_experiences:
                work_experience.summary += f" <[DATE]>:{work_experience.dates}"

            return {"resume": resume}
        except Exception as ex:
            error_message = f"Error while extracting resume: {ex}"
            self.logger.error(error_message)
            raise error_message