# Chatbox - AI Elevate Interview System

An AI-powered interview application that uses Job Description and Resume matching to qualify candidates before starting the interview process.

## Features

### 🔍 Smart Qualification System
- **Dual Upload Interface**: Upload Job Description (left panel) and Resume (right panel) as PDF files
- **AI-Powered Matching**: Uses AWS Bedrock models for semantic analysis and matching
- **50% Threshold**: Only candidates with 50%+ compatibility can proceed to interview
- **Detailed Analysis**: Shows matching skills, missing requirements, and AI assessment

### 🎤 AI Interview Session
- **Context-Aware Questions**: AI generates relevant questions based on the uploaded resume
- **RAG-Enabled Chat**: Uses vector search on resume content for informed responses
- **Professional Interface**: Clean, intuitive design for smooth interview experience
- **Session Management**: Easy reset and new session functionality

## Architecture

The application consists of two main components:

1. **Chatbox App** (`apps/chatbox`): Streamlit-based frontend application
2. **Matching Service** (`apps/matching`): FastAPI service for JD-Resume compatibility analysis

### Project Structure

```
apps/chatbox/
├── main.py              # Application entry point
├── app.py               # Main application class
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── components/         # UI components
│   ├── styles.py       # Custom CSS styling
│   └── ui.py           # UI helper functions
├── pages/              # Application pages
│   ├── upload.py       # File upload page
│   ├── processing.py   # Document processing page
│   └── interview.py    # AI interview page
├── services/           # External service integrations
│   ├── matching.py     # Matching service client
│   └── interview.py    # Interview AI service
├── configs/            # Configuration files
└── utils/              # Utility functions
```

## How It Works

1. **Upload Phase**: User uploads JD and Resume PDFs through the web interface
2. **Analysis Phase**: Files are sent to the matching service for AI analysis
3. **Qualification Check**: System evaluates if match score ≥ 50%
4. **Interview Phase**: Qualified candidates proceed to AI-powered interview

## Dependencies

- **Streamlit** - Web application framework
- **LangChain** - LLM integration and document processing
- **AWS Bedrock** - AI models via LangChain AWS
- **FAISS** - Vector similarity search
- **PyPDF** - PDF document processing
- **Requests** - HTTP client for service integration

## Docker Image Preparation

Login to ECR:

```sh
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 058264469194.dkr.ecr.ap-southeast-1.amazonaws.com
```

Build & Push:

```sh
REPO=058264469194.dkr.ecr.ap-southeast-1.amazonaws.com
IMAGE=ai-elevate/chatbox
TAG=

docker build --network=host -t ${REPO}/${IMAGE}:${TAG} .
docker push ${REPO}/${IMAGE}:${TAG}
```

## Running the Application

### Local Development
```bash
pip install -r requirements.txt
streamlit run main.py
```

### Docker
```bash
docker build -t chatbox .
docker run -p 8501:8501 -v /path/to/configs:/chatbox/configs chatbox
```

The application will be available at `http://localhost:8501`

### Using Docker Compose (Recommended)
```bash
cd compose
docker-compose up chatbox matching
```

## Configuration

Set the `CONFIG_FILE` environment variable to point to your configuration file:

```bash
export CONFIG_FILE=/app/configs/ai-elevate-dev.json
```

### Environment Variables

#### Chatbox App
- `CONFIG_FILE`: Path to configuration file (default: `/app/configs/ai-elevate-dev.json`)
- `MATCHING_SERVICE_URL`: URL of the matching service (default: `http://matching:8001`)
- AWS credentials: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`

#### Matching Service
- `CONFIG_FILE`: Path to configuration file (default: `/app/configs/ai-elevate-dev.json`)
- `PORT`: Service port (default: `8001`)
- AWS credentials: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`

Both apps use the same configuration format in `configs/ai-elevate-dev.json`:

```json
{
    "aws": {
        "region": "ap-southeast-1",
        "bedrock": {
            "model_id": "us.deepseek.r1-v1:0",
            "model_region": "us-west-2",
            "model_kwargs": { "temperature": 0.8 },
            "embedding_model_id": "amazon.titan-embed-text-v2:0"
        }
    },
    "initial_system_message": "You are an interviewer...",
    "initial_ai_message": "Please submit your CV/Resume...",
    "holding_context_message": "..."
}
```

## API Integration

### Matching Service (`http://localhost:8001`)
- `GET /`: Service information
- `GET /health`: Health check
- `POST /match`: Upload JD and Resume for analysis

### Chatbox App (`http://localhost:8501`)
- Web interface accessible through browser

## Additional Information

### User Flow

```
1. Landing Page
   ├── Upload JD (PDF) - Left Panel
   └── Upload Resume (PDF) - Right Panel
   
2. Click "Analyze Compatibility"
   ├── Processing screen with spinner
   └── API call to matching service
   
3. Results Display
   ├── Match Score ≥ 50% → Proceed to Interview
   └── Match Score < 50% → Show improvement suggestions
   
4. Interview Session (if qualified)
   ├── AI generates context-aware questions
   ├── User responds via chat interface
   └── AI provides follow-up questions
```

### Customization

- **Threshold**: Modify the 50% threshold in `main.py`
- **Styling**: Update CSS in the Streamlit app
- **Prompts**: Adjust interview prompts in configuration
- **Models**: Change AI models in configuration file

### Security Considerations

- PDF files are processed in temporary directories and cleaned up
- No persistent storage of uploaded files
- CORS enabled for web integration
- Health checks for service monitoring

## Customization

- **Threshold**: Modify the 50% threshold in `main.py`
- **Styling**: Update CSS in the Streamlit app
- **Prompts**: Adjust interview prompts in configuration
- **Models**: Change AI models in configuration file

## Security Considerations

- PDF files are processed in temporary directories and cleaned up
- No persistent storage of uploaded files
- CORS enabled for web integration
- Health checks for service monitoring
