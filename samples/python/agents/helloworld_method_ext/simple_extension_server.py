"""Simple extension server for method extension specification."""

import json
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities
from starlette.responses import JSONResponse
from starlette.routing import Route


async def get_extension_spec(request):
    """Serve the simple time greeting extension specification."""
    with open('simple_time_greeting_spec.json', 'r') as f:
        spec = json.load(f)
    return JSONResponse(spec)


class ExtensionAgentExecutor:
    """Minimal agent executor for extension documentation."""
    
    async def execute(self, context, event_queue):
        pass
        
    async def cancel(self, context, event_queue):
        pass


if __name__ == "__main__":
    extension_agent_card = AgentCard(
        name='Simple Time Greeting Extension Server',
        description='Hosts specification for the Simple Time Greeting method extension',
        url='http://localhost:8080/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=False),
        skills=[],
    )
    
    request_handler = DefaultRequestHandler(
        agent_executor=ExtensionAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    
    a2a_server = A2AStarletteApplication(
        agent_card=extension_agent_card,
        http_handler=request_handler,
    )
    
    app = a2a_server.build()
    app.router.routes.append(Route('/extensions/simple-time-greeting/v1', get_extension_spec))
    
    print("Starting Simple Time Greeting Extension Server on http://localhost:8080")
    print("Extension spec: http://localhost:8080/extensions/simple-time-greeting/v1")
    print("Agent card: http://localhost:8080/.well-known/agent-card.json")
    
    uvicorn.run(app, host="0.0.0.0", port=8080)