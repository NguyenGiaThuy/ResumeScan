import os
from logging import Logger
from langgraph.graph.state import CompiledStateGraph, StateGraph, START, END
from tools.resume_evaluator import resume_evaluator
from core.agents.resume_comparison_agent import ResumeComparisonAgent
from core.agents.jd_extraction_agent import JDExtractionAgent
from core.agents.resume_extraction_agent import ResumeExtractionAgent
from core.agents.states import ComparerState, ResumeEvaluationGraphState
from common_modules.factories.llm_factory import LLMFactory
from tools.document_loader import docx_loader, pdf_loader, minio_pdf_loader, minio_pdf_loader_by_key, list_minio_pdfs
from typing import Any
from langchain_core.rate_limiters import InMemoryRateLimiter


class Orchestrator:
    def __init__(self):
        LLM_MODEL = os.environ["GEMINI_MODEL"]
        LLM_API_KEY = os.environ["GEMINI_API_KEY"]
        self.llm = LLMFactory.create_llm(
            llm_provider=LLMFactory.Provider.GEMINI,
            config=LLMFactory.Config(
                model_name=LLM_MODEL,
                api_key=LLM_API_KEY,
                temperature=0.0,
                top_p=1.0,
                rate_limiter=InMemoryRateLimiter(
                    requests_per_second=0.25,  # 1 yêu cầu mỗi 4 giây
                    check_every_n_seconds=0.1,
                    max_bucket_size=15
                )
            )
        )
        self.tools = [pdf_loader, docx_loader, minio_pdf_loader, minio_pdf_loader_by_key, list_minio_pdfs, resume_evaluator]
        self.logger = Logger("orchestrator")

    def orchestrate(self) -> CompiledStateGraph[Any, Any, Any, Any]:
        try:
            resume_extraction_agent = ResumeExtractionAgent("resume_extraction_agent", self.llm, self.tools)
            jd_extraction_agent = JDExtractionAgent("jd_extraction_agent", self.llm, self.tools)
            resume_comparison_agent = ResumeComparisonAgent("resume_comparison_agent", self.llm, self.tools)

            # Subgraph
            subgraph_builder = StateGraph(ComparerState)
            subgraph_builder.add_node("increment_1", resume_comparison_agent.increase_section_idx)
            subgraph_builder.add_node("increment_2", resume_comparison_agent.increase_section_idx)
            subgraph_builder.add_node("increment_3", resume_comparison_agent.increase_section_idx)

            subgraph_builder.add_node("section_comparison_1", resume_comparison_agent.compare_section)
            subgraph_builder.add_node("section_comparison_2", resume_comparison_agent.compare_section)
            subgraph_builder.add_node("section_comparison_3", resume_comparison_agent.compare_section)
            subgraph_builder.add_node("section_comparison_4", resume_comparison_agent.compare_section)
            subgraph_builder.add_node("resume_comparison", resume_comparison_agent.compare_resume)

            subgraph_builder.add_edge(START, "section_comparison_1")
            subgraph_builder.add_edge(START, "increment_1")
            subgraph_builder.add_edge("increment_1", "increment_2")
            subgraph_builder.add_edge("increment_2", "increment_3")
            subgraph_builder.add_edge("increment_1", "section_comparison_2")
            subgraph_builder.add_edge("increment_2", "section_comparison_3")
            subgraph_builder.add_edge("increment_3", "section_comparison_4")
            subgraph_builder.add_edge("section_comparison_1", "resume_comparison")
            subgraph_builder.add_edge("section_comparison_2", "resume_comparison")
            subgraph_builder.add_edge("section_comparison_3", "resume_comparison")
            subgraph_builder.add_edge("section_comparison_4", "resume_comparison")
            subgraph_builder.add_edge("resume_comparison", END)

            subgraph = subgraph_builder.compile()

            subgraph_node = lambda state: {
                "resume_comparer": subgraph.invoke({
                    "resume": state["resume"], "jd": state["jd"]
                })["resume_comparer"]
            }

            resume_evaluator_node = lambda state: {
                "matching_points": resume_evaluator.invoke({
                    "jd": state["jd"], "resume_comparer": state["resume_comparer"]
                })
            }

            # Main graph
            maingraph_builder = StateGraph(ResumeEvaluationGraphState)
            maingraph_builder.add_node("resume_extraction", resume_extraction_agent.extract_resume)
            maingraph_builder.add_node("jd_extraction", jd_extraction_agent.extract_jd)
            maingraph_builder.add_node("resume_comparison", subgraph_node)
            maingraph_builder.add_node("resume_evaluation", resume_evaluator_node)

            maingraph_builder.add_edge(START, "resume_extraction")
            maingraph_builder.add_edge(START, "jd_extraction")
            maingraph_builder.add_edge("resume_extraction", "resume_comparison")
            maingraph_builder.add_edge("jd_extraction", "resume_comparison")
            maingraph_builder.add_edge("resume_comparison", "resume_evaluation")
            maingraph_builder.add_edge("resume_evaluation", END)

            self.graph = maingraph_builder.compile()

            return self.graph
        except Exception as ex:
            self.logger.error(f"Error while building graph: {ex}")
            return None

    def export_graph(self, path: str) -> None:
        try:
            with open(path, "wb") as f:
                f.write(self.graph.get_graph().draw_mermaid_png())
        except Exception as ex:
            self.logger.error(f"Error while exporting graph: {ex}")