import asyncio
import httpx
from uuid import uuid4

async def test_orchestrator():
    print("Testing orchestrator with the queue closure fix...")

    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "jsonrpc": "2.0",
            "method": "message/send",
            "params": {
                "context_id": "test-ctx-" + str(uuid4()),
                "message": {
                    "messageId": "test-msg-" + str(uuid4()),
                    "role": "user",
                    "parts": [{"text": "Plan a 3-day trip to Paris"}]
                }
            },
            "id": "test-orchestrator-1"
        }

        print(f"Sending request to orchestrator on port 10101...")
        response = await client.post("http://localhost:10101/", json=payload)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ SUCCESS: Orchestrator responded!")
            response_json = response.json()
            print(f"Response preview: {str(response_json)[:500]}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response: {response.text[:500]}")

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
