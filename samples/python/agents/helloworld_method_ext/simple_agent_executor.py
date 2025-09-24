"""Simple Agent Executor with proper A2A method extension support."""

from typing import Optional
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from simple_time_greeting_extension import SimpleTimeGreetingExtension


class HelloWorldAgent:
    """Hello World Agent."""

    async def invoke(self) -> str:
        return 'Hello World'


class SimpleAgentExecutor(AgentExecutor):
    """Agent executor with proper method extension support."""

    def __init__(self, time_greeting_extension: Optional[SimpleTimeGreetingExtension] = None):
        self.agent = HelloWorldAgent()
        self.time_greeting_extension = time_greeting_extension

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute agent with method extension support."""
        
        # Check if this is a JSON-RPC method call for our extension
        if (self.time_greeting_extension and 
            hasattr(context, 'method_name') and 
            context.method_name == "time-greeting"):
            
            # Handle as JSON-RPC method call
            params = getattr(context, 'method_params', {})
            result = self.time_greeting_extension.time_greeting(params)
            
            if 'error' in result:
                # Return error response
                error_msg = result['error']['message']
                await event_queue.enqueue_event(new_agent_text_message(f"Error: {error_msg}"))
            else:
                # Return successful method result
                greeting_text = f"{result['greeting']} (It's {result['time_period']} time)"
                await event_queue.enqueue_event(new_agent_text_message(greeting_text))
        else:
            # Normal agent execution
            result = await self.agent.invoke()
            await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel execution."""
        raise Exception('cancel not supported')
    
    def get_supported_methods(self) -> list:
        """Return list of supported JSON-RPC methods."""
        if self.time_greeting_extension:
            return ["time-greeting"]
        return []