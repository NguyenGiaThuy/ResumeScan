from typing import Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from common_modules.agents.base_agent import BaseAgent
from core.agents.states import ResumeEvaluationGraphState
from common_modules.schemas.jd import JD
from tools.document_loader import docx_loader, pdf_loader, minio_pdf_loader

text_prompt = [
    (
        "system",
        """
You are a Job Description (JD) Extraction Assistant tasked with analyzing the JD text provided between triple backticks.

Instructions:
1. Extract **explicitly stated skills, qualifications, experience requirements, and certifications** from the JD.
2. Do not infer or assume any details not explicitly mentioned.
3. Ignore personal qualities, generic statements, or soft skills unless explicitly listed as a requirement.
4. Categorize extracted items clearly as:
   - Required hard skills
   - Optional hard skills
   - Required soft skills (if explicitly listed)
   - Optional soft skills (if explicitly listed)
   - Required years of experience
   - Required certifications or licenses
5. Maintain clarity: provide a concise, structured list.
6. If the JD text is empty or missing, return exactly: `EMPTY`.

Example:
JD text: "Required: Java, Python, 3+ years of experience. Optional: C#, AWS experience. Must be a fast learner."
Output:
- Required hard skills: Java, Python
- Optional hard skills: C#, AWS experience
- Required years of experience: 3
Ignore: "Must be a fast learner" (generic, not a specific skill or qualification).
"""
    ),
    (
        "human",
        "Please analyze the following JD: ```{jd_content}```"
    ),
]

class JDExtractionAgent(BaseAgent):
    def __init__(self, name: str, llm: BaseChatModel, tools: list[Callable]):
        super().__init__(name, llm, tools)
        self.prompt = self.get_jd_extraction_prompt_template()

    def get_jd_extraction_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate(text_prompt)
        # return ChatPromptTemplate([
        #     (
        #         "system",
        #         """
        #         You are a Job Description (JD) Extraction Assistant tasked with analyzing the JD text provided between triple backticks.

        #         Instructions:
        #         1. Extract only skills, qualifications, and requirements explicitly listed in the JD.
        #         2. Do not infer, assume, or include details not explicitly stated.
        #         3. Ignore personal qualities, preferences, or generic statements (e.g., "team player," "enjoys learning") unless explicitly listed as skills or qualifications.
        #         4. If the JD text is empty or missing, return exactly: `EMPTY`.
        #         5. Categorize extracted items as required or optional when specified in the JD.

        #         Example:
        #         JD text: "Required: Java, Python, 3+ years of experience. Optional: C#, AWS experience. Must be a fast learner."
        #         Output:
        #         - Required hard skills: Java, Python
        #         - Optional hard skills: C#, AWS experience
        #         - Required years of experience: 3
        #         Ignore: "Must be a fast learner" (generic, not a specific skill or qualification).
        #         """
        #     ),
        #     ("human", "Please analyze the following JD: ```{jd_content}```"),
        # ])

    def extract_jd(self, state: ResumeEvaluationGraphState) -> ResumeEvaluationGraphState:
        try:
            jd_path = state["jd_path"]

            # Check if it's an S3 URI
            if jd_path.startswith("s3://"):
                if jd_path.endswith(".pdf"):
                    self.logger.info(f"Processing S3 URI: {jd_path}")
                    jd_content = minio_pdf_loader.invoke(jd_path)
            # Check if it's a local file
            else:
                if jd_path.endswith(".pdf"):
                    self.logger.info(f"Processing local PDF: {jd_path}")
                    jd_content = pdf_loader.invoke(jd_path)
                elif jd_path.endswith(".docx"):
                    self.logger.info(f"Processing local DOCX: {jd_path}")
                    jd_content = docx_loader.invoke(jd_path)

            chain = self.prompt | self.llm.with_structured_output(JD)
            jd = chain.invoke({"jd_content": jd_content})

            return {"jd": jd}
        except Exception as ex:
            error_message = f"Error while extracting JD: {ex}"
            self.logger.error(error_message)
            raise error_message