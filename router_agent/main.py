from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from urllib.parse import urlparse
import logging

app = FastAPI()

# In-memory storage for agent servers with their metadata
agent_servers_info = {}

class AgentServerRegistration(BaseModel):
    url: str  # e.g., "http://agent_one:8000"
    metadata: Dict[str, Any]

@app.post("/register_agent_server")
def register_agent_server(reg: AgentServerRegistration):
    parsed = urlparse(reg.url)
    if parsed.hostname in ("0.0.0.0", "localhost", "127.0.0.1"):
        return {"success": False, "error": "Invalid agent server address"}
    
    # Store both URL and metadata
    agent_servers_info[reg.url] = reg.metadata
    return {
        "success": True, 
        "registered": {
            "url": reg.url,
            "metadata": reg.metadata
        }
    }

@app.get("/list_agents")
async def list_all_agents():
    """Return all registered agents with their metadata"""
    logger = logging.getLogger("router_agent")
    
    agent_servers_list = []
    for url, metadata in agent_servers_info.items():
        logger.info(f"Processing server: {url}")
        server_info = {
            "server_url": url,
            "metadata": metadata
        }
        agent_servers_list.append(server_info)
    
    logger.info(f"Returning {len(agent_servers_list)} agent servers")
    return {"agent_servers": agent_servers_list} 