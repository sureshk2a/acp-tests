import os
import asyncio
from collections.abc import AsyncGenerator
import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager
from acp_sdk.models import Message
from acp_sdk.server import Context, RunYield, RunYieldResume, Server
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent_one")

server = Server()

agent_host = os.environ.get("AGENT_HOST")
agent_port = int(os.environ.get("AGENT_PORT"))
agent_url = f"http://{agent_host}:{agent_port}"

async def register_agent_server():
    logger.info(f"Attempting to register agent server at {agent_url} with router...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://192.168.0.105:8001/register_agent_server",
                json={"url": agent_url}
            )
            logger.info(f"Registration response: {response.status_code} {response.text}")
        except Exception as e:
            import traceback
            logger.error(f"Failed to register agent server: {e}")
            traceback.print_exc()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Agent URL: {agent_url}")
    logger.info("Starting up and registering agent server...")
    await register_agent_server()
    logger.info("Agent server registration complete. Application startup continuing...")
    yield
    logger.info("Application shutdown sequence initiated.")

server.lifespan = lifespan

@server.agent(
    name="agent_one",
    description="Echo agent",
    metadata={
        "capabilities": [
            {"name": "echo", "description": "Echoes all input messages back to the sender."},
            {"name": "respond_to_messages", "description": "Responds to any message with the same content."}
        ]
    }
)
async def agent_one(
    input: list[Message], context: Context
) -> AsyncGenerator[RunYield, RunYieldResume]:
    logger.info(f"agent_one invoked with {len(input)} messages.")
    for message in input:
        await asyncio.sleep(0.5)
        yield {"thought": "I should echo everything"}
        await asyncio.sleep(0.5)
        yield message

logger.info(f"Running agent_one server on 0.0.0.0:8000...")
server.run(host="0.0.0.0", port=8000)