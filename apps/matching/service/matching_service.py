"""
Matching Service
Handles JD-Resume matching logic using embeddings and LLM analysis
"""
import json
import re
from typing import Dict, Any
from langchain_community.embeddings import BedrockEmbeddings
from langchain_aws import ChatBedrock
from sklearn.metrics.pairwise import cosine_similarity


def create_embeddings_client(embedding_config: Dict[str, str]) -> BedrockEmbeddings:
    """Create and return embeddings client."""
    return BedrockEmbeddings(**embedding_config)


def create_model_client(model_config: Dict[str, Any]) -> ChatBedrock:
    """Create and return model client."""
    return ChatBedrock(**model_config)


def calculate_similarity_score(jd_text: str, resume_text: str, embeddings: BedrockEmbeddings) -> float:
    """Calculate similarity score between JD and Resume using embeddings."""
    try:
        # Get embeddings for both texts
        jd_embedding = embeddings.embed_query(jd_text)
        resume_embedding = embeddings.embed_query(resume_text)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(
            [jd_embedding], [resume_embedding]
        )[0][0]
        
        # Convert to percentage
        return float(similarity * 100)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0


def analyze_match_with_llm(jd_text: str, resume_text: str, model: ChatBedrock) -> Dict[str, Any]:
    """Use LLM to analyze the match between JD and Resume."""
    prompt = f"""
    Analyze the following Job Description and Resume to determine their compatibility.
    
    Job Description:
    {jd_text[:2000]}...
    
    Resume:
    {resume_text[:2000]}...
    
    Please provide:
    1. A match percentage (0-100)
    2. Key matching skills/experiences
    3. Missing requirements
    4. Overall assessment
    
    Respond in JSON format:
    {{
        "match_percentage": <number>,
        "matching_skills": ["skill1", "skill2", ...],
        "missing_requirements": ["req1", "req2", ...],
        "assessment": "detailed assessment text"
    }}
    """
    
    try:
        response = model.invoke(prompt)
        # Try to parse JSON from response
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            # Fallback if JSON parsing fails
            return {
                "match_percentage": 0,
                "matching_skills": [],
                "missing_requirements": [],
                "assessment": "Unable to parse analysis"
            }
    except Exception as e:
        print(f"Error in LLM analysis: {e}")
        return {
            "match_percentage": 0,
            "matching_skills": [],
            "missing_requirements": [],
            "assessment": f"Analysis failed: {str(e)}"
        }


def perform_complete_match(
    jd_text: str, 
    resume_text: str, 
    jd_filename: str, 
    resume_filename: str,
    embeddings: BedrockEmbeddings,
    model: ChatBedrock
) -> Dict[str, Any]:
    """Perform complete matching analysis combining embeddings and LLM."""
    # Calculate similarity using embeddings
    similarity_score = calculate_similarity_score(jd_text, resume_text, embeddings)
    
    # Get detailed analysis from LLM
    llm_analysis = analyze_match_with_llm(jd_text, resume_text, model)
    
    # Combine results
    result = {
        "embedding_similarity": similarity_score,
        "llm_analysis": llm_analysis,
        "final_match_percentage": max(similarity_score, llm_analysis.get("match_percentage", 0)),
        "is_qualified": max(similarity_score, llm_analysis.get("match_percentage", 0)) >= 50.0,
        "jd_filename": jd_filename,
        "resume_filename": resume_filename
    }
    
    return result
