from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from typing import Optional

from basic_logging_extension import BasicLoggingExtension


# --8<-- [start:HelloWorldAgent]
class HelloWorldAgent:
    """Hello World Agent."""

    async def invoke(self) -> str:
        return 'Hello World'


# --8<-- [end:HelloWorldAgent]


# --8<-- [start:HelloWorldAgentExecutor_init]
class HelloWorldAgentExecutor(AgentExecutor):
    """Test AgentProxy Implementation."""

    def __init__(self, logging_extension: Optional[BasicLoggingExtension] = None):
        self.agent = HelloWorldAgent()
        self.logging_extension = logging_extension

    # --8<-- [end:HelloWorldAgentExecutor_init]
    # --8<-- [start:HelloWorldAgentExecutor_execute]
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        log_context = None
        
        if self._is_logging_extension_active(context):
            request_id = getattr(context.message, 'messageId', None)
            log_context = self.logging_extension.start_request(request_id)
        
        try:
            result = await self.agent.invoke()
            await event_queue.enqueue_event(new_agent_text_message(result))
            
            if log_context:
                self.logging_extension.log_completion(log_context, "success")
                
        except Exception:
            if log_context:
                self.logging_extension.log_completion(log_context, "error")
            raise

    # --8<-- [end:HelloWorldAgentExecutor_execute]
    
    def _is_logging_extension_active(self, context: RequestContext) -> bool:
        """Check if logging extension is active."""
        return self.logging_extension is not None

    # --8<-- [start:HelloWorldAgentExecutor_cancel]
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')

    # --8<-- [end:HelloWorldAgentExecutor_cancel]
