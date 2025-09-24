# Hello World Method Extension Example

Hello World example agent enhanced with A2A protocol method extension demonstrating:
- **Time-Based Greeting Extension**: Contextually appropriate greetings based on current time of day

This agent extends the basic HelloWorld functionality with a method extension that showcases how agents can provide intelligent, time-aware responses using the A2A extension system.

## Extension Features

### Time-Based Greeting Extension
- **Smart Time Detection**: Automatically determines appropriate greeting based on current time
- **Multiple Time Periods**: dawn (5-7am), morning (7-12pm), noon (12pm), afternoon (1-6pm), evening (6-9pm), night (9-11pm), late_night (11pm-5am)
- **Timezone Support**: 20+ timezone options including UTC, GMT, major cities worldwide
- **Language Support**: English, Spanish, French, German, Japanese  
- **Greeting Styles**: casual, formal, brief
- **Time Display Options**: 12-hour or 24-hour format, optional time inclusion
- **Extension URI**: `http://localhost:8080/extensions/time-greeting/v1`
- **Method Name**: `greeting/time-based`

## Getting Started

1. Start the server

   ```bash
   uv run .
   ```

2. Run the test client

   ```bash
   uv run test_client.py
   ```

## Extension Usage Examples

### Natural Language Activation (Keyword-based)

1. **Basic time greetings**:
   - "time greeting"
   - "good morning"
   - "what time is it"

2. **With specific parameters**:
   - "time greeting in Tokyo"
   - "formal time greeting in Spanish"  
   - "good morning in 24 hour format"
   - "time greeting without time"

3. **Timezone-specific**:
   - "time greeting in New York"
   - "good afternoon in London"
   - "greet me based on time in Tokyo"

### A2A Extension Protocol Activation

Use proper A2A extension headers and metadata:

```bash
curl -X POST http://localhost:9999/ \
  -H "Content-Type: application/json" \
  -H "X-A2A-Extensions: http://localhost:8080/extensions/time-greeting/v1" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test",
    "method": "message/send",
    "params": {
      "message": {
        "kind": "message",
        "messageId": "msg-1",
        "parts": [{"kind": "text", "text": "Time greeting please"}],
        "role": "user",
        "metadata": {
          "extensions": {
            "http://localhost:8080/extensions/time-greeting/v1": {
              "timezone": "Asia/Tokyo",
              "style": "formal",
              "language": "ja",
              "format": "24h",
              "includeTime": true
            }
          }
        }
      }
    }
  }'
```

### Example Responses

- **Dawn (5-7am)**: "Good early morning! The sun is just rising. ☀️ It's currently 6:30 AM."
- **Noon**: "Good afternoon! Perfect time for lunch! 🌞 It's currently 12:00 PM."
- **Late Night**: "Good night! You're up quite late! 🌛 It's currently 11:45 PM."

## Supported Timezones

- **UTC/GMT**: UTC, GMT
- **Americas**: New_York, Los_Angeles, Chicago, Denver
- **Europe**: London, Paris, Berlin, Rome  
- **Asia**: Tokyo, Shanghai, Mumbai, Dubai
- **Pacific**: Sydney, Auckland

## Build Container Image

Agent can also be built using a container file.

1. Navigate to the directory `samples/python/agents/helloworld_method_ext` directory:

  ```bash
  cd samples/python/agents/helloworld_method_ext
  ```

2. Build the container file

    ```bash
    podman build . -t helloworld-method-ext-a2a-server
    ```

> [!Tip]  
> Podman is a drop-in replacement for `docker` which can also be used in these commands.

3. Run your container

    ```bash
    podman run -p 9999:9999 helloworld-method-ext-a2a-server
    ```

## Validate

To validate in a separate terminal, run the A2A client:

```bash
cd samples/python/hosts/cli
uv run . --agent http://localhost:9999
```

## Architecture Changes from Basic HelloWorld

### New Files Added
- `time_greeting_extension.py` - Method extension implementing time-based greetings
- `time_greeting_extension_spec.json` - Extension specification
- Extension server files for standalone operation

### Core Modifications  
- **`__main__.py`**:
  - Lines 14, 19: Import and initialize TimeGreetingExtension
  - Lines 38-51: Added TimeGreeting AgentSkill
  - Lines 69-74, 93-98: Extension metadata integration 
  - Lines 101-102: Pass extension to HelloWorldAgentExecutor

- **`agent_executor.py`**:
  - Lines 24-26: Constructor accepts time greeting extension
  - Lines 38-53: Enhanced execute method with time greeting activation
  - Lines 65-142: Extension activation logic and parameter extraction
  - Smart natural language parsing for timezone, style, and language detection
  - Comprehensive parameter mapping for proper A2A protocol support


## Disclaimer
Important: The sample code provided is for demonstration purposes and illustrates the mechanics of the Agent-to-Agent (A2A) protocol. When building production applications, it is critical to treat any agent operating outside of your direct control as a potentially untrusted entity.

All data received from an external agent—including but not limited to its AgentCard, messages, artifacts, and task statuses—should be handled as untrusted input. For example, a malicious agent could provide an AgentCard containing crafted data in its fields (e.g., description, name, skills.description). If this data is used without sanitization to construct prompts for a Large Language Model (LLM), it could expose your application to prompt injection attacks.  Failure to properly validate and sanitize this data before use can introduce security vulnerabilities into your application.

Developers are responsible for implementing appropriate security measures, such as input validation and secure handling of credentials to protect their systems and users.