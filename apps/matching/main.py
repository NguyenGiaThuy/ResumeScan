"""
JD and Resume Matching Service
FastAPI application for matching Job Descriptions with Resumes
"""
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from service import (
    get_embedding_config,
    get_model_config,
    extract_text_from_pdf,
    create_embeddings_client,
    create_model_client,
    perform_complete_match
)

app = FastAPI(
    title="JD-Resume Matching Service", 
    version="1.0.0",
    description="AI-powered service to match Job Descriptions with Resumes"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
embeddings = create_embeddings_client(get_embedding_config())
model = create_model_client(get_model_config())



@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "JD-Resume Matching Service",
        "version": "1.0.0",
        "description": "AI-powered service to match Job Descriptions with Resumes",
        "endpoints": {
            "health": "/health",
            "match": "/match"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "JD-Resume Matching Service"}


@app.post("/match")
async def match_jd_resume(
    jd_file: UploadFile = File(..., description="Job Description PDF"),
    resume_file: UploadFile = File(..., description="Resume PDF")
):
    """
    Match Job Description with Resume and return compatibility score.
    """
    if not jd_file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="JD file must be a PDF")
    
    if not resume_file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Resume file must be a PDF")
    
    try:
        # Extract text from both PDFs
        jd_content = await jd_file.read()
        resume_content = await resume_file.read()
        
        jd_text = extract_text_from_pdf(jd_content)
        resume_text = extract_text_from_pdf(resume_content)
        
        if not jd_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from JD PDF")
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from Resume PDF")
        
        # Perform complete matching analysis using functional approach
        result = perform_complete_match(
            jd_text=jd_text,
            resume_text=resume_text,
            jd_filename=jd_file.filename,
            resume_filename=resume_file.filename,
            embeddings=embeddings,
            model=model
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
