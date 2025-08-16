# JD-Resume Matching Service

This FastAPI service provides AI-powered matching between Job Descriptions and Resumes using AWS Bedrock models.

## Features

- PDF text extraction for both JD and Resume files
- Semantic similarity analysis using embeddings
- LLM-powered detailed matching analysis
- RESTful API with automatic documentation
- Health check endpoint
- CORS support for web integration

## API Endpoints

### GET /
Service information and available endpoints

### GET /health
Health check endpoint

### POST /match
Upload JD and Resume PDFs to get compatibility analysis

**Request:**
- `jd_file`: Job Description PDF file
- `resume_file`: Resume/CV PDF file

**Response:**
```json
{
    "embedding_similarity": 75.2,
    "llm_analysis": {
        "match_percentage": 78,
        "matching_skills": ["Python", "Machine Learning", "AWS"],
        "missing_requirements": ["Kubernetes", "5+ years experience"],
        "assessment": "Strong technical match with some experience gaps"
    },
    "final_match_percentage": 78.0,
    "is_qualified": true,
    "jd_filename": "job_description.pdf",
    "resume_filename": "resume.pdf"
}
```

## Configuration

Set the `CONFIG_FILE` environment variable to point to your configuration file:

```bash
export CONFIG_FILE=/app/configs/ai-elevate-dev.json
```

## Running the Service

### Local Development
```bash
python main.py
```

### Docker
```bash
docker build -t matching .
docker run -p 8001:8001 -v /path/to/configs:/app/configs matching
```

The service will be available at `http://localhost:8001`

## Dependencies

- FastAPI - Web framework
- LangChain - LLM integration
- AWS Bedrock - AI models
- scikit-learn - Similarity calculations
- PyPDF - PDF text extraction
