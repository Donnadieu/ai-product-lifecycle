from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from openai.error import OpenAIError, RateLimitError, AuthenticationError
from dotenv import load_dotenv
from stakeholder_agents import run_stakeholder_crew
from pm_agents import run_pm_crew
from engineering_agents import run_engineering_crew
from ticketing_agents import run_ticketing_crew
from feature_orchestrator import orchestrate_feature_pipeline
import os
from functools import wraps

def handle_openai_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RateLimitError:
            raise HTTPException(
                status_code=429,
                detail="OpenAI API rate limit exceeded. Please try again later or check your quota."
            )
        except AuthenticationError:
            raise HTTPException(
                status_code=401,
                detail="Invalid OpenAI API key. Please check your configuration."
            )
        except OpenAIError as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    return wrapper

load_dotenv()

# Verify OpenAI API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-stakeholder-requirements/")
@handle_openai_errors
async def generate_stakeholder_requirements(data: dict):
    idea = data.get("idea", "")
    if not idea:
        raise HTTPException(status_code=400, detail="Missing 'idea'")
    
    context = {"openai_api_key": api_key}
    output = run_stakeholder_crew(idea, context)
    return {"output": output}

@app.post("/generate-pm-specs/")
@handle_openai_errors
async def generate_pm_specs(data: dict):
    idea = data.get("idea", "")
    if not idea:
        raise HTTPException(status_code=400, detail="Missing 'idea'")
    
    context = {"openai_api_key": api_key}
    output = run_pm_crew(idea, context)
    return {"output": output}

@app.post("/generate-engineering-plan/")
async def generate_engineering_plan(data: dict):
    prd = data.get("prd", "")
    if not prd:
        raise HTTPException(status_code=400, detail="Missing 'prd'")
    
    context = { "openai_api_key": os.getenv("OPENAI_API_KEY") }
    output = run_engineering_crew(prd, context)
    return {"output": output}

@app.post("/generate-tickets/")
async def generate_tickets(data: dict):
    plan = data.get("plan", "")
    if not plan:
        raise HTTPException(status_code=400, detail="Missing 'plan'")
    
    context = { "openai_api_key": os.getenv("OPENAI_API_KEY") }
    output = run_ticketing_crew(plan, context)
    return {"output": output}

@app.post("/build-feature/")
async def build_feature(data: dict):
    idea = data.get("idea")
    if not idea:
        raise HTTPException(status_code=400, detail="Missing 'idea'")
    
    result = await orchestrate_feature_pipeline(idea)
    return result
