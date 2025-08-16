import json
import re
from typing import Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from common_modules.agents.base_agent import BaseAgent
from core.agents.states import ComparerState
from common_modules.schemas.resume_comparer import ResumeComparer, SectionComparer

text_prompt = [
    (
        "system",
        """
You are a Resume Evaluation Assistant tasked with analyzing the similarity between a resume section and a job description (JD). Follow these steps:

1. Compare the resume section to the required and optional sections in the JD.
2. For each item in the resume section:
   - If it matches a required JD item, assign "value": 1.
   - If it matches an optional JD item, assign "value": 0.
   - If it is not in the JD but is semantically related to a required or optional JD item, assign "value": 0.
   - If it is unrelated to any JD item, do NOT include it in the output.
3. For each required or optional JD item not present in the resume, include it with "value": -1.
4. Correct typos in the resume section (e.g., "Pytoch" → "Pytorch") and match items based on corrected terms or semantic similarity.
5. Include all work experience dates as given (format: <[DATE]>: YYYY - YYYY).
6. Always return a JSON object with the following structure:

{{
  "items": [
    {{
      "name": "<item_name>",
      "value": <assigned_value>
    }},
    ...
  ]
}}

7. Ensure all items from the resume and JD (even missing JD items) are represented according to the rules above. Do not omit keys.

Example:
Resume section: ["Java", "Python", "Go", "Spring Boot", "Pytoch", "C#"]
JD required: ["Java", "Python", "Rust"]
JD optional: ["C#"]
Expected output:
{{
  "items": [
    {{"name": "Java", "value": 1}},
    {{"name": "Python", "value": 1}},
    {{"name": "Spring Boot", "value": 0}},
    {{"name": "Pytorch", "value": 0}},
    {{"name": "C#", "value": 0}},
    {{"name": "Rust", "value": -1}}
  ]
}}
"""
    ),
    (
        "human",
        """Please evaluate the following section:
Resume Section: {resume_section}
JD Required: {jd_required_section}
JD Optional: {jd_optional_section}
"""
    ),
]

class ResumeComparisonAgent(BaseAgent):
    def __init__(self, name: str, llm: BaseChatModel, tools: list[Callable]):
        super().__init__(name, llm, tools)
        self.prompt = self.get_section_comparison_prompt_template()

    def get_section_comparison_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate(text_prompt)

        # return ChatPromptTemplate([
        #     (
        #         "system",
        #         """
        #         You are a resume evaluator tasked with analyzing the similarity between a resume section and a job description (JD). Follow these steps:
        #         1. Compare the resume section to the required and optional sections in the JD.
        #         2. For each item in the resume section:
        #         - If it matches a required item in the JD, assign value=1.
        #         - If it matches an optional item in the JD, assign value=0.
        #         - If it is not in the JD but is closely related to a required or optional JD item, assign value=0.
        #         - If it is unrelated to any JD item, do not include it in the output.
        #         3. For each required or optional JD item not present in the resume, include it with value=-1.
        #         4. Correct typos in the resume section (e.g., "Pytoch" → "Pytorch") and match items to the JD based on corrected terms or semantic similarity.
        #         5. Return the result as a JSON object mapping each item to its assigned value.
        #         6. For the work experiences, do not ommitted the <[DATE]>: YYYY - YYYY part at the end.

        #         Example:
        #         Resume:
        #         - Section: ["Java", "Python", "Go", "Spring Boot", "Pytoch", "C#"]
        #         JD:
        #         - Required section: ["Java", "Python", "Rust"]
        #         - Optional section: ["C#"]
        #         Expected output:
        #         - "output": {{"Java": 1, "Python": 1, "Spring Boot": 0, "Pytorch": 0, "C#": 0, "Rust": -1}}
        #         Explanation step by step:
        #         - Java, Python exists in resume and is required in JD. → included with value=1
        #         - Go exists in resume, but does not exists in JD. → not included
        #         - Spring Boot exists in resume and is related to Java (which is required in JD). → included with value=0
        #         - Pytoch exists in resume, and is a typo of Pytorch, and is related to Python (which is required in JD). → included with value=0
        #         - C# exists in resume, and is optional in JD. → included with value=0
        #         - Rust does not exist in resume, but is required in JD. → included with value=-1
        #         """
        #     ),
        #     (
        #         "human",
        #         """Please evaluate following section:
        #         Resume:
        #         - Section: {resume_section}
        #         JD:
        #         - Required section: {jd_required_section}
        #         - Optional section: {jd_optional_section}
        #         """
        #     ),
        # ])

    def compare_section(self, state: ComparerState) -> ComparerState:
        try:
            resume_section = state["resume"].hard_skills
            jd_required_section = state["jd"].required_hard_skills
            jd_optional_section = state["jd"].optional_hard_skills
            if state["current_section_idx"] == 1:
                resume_section = state["resume"].soft_skills
                jd_required_section = state["jd"].required_soft_skills
                jd_optional_section = state["jd"].optional_soft_skills
            elif state["current_section_idx"] == 2:
                resume_section = [item.summary for item in state["resume"].work_experiences]
                jd_required_section = [item.summary for item in state["jd"].required_work_experiences]
                jd_optional_section = [item.summary for item in state["jd"].optional_work_experiences]
            elif state["current_section_idx"] == 3:
                resume_section = [item.summary for item in state["resume"].educations]
                jd_required_section = [item.summary for item in state["jd"].required_educations]
                jd_optional_section = [item.summary for item in state["jd"].optional_educations]
            elif state["current_section_idx"] == 4:
                resume_section = state["resume"].certifications
                jd_required_section = state["jd"].required_hard_skills
                jd_optional_section = state["jd"].optional_hard_skills

            chain = self.prompt | self.llm.with_structured_output(SectionComparer)
            output = chain.invoke({
                "resume_section": json.dumps(resume_section, ensure_ascii=False),
                "jd_required_section": json.dumps(jd_required_section, ensure_ascii=False),
                "jd_optional_section": json.dumps(jd_optional_section, ensure_ascii=False)
            })
            section_items = output.section_items

            return {"sections": {state["current_section_idx"]: json.loads(section_items or "{}")}}
        except Exception as ex:
            error_message = f"Error while comparing resume: {ex}"
            self.logger.error(error_message)
            raise error_message

    def increase_section_idx(self, state: ComparerState) -> ComparerState:
        return {"current_section_idx": 1}

    def compare_resume(self, state: ComparerState) -> ComparerState:
        def total_year(input_list: list):
            extract_date_list = []
            for item in input_list:
                item = re.findall(r"<\[DATE\]>\s*[:]*\s*(\d{4}\s*-\s*\d{4})\s*", item)
                if item:
                    extract_date_list.extend(item)
            result = 0
            i = 0
            while i < len(extract_date_list):
                start_element1, end_element1 = map(int, extract_date_list[i].split('-'))
                j = i + 1
                while j < len(extract_date_list):
                    start_element2, end_element2 = map(int, extract_date_list[j].split('-'))
                    if(start_element1 <= start_element2 and end_element1 >= end_element2):
                        extract_date_list.pop(j)
                    elif(start_element1 >= start_element2 and end_element1 <= end_element2):
                        extract_date_list.pop(i)
                        i = i - 1
                        break
                    elif(start_element1 <= start_element2 <= end_element1 <= end_element2 ):
                        new_start = start_element1
                        new_end = end_element2
                        extract_date_list[i] = f"{new_start}-{new_end}"
                        extract_date_list.pop(j)
                        start_element1 = new_start
                        end_element1 = new_end
                    elif(start_element2 <= start_element1 <= end_element2 <= end_element1 ):
                        new_start = start_element2
                        new_end = end_element1
                        extract_date_list[i] = f"{new_start}-{new_end}"
                        extract_date_list.pop(j)
                        start_element1 = new_start
                        end_element1 = new_end
                    else:
                        j = j + 1
                i = i + 1
            for tmp in range(len(extract_date_list)):
                start_element, end_element = map(int, extract_date_list[tmp].split('-'))
                result = result + (end_element - start_element)

            return result

        relevant_experiences = [exp for exp, flag in state["sections"].get(2, {}).items() if flag in (0, 1)]
        years_of_experience = total_year(relevant_experiences)

        resume_comparer = ResumeComparer(
            profile_summary=state["resume"].profile_summary,
            hard_skills=state["sections"].get(0, {}),
            soft_skills=state["sections"].get(1, {}),
            work_experiences=state["sections"].get(2, {}),
            years_of_experience=years_of_experience,
            educations=state["sections"].get(3, {}),
            certifications=state["sections"].get(4, {}),
            projects=state["resume"].projects,
        )

        return {"resume_comparer": resume_comparer}