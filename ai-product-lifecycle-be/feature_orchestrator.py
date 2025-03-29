import httpx
import asyncio
from fastapi import HTTPException
from typing import Dict, Any

def handle_response(response: httpx.Response, step: str) -> Dict[str, Any]:
    """Handle API response and extract output safely"""
    try:
        if response.status_code != 200:
            error_detail = response.json().get('detail', f'Error in {step}')
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        
        data = response.json()
        if not isinstance(data, dict) or 'output' not in data:
            raise HTTPException(status_code=500, detail=f'Invalid response format in {step}')
        
        return data['output']
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f'HTTP error in {step}: {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error processing {step}: {str(e)}')

async def orchestrate_feature_pipeline(idea: str) -> dict:
    try:
        # Use relative URLs since we're calling endpoints within the same app
        async with httpx.AsyncClient() as client:
            # Generate stakeholder requirements
            # Generate stakeholder requirements
            r1 = await client.post("http://localhost:8000/generate-stakeholder-requirements/", json={"idea": idea})
            stakeholder = handle_response(r1, "stakeholder requirements")

            # Generate PM specifications
            r2 = await client.post("http://localhost:8000/generate-pm-specs/", json={"idea": stakeholder})
            prd = handle_response(r2, "PM specifications")

            # Generate engineering plan
            r3 = await client.post("http://localhost:8000/generate-engineering-plan/", json={"prd": prd})
            eng = handle_response(r3, "engineering plan")

            # Generate tickets
            r4 = await client.post("http://localhost:8000/generate-tickets/", json={"plan": eng})
            tickets = handle_response(r4, "tickets")

        return {
            "stakeholder": stakeholder,
            "prd": prd,
            "engineering": eng,
            "tickets": tickets
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")
