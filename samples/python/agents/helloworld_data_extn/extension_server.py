#!/usr/bin/env python3
"""A2A-compliant extension server to host the basic logging extension specification."""

import json
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities
from starlette.responses import JSONResponse
from starlette.routing import Route


async def get_extension_spec(request):
    """Serve the basic logging extension specification."""
    with open('basic_logging_extension_spec.json', 'r') as f:
        spec = json.load(f)
    return JSONResponse(spec)


async def get_extension_docs(request):
    """Serve basic documentation for the extension."""
    docs = {
        "extension": "Basic Request Logging",
        "version": "1.0.0",
        "description": "Simple request tracking with timestamps and processing time",
        "activation": "Always active when extension is present",
        "log_format": {
            "timestamp": "ISO 8601 timestamp",
            "request_id": "Unique request identifier", 
            "processing_time_ms": "Processing time in milliseconds",
            "status": "success or error"
        },
        "example_log": "[2025-08-27T21:06:15.026377+00:00] msg-123 completed in 15ms - success"
    }
    return JSONResponse(docs)


class ExtensionAgentExecutor:
    """Minimal agent executor for extension documentation."""
    
    async def execute(self, context, event_queue):
        pass
        
    async def cancel(self, context, event_queue):
        pass


if __name__ == "__main__":
    extension_agent_card = AgentCard(
        name='Basic Logging Extension Server',
        description='Hosts specification and documentation for the Basic Logging extension',
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
    
    # Add extension routes
    app.router.routes.append(Route('/extensions/basic-logging/v1', get_extension_spec))
    app.router.routes.append(Route('/extensions/basic-logging/v1/docs', get_extension_docs))
    
    print("Starting A2A extension server on http://localhost:8080")
    print("Extension spec: http://localhost:8080/extensions/basic-logging/v1")
    print("Extension docs: http://localhost:8080/extensions/basic-logging/v1/docs")
    print("Agent card: http://localhost:8080/.well-known/agent-card.json")
    
    uvicorn.run(app, host="0.0.0.0", port=8080)