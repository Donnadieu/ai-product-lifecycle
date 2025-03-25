from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from stakeholder_agents import run_stakeholder_crew
from pm_agents import run_pm_crew
from engineering_agents import run_engineering_crew
from ticketing_agents import run_ticketing_crew
from feature_orchestrator import orchestrate_feature_pipeline
from fastapi import HTTPException
import os

load_dotenv()
client = OpenAI()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-stakeholder-requirements/")
async def generate_stakeholder_requirements(data: dict):
    idea = data.get("idea", "")
    if not idea:
        raise HTTPException(status_code=400, detail="Missing 'idea'")
    
    context = {
        "openai_api_key": os.getenv("OPENAI_API_KEY")
    }

    output = run_stakeholder_crew(idea, context)
    return {"output": output}

@app.post("/generate-pm-specs/")
async def generate_pm_specs(data: dict):
    idea = data.get("idea", "")
    if not idea:
        raise HTTPException(status_code=400, detail="Missing 'idea'")
    
    context = { "openai_api_key": os.getenv("OPENAI_API_KEY") }
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
