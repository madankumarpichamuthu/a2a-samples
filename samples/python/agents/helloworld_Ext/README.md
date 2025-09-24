# Hello World Extension Example

Hello World example agent enhanced with A2A protocol extensions demonstrating:
- **Greeting Style Extension**: Customizable greeting styles and languages
- **Random Method Extension**: Custom JSON-RPC method for random greeting generation

This agent extends the basic HelloWorld functionality with two extension types that showcase the A2A extension system capabilities.

## Extension Features

### 1. Greeting Style Extension
- **Multiple Styles**: casual, formal, enthusiastic, multilingual
- **Language Support**: English, Spanish, French, German, Japanese
- **Extension URI**: `http://localhost:8080/extensions/greeting-style/v1`
- **Activation**: Via `X-A2A-Extensions` header or keyword detection

### 2. Random Method Extension  
- **Custom Method**: `message/random` JSON-RPC method
- **Parameters**: `excludeStyles`, `excludeLanguages`, `seed` (optional)
- **Extension URI**: `http://localhost:8080/extensions/random-greeting-method/v1`
- **Features**: Reproducible results with seed, exclusion filters

## Getting Started

1. Start the server

   ```bash
   uv run .
   ```

2. Run the test client

   ```bash
   uv run test_client.py
   ```

## Testing Extensions

### Greeting Style Extension Examples

1. **Header-based activation** (proper A2A extension):
   ```bash
   curl -X POST http://localhost:9999/ \
     -H "Content-Type: application/json" \
     -H "X-A2A-Extensions: http://localhost:8080/extensions/greeting-style/v1" \
     -d '{
       "jsonrpc": "2.0",
       "id": "test",
       "method": "message/send",
       "params": {
         "message": {
           "kind": "message",
           "messageId": "msg-1",
           "parts": [{"kind": "text", "text": "Hello"}],
           "role": "user",
           "metadata": {
             "extensions": {
               "http://localhost:8080/extensions/greeting-style/v1": {
                 "style": "formal",
                 "language": "fr"
               }
             }
           }
         }
       }
     }'
   ```

2. **Keyword-based activation** (demo compatibility):
   - "formal greeting in French"
   - "enthusiastic hello in Japanese" 
   - "casual greeting in Spanish"
   - "multilingual greeting"

### Random Method Extension Examples

1. **Basic random greeting**:
   - "Generate a random greeting"
   - "Random hello"
   - "Surprise me with a greeting"

2. **With exclusions**:
   - "Random greeting, no formal style"
   - "Generate random hello, not in Spanish"

## Build Container Image

Agent can also be built using a container file.

1. Navigate to the directory `samples/python/agents/helloworld_Ext` directory:

  ```bash
  cd samples/python/agents/helloworld_Ext
  ```

2. Build the container file

    ```bash
    podman build . -t helloworld-ext-a2a-server
    ```

> [!Tip]  
> Podman is a drop-in replacement for `docker` which can also be used in these commands.

3. Run your container

    ```bash
    podman run -p 9999:9999 helloworld-ext-a2a-server
    ```

## Validate

To validate in a separate terminal, run the A2A client:

```bash
cd samples/python/hosts/cli
uv run . --agent http://localhost:9999
```

## Architecture Changes from Basic HelloWorld

### New Files Added
- `greeting_style_extension.py` - Greeting style extension implementation
- `random_method_extension.py` - Random method extension implementation  
- `extension_server.py` - Standalone extension server
- `grpc_main.py` & `grpc_agent_executor.py` - GRPC variants
- Extension specification files (JSON)

### Core Modifications
- **`__main__.py`**: Extension initialization and AgentCard enhancement
- **`agent_executor.py`**: Extension activation logic and parameter parsing
- **Enhanced AgentCard**: Extension metadata and capabilities registration


## Disclaimer
Important: The sample code provided is for demonstration purposes and illustrates the mechanics of the Agent-to-Agent (A2A) protocol. When building production applications, it is critical to treat any agent operating outside of your direct control as a potentially untrusted entity.

All data received from an external agent—including but not limited to its AgentCard, messages, artifacts, and task statuses—should be handled as untrusted input. For example, a malicious agent could provide an AgentCard containing crafted data in its fields (e.g., description, name, skills.description). If this data is used without sanitization to construct prompts for a Large Language Model (LLM), it could expose your application to prompt injection attacks.  Failure to properly validate and sanitize this data before use can introduce security vulnerabilities into your application.

Developers are responsible for implementing appropriate security measures, such as input validation and secure handling of credentials to protect their systems and users.