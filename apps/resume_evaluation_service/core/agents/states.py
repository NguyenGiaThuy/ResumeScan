from typing import Annotated, Dict, TypedDict
from common_modules.schemas.jd import JD
from common_modules.schemas.resume import Resume
from common_modules.schemas.resume_comparer import ResumeComparer
import operator


class ResumeEvaluationGraphState(TypedDict):
    resume_path: str
    resume: Resume
    jd_path: str
    jd: JD
    resume_comparer: ResumeComparer
    matching_points: float


class ComparerState(TypedDict):
    def merge_dict(existing: Dict, new: Dict) -> Dict:
        return {**existing, **new}

    resume: Resume
    jd: JD
    current_section_idx: Annotated[int, operator.add]
    sections: Annotated[Dict[int, Dict[str, int]], merge_dict]
    resume_comparer: ResumeComparer
