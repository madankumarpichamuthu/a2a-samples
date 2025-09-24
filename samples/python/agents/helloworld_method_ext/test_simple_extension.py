"""Test script for the simple time greeting method extension."""

import asyncio
from unittest.mock import MagicMock
from simple_time_greeting_extension import SimpleTimeGreetingExtension
from simple_agent_executor import SimpleAgentExecutor


async def test_method_extension():
    """Test the simple time greeting method extension."""
    print("Testing Simple Time Greeting Method Extension...")
    
    # Test direct method call
    print("\n1. Testing direct method call...")
    extension = SimpleTimeGreetingExtension()
    
    result = extension.time_greeting({})
    print(f"   Default timezone: {result}")
    
    result = extension.time_greeting({"timezone": "America/New_York"})  
    print(f"   New York timezone: {result}")
    
    # Test extension metadata
    print("\n2. Testing extension metadata...")
    metadata = extension.get_extension_metadata()
    print(f"   Extension metadata: {metadata}")
    
    # Test agent executor integration
    print("\n3. Testing agent executor integration...")
    agent_executor = SimpleAgentExecutor(time_greeting_extension=extension)
    
    # Mock context for normal execution
    mock_context = MagicMock()
    mock_context.method_name = None
    
    async def mock_enqueue(message):
        print(f"   Mock event received (message type: {type(message).__name__})")
    
    mock_event_queue = MagicMock()
    mock_event_queue.enqueue_event = mock_enqueue
    
    print("   Testing normal agent execution...")
    await agent_executor.execute(mock_context, mock_event_queue)
    
    # Mock context for method call
    mock_context.method_name = "time-greeting"
    mock_context.method_params = {"timezone": "UTC"}
    
    print("   Testing method call execution...")
    await agent_executor.execute(mock_context, mock_event_queue)
    
    # Test supported methods
    methods = agent_executor.get_supported_methods()
    print(f"   Supported methods: {methods}")
    
    print("\nSimple method extension test completed!")


if __name__ == "__main__":
    asyncio.run(test_method_extension())