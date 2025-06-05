from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import httpx
import asyncio
from urllib.parse import urlparse
import logging

app = FastAPI()

# In-memory list of agent server URLs
agent_servers = set()

class AgentServerRegistration(BaseModel):
    url: str  # e.g., "http://agent_one:8000"

@app.post("/register_agent_server")
def register_agent_server(reg: AgentServerRegistration):
    parsed = urlparse(reg.url)
    if parsed.hostname in ("0.0.0.0", "localhost", "127.0.0.1"):
        return {"success": False, "error": "Invalid agent server address"}
    agent_servers.add(reg.url)
    return {"success": True, "registered": list(agent_servers)}

@app.get("/agents")
async def list_all_agents():
    """Return agents grouped by their server, with detailed logging."""
    logger = logging.getLogger("router_agent")

    agent_servers_list = []
    logger.info(f"Starting aggregation from agent servers: {agent_servers}")
    async with httpx.AsyncClient() as client:
        tasks = [client.get(f"{url}/agents") for url in agent_servers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for url, result in zip(agent_servers, results):
            logger.info(f"Processing server: {url}")
            if isinstance(result, Exception):
                logger.error(f"Error contacting {url}/agents: {result}")
                continue
            try:
                logger.info(f"Response from {url}/agents: {result.status_code}")
                data = result.json()
                logger.debug(f"Data from {url}/agents: {data}")
                if "agents" in data:
                    logger.info(f"Found {len(data['agents'])} agents at {url}")
                    agent_servers_list.append({
                        "server_url": url,
                        "agents": data["agents"]
                    })
                else:
                    logger.warning(f"No 'agents' key in response from {url}")
            except Exception as e:
                logger.error(f"Failed to process response from {url}: {e}")
                continue
    logger.info(f"Aggregated agent servers: {agent_servers_list}")
    return {"agent_servers": agent_servers_list} 