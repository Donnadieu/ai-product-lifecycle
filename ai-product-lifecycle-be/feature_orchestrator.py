import httpx
import asyncio

async def orchestrate_feature_pipeline(idea: str) -> dict:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        r1 = await client.post("/generate-stakeholder-requirements/", json={"idea": idea})
        stakeholder = r1.json()["output"]

        r2 = await client.post("/generate-pm-specs/", json={"idea": stakeholder})
        prd = r2.json()["output"]

        r3 = await client.post("/generate-engineering-plan/", json={"prd": prd})
        eng = r3.json()["output"]

        r4 = await client.post("/generate-tickets/", json={"plan": eng})
        tickets = r4.json()["output"]

    return {
        "stakeholder": stakeholder,
        "prd": prd,
        "engineering": eng,
        "tickets": tickets
    }
