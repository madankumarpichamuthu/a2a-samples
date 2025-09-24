"""Simple HelloWorld agent with proper A2A method extension."""

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from simple_agent_executor import SimpleAgentExecutor
from simple_time_greeting_extension import SimpleTimeGreetingExtension


if __name__ == '__main__':
    # Create the simple time greeting extension
    time_greeting_extension = SimpleTimeGreetingExtension()
    
    # Basic hello world skill
    hello_skill = AgentSkill(
        id='hello_world',
        name='Returns hello world',
        description='Returns a simple hello world greeting',
        tags=['hello world'],
        examples=['hi', 'hello world'],
    )
    
    # Time greeting method skill
    time_skill = AgentSkill(
        id='time_greeting',
        name='Time-based greeting',
        description='Returns greeting appropriate for current time of day',
        tags=['greeting', 'time'],
        examples=['good morning', 'time greeting', 'what time greeting'],
    )
    
    # Create agent card with method extension
    agent_card = AgentCard(
        name='HelloWorld Agent with Simple Time Greeting',
        description='HelloWorld agent with simple time-based greeting method extension',
        url='http://localhost:9999/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(
            streaming=True,
            extensions=[time_greeting_extension.get_extension_metadata()]
        ),
        skills=[hello_skill, time_skill],
    )
    
    # Create request handler
    request_handler = DefaultRequestHandler(
        agent_executor=SimpleAgentExecutor(time_greeting_extension=time_greeting_extension),
        task_store=InMemoryTaskStore(),
    )
    
    # Create A2A server
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    
    print("Starting Simple HelloWorld Agent with Time Greeting Extension")
    print("Agent card: http://localhost:9999/.well-known/agent-card.json")
    print("JSON-RPC method: time-greeting")
    
    uvicorn.run(server.build(), host='0.0.0.0', port=9999)