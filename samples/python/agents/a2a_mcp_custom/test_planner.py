import asyncio
import httpx
from uuid import uuid4

async def test_planner():
    print("Testing planner agent...")

    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {
            "jsonrpc": "2.0",
            "method": "message/send",
            "params": {
                "context_id": "test-ctx-" + str(uuid4()),
                "message": {
                    "messageId": "test-msg-" + str(uuid4()),
                    "role": "user",
                    "parts": [{"text": "Plan a simple trip to Paris"}]
                }
            },
            "id": "test-1"
        }

        print(f"Sending request to planner...")
        response = await client.post("http://localhost:10102/", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")

if __name__ == "__main__":
    asyncio.run(test_planner())
