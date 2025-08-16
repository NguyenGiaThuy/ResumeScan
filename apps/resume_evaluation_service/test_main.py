import os
from core.agents.orchestrator import Orchestrator
from dotenv import load_dotenv


load_dotenv()

orchestrator = Orchestrator()
graph = orchestrator.orchestrate()

base_dir = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "graph_diagrams/graph.png")
orchestrator.export_graph(image_path)

resume_path = os.path.join(base_dir, "test_samples/resumes/cv1.pdf")
jd_path = os.path.join(base_dir, "test_samples/jds/jd5.pdf")
content = graph.invoke(input={"resume_path": resume_path, "jd_path": jd_path})
resume_comparer = content["resume_comparer"]
resume = content["resume"]
jd = content["jd"]
points = content["matching_points"]
print(resume_comparer.model_dump_json() + "\n")
print(jd.model_dump_json() + "\n")
print(resume.model_dump_json() + "\n")
print(points)
# print(content)




# import uvicorn
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from apis.routers import router


# app = FastAPI(
#     title="Resume Evaluator",
#     description="To evaluate resume - JD matching",
#     version="1.0.0-beta",
# )
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.include_router(router)

# if __name__ == "__main__":
#     uvicorn.run(
#         app,
#         host="0.0.0.0",
#         port=8088,
#         log_level="debug",
#         access_log=True,
#     )
