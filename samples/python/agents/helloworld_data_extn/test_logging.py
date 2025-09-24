#!/usr/bin/env python3
"""Test script for the basic logging extension."""

import time
import asyncio
from unittest.mock import MagicMock

from basic_logging_extension import BasicLoggingExtension
from agent_executor import HelloWorldAgentExecutor


async def test_logging_extension():
    """Test the basic logging extension."""
    print("Testing Basic Logging Extension...")
    
    logging_ext = BasicLoggingExtension()
    agent_executor = HelloWorldAgentExecutor(logging_extension=logging_ext)
    
    mock_context = MagicMock()
    mock_context.message.messageId = "test-msg-123"
    mock_event_queue = MagicMock()
    mock_event_queue.enqueue_event = MagicMock(return_value=asyncio.sleep(0))
    
    print("\n1. Testing successful request...")
    await agent_executor.execute(mock_context, mock_event_queue)
    
    print("\n2. Testing error handling...")
    agent_executor.agent.invoke = lambda: exec('raise Exception("Test error")')
    
    try:
        await agent_executor.execute(mock_context, mock_event_queue)
    except Exception as e:
        print(f"   Caught expected error: {e}")
    
    print("\n3. Testing direct extension usage...")
    context = logging_ext.start_request("direct-test-456")
    time.sleep(0.1)
    logging_ext.log_completion(context, "success")
    
    print("\nLogging test completed!")


if __name__ == "__main__":
    asyncio.run(test_logging_extension())