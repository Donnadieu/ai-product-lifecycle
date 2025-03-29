from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from stakeholder_agents import run_stakeholder_crew
from pm_agents import run_pm_crew
from engineering_agents import run_engineering_crew
from ticketing_agents import run_ticketing_crew
from feature_orchestrator import orchestrate_feature_pipeline
from llm_config import LLMConfig, LLMProvider
import os
from functools import wraps

def handle_llm_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if "rate limit" in str(e).lower():
                raise HTTPException(
                    status_code=429,
                    detail=f"LLM API rate limit exceeded. Please try again later or check your quota."
                )
            elif "auth" in str(e).lower() or "key" in str(e).lower():
                raise HTTPException(
                    status_code=401,
                    detail=f"Invalid API key. Please check your configuration."
                )
            else:
                raise HTTPException(status_code=500, detail=f"LLM API error: {str(e)}")
    return wrapper

load_dotenv()

# Initialize LLM configuration
llm_provider = os.getenv("LLM_PROVIDER", LLMProvider.OPENAI)
api_key = os.getenv(f"{llm_provider.upper()}_API_KEY")
if not api_key:
    raise ValueError(f"{llm_provider.upper()}_API_KEY environment variable is not set")

llm_config = LLMConfig(provider=llm_provider, api_key=api_key)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-stakeholder-requirements/")
@handle_llm_errors
async def generate_stakeholder_requirements(data: dict):
    idea = data.get("idea", "")
    if not idea:
        raise HTTPException(status_code=400, detail="Missing 'idea'")
    
    output = run_stakeholder_crew(idea)
    return {"output": output}

@app.post("/generate-pm-specs/")
@handle_llm_errors
async def generate_pm_specs(data: dict):
    idea = data.get("idea", "")
    if not idea:
        raise HTTPException(status_code=400, detail="Missing 'idea'")
    
    output = run_pm_crew(idea)
    return {"output": output}

@app.post("/generate-engineering-plan/")
@handle_llm_errors
async def generate_engineering_plan(data: dict):
    prd = data.get("prd", "")
    if not prd:
        raise HTTPException(status_code=400, detail="Missing 'prd'")
    
    output = run_engineering_crew(prd)
    return {"output": output}

@app.post("/generate-tickets/")
@handle_llm_errors
async def generate_tickets(data: dict):
    plan = data.get("plan", "")
    if not plan:
        raise HTTPException(status_code=400, detail="Missing 'plan'")
    
    output = run_ticketing_crew(plan)
    return {"output": output}

@app.post("/build-feature/")
@handle_llm_errors
async def build_feature(data: dict):
    idea = data.get("idea")
    if not idea:
        raise HTTPException(status_code=400, detail="Missing 'idea'")
    
    result = await orchestrate_feature_pipeline(idea)
    return result

@app.post("/quick-test/")
@handle_llm_errors
async def quick_test(data: dict):
    """Quick test endpoint that makes a single LLM call for faster testing"""
    idea = data.get("idea")
    if not idea:
        raise HTTPException(status_code=400, detail="Missing 'idea'")
    
    llm = LLMConfig()
    
    # Create a simple prompt for quick testing
    prompt = f"""Given this product idea: {idea}
    
    Provide a quick analysis in this JSON format:
    {{
        "summary": "Brief 2-3 sentence summary",
        "key_features": ["3-4 main features"],
        "technical_stack": ["2-3 recommended technologies"],
        "challenges": ["2-3 potential challenges"]
    }}
    
    Return ONLY the JSON object, no additional text or formatting.
    Make sure the response is valid JSON that can be parsed."""
    
    # Make a single LLM call
    response = await llm.generate_response(prompt, temperature=0.7)
    
    # Try to parse response as JSON
    try:
        import json
        # Clean up the response - remove any markdown formatting if present
        clean_response = response.strip().strip('`').strip()
        if clean_response.startswith('```json'):
            clean_response = clean_response[7:]
        if clean_response.startswith('```'):
            clean_response = clean_response[3:]
        clean_response = clean_response.strip('`').strip()
        
        # Parse and validate JSON
        parsed = json.loads(clean_response)
        
        # Ensure all required fields are present
        required_fields = ['summary', 'key_features', 'technical_stack', 'challenges']
        for field in required_fields:
            if field not in parsed:
                parsed[field] = []
                
        return parsed
    except json.JSONDecodeError:
        # If parsing fails, return the raw response
        return response
