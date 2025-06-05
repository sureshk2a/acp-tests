import asyncio

from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart


async def example() -> None:
    async with Client(base_url="http://localhost:8080") as client:
        run = await client.run_sync(
            agent="agent_one",
            input=[
                Message(
                    parts=[MessagePart(content="Howdy to agent_one from client!", content_type="text/plain")]
                )
            ],
        )
        print(run.output)


if __name__ == "__main__":
    asyncio.run(example())