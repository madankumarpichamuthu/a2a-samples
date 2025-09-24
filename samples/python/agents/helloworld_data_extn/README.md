# Hello World Data Extension Example

Hello World example agent enhanced with A2A protocol data extension demonstrating:
- **Basic Logging Extension**: Request tracking with timestamps and processing metrics

This agent extends the basic HelloWorld functionality with a data extension that showcases how agents can collect and track operational data using the A2A extension system.

## Extension Features

### Basic Logging Extension
- **Request Tracking**: Automatic tracking of incoming requests with unique IDs
- **Processing Metrics**: Measures and logs processing time in milliseconds
- **Status Monitoring**: Tracks completion status (success/error)
- **Extension URI**: `http://localhost:8080/extensions/basic-logging/v1`
- **Extension Type**: Data extension (non-interactive)

## Getting Started

1. Start the server

   ```bash
   uv run .
   ```

2. Run the test client

   ```bash
   uv run test_client.py
   ```

## Extension Behavior

The logging extension automatically tracks all requests and outputs log entries like:
```
[2024-01-15T10:30:45.123456Z] req_a1b2c3d4 completed in 15ms - success
```

Each log entry includes:
- **Timestamp**: ISO 8601 formatted timestamp with timezone
- **Request ID**: Unique identifier (from message or auto-generated)
- **Processing Time**: Execution time in milliseconds  
- **Status**: Completion status (success/error)

## Testing the Extension

1. **Basic request logging**:
   ```bash
   uv run test_client.py
   ```

2. **Custom logging test**:
   ```bash
   uv run test_logging.py
   ```

## Build Container Image

Agent can also be built using a container file.

1. Navigate to the directory `samples/python/agents/helloworld_data_extn` directory:

  ```bash
  cd samples/python/agents/helloworld_data_extn
  ```

2. Build the container file

    ```bash
    podman build . -t helloworld-data-extn-a2a-server
    ```

> [!Tip]  
> Podman is a drop-in replacement for `docker` which can also be used in these commands.

3. Run your container

    ```bash
    podman run -p 9999:9999 helloworld-data-extn-a2a-server
    ```

## Validate

To validate in a separate terminal, run the A2A client:

```bash
cd samples/python/hosts/cli
uv run . --agent http://localhost:9999
```

## Architecture Changes from Basic HelloWorld

### New Files Added
- `basic_logging_extension.py` - Data extension for request logging and metrics
- `test_logging.py` - Specific test for logging functionality

### Core Modifications
- **`__main__.py`**: 
  - Lines 14, 19: Import and initialize BasicLoggingExtension
  - Line 43: Updated description to mention logging extension
  - Line 50: Added extension metadata to AgentCapabilities
  - Line 74: Pass logging extension to HelloWorldAgentExecutor

- **`agent_executor.py`**:
  - Lines 24-26: Constructor accepts logging extension parameter  
  - Lines 35-51: Enhanced execute method with request tracking
  - Lines 55-57: Helper method to check if logging is active
  - Automatic start/completion logging for all requests


## Disclaimer
Important: The sample code provided is for demonstration purposes and illustrates the mechanics of the Agent-to-Agent (A2A) protocol. When building production applications, it is critical to treat any agent operating outside of your direct control as a potentially untrusted entity.

All data received from an external agent—including but not limited to its AgentCard, messages, artifacts, and task statuses—should be handled as untrusted input. For example, a malicious agent could provide an AgentCard containing crafted data in its fields (e.g., description, name, skills.description). If this data is used without sanitization to construct prompts for a Large Language Model (LLM), it could expose your application to prompt injection attacks.  Failure to properly validate and sanitize this data before use can introduce security vulnerabilities into your application.

Developers are responsible for implementing appropriate security measures, such as input validation and secure handling of credentials to protect their systems and users.