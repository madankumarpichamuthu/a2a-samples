# A2A MCP HTML Test Client

A beautiful, interactive single-page test client for the A2A MCP multi-agent system.

## Quick Start

### 1. Set up your API key

Edit the `.env` file and add your Google API key:

```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

Get your API key from: https://aistudio.google.com/app/apikey

### 2. Start all agents

```bash
cd samples/python/agents/a2a_mcp
./start_agents.sh
```

This will start all 6 agents:
- MCP Server (port 10100)
- Orchestrator Agent (port 10101)
- Planner Agent (port 10102)
- Air Ticketing Agent (port 10103)
- Hotel Booking Agent (port 10104)
- Car Rental Agent (port 10105)

**Keep this terminal open** - the agents will run until you press Ctrl+C.

### 3. Open the test client

Open `test_client.html` in your browser:

```bash
open test_client.html
```

Or simply double-click the file.

### 4. Test the connection

1. Click the **"Test Connection"** button
2. The status indicator should turn green
3. You should see a system message confirming connection

### 5. Start chatting!

**Try one of the example queries:**
- Click on any example in the sidebar
- Or type your own travel planning request

**Example queries:**
```
Plan a business trip from San Francisco to London for June 1-7, budget $5000
I need to travel to Paris for a conference, 2 travelers, July 15-20
Book a vacation to Tokyo, departing from New York, staying 5 nights
```

## How It Works

The test client:
1. Sends your query to the **Orchestrator Agent**
2. Orchestrator discovers and calls the **Planner Agent** via MCP
3. Planner breaks down your request into tasks
4. Orchestrator finds the right agents (Air/Hotel/Car) via MCP semantic search
5. Each specialist agent executes their task using MCP tools to query the database
6. Orchestrator collects results and generates a summary

You'll see:
- Real-time messages in the chat
- Task progress in the sidebar
- Agent status indicators
- Final travel plan summary

## Features

### Chat Interface
- User messages (purple)
- Agent responses (pink)
- System messages (blue)
- Error messages (red)

### Sidebar Features
- **Example Queries**: Click to use pre-made queries
- **Expected Agents**: Shows connection status for all agents
- **Current Tasks**: Real-time task tracking with status

### Quick Actions
- **Clear Chat**: Reset the conversation
- **Test Connection**: Verify orchestrator is running
- **New Session**: Start fresh with a new session ID

## Troubleshooting

### "Connection failed" error

**Cause**: Agents aren't running

**Fix**:
```bash
# In a terminal, run:
cd samples/python/agents/a2a_mcp
./start_agents.sh
```

### "Failed to fetch" error

**Cause**: CORS or agent not responding

**Fix**:
1. Check that all agents started successfully
2. Look at logs in `logs/` directory:
   ```bash
   tail -f logs/orchestrator_agent.log
   ```
3. Make sure no other process is using ports 10100-10105

### No API key error

**Fix**: Update `.env` file with your Google API key:
```bash
GOOGLE_API_KEY=your_actual_key_here
```

### Agents won't start

**Fix**: Make sure you have `uv` installed:
```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

## Viewing Logs

All agent logs are in the `logs/` directory:

```bash
# View all logs
ls -la logs/

# Tail orchestrator log
tail -f logs/orchestrator_agent.log

# Check MCP server log
tail -f logs/mcp_server.log

# View all logs at once
tail -f logs/*.log
```

## Stopping the Agents

Press **Ctrl+C** in the terminal where `start_agents.sh` is running.

All agents will shut down gracefully.

## Architecture

```
Browser (test_client.html)
    ↓ HTTP/JSON-RPC
Orchestrator Agent (10101)
    ↓ A2A Protocol
    ├─→ MCP Server (10100) [Agent Discovery + Tools]
    ├─→ Planner Agent (10102) [Task Breakdown]
    ├─→ Air Ticketing Agent (10103) [Flight Booking]
    ├─→ Hotel Booking Agent (10104) [Hotel Booking]
    └─→ Car Rental Agent (10105) [Car Rental]
```

## Technical Details

- **Protocol**: A2A (Agent-to-Agent) JSON-RPC 2.0
- **Agent Discovery**: MCP semantic search with embeddings
- **Communication**: HTTP + Server-Sent Events (SSE) for streaming
- **Database**: SQLite (`travel_agency.db`)
- **LLM**: Google Gemini 2.0 Flash

## Files

- `test_client.html` - The HTML test client (this file)
- `start_agents.sh` - Script to start all agents
- `.env` - Environment configuration (API keys)
- `logs/` - Agent log files
- `agent_cards/` - Agent capability declarations
- `travel_agency.db` - Sample travel data

## Learn More

- [A2A Protocol Documentation](https://github.com/a2aproject/A2A)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Google Gemini API](https://ai.google.dev/)

## License

Same as the parent a2a-samples repository.
