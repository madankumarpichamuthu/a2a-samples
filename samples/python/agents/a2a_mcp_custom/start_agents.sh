#!/bin/bash

# Script to start all A2A MCP agents for use with the HTML test client
# This keeps all agents running until you press Ctrl+C

set -e

WORK_DIR="."
LOG_DIR="logs"

# Cleanup function
cleanup() {
    echo ""
    echo "Shutting down all agents..."
    if [ ${#pids[@]} -ne 0 ]; then
        kill "${pids[@]}" 2>/dev/null
        wait "${pids[@]}" 2>/dev/null
    fi
    echo "All agents stopped."
}

trap cleanup EXIT INT TERM

# Create log directory
mkdir -p "$LOG_DIR"

echo "================================================"
echo "Starting A2A MCP Agents"
echo "================================================"
echo ""
echo "Make sure you have set GOOGLE_API_KEY in .env file"
echo ""

# Check if .env exists and has API key
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env file with your GOOGLE_API_KEY"
    exit 1
fi

if grep -q "your_api_key_here" .env; then
    echo "WARNING: Please update GOOGLE_API_KEY in .env file"
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Setting up Python virtual environment..."
~/.local/bin/uv venv
source .venv/bin/activate
echo "Virtual environment activated."
echo ""

echo "Upgrading dependencies (fixing a2a-sdk version)..."
~/.local/bin/uv pip install "a2a-sdk[sql]>=0.3.9" --upgrade
echo ""

pids=()

echo "Starting agents (logs in $LOG_DIR/)..."
echo ""

# 1. Start MCP Server
echo "[1/6] Starting MCP Server on port 10100..."
~/.local/bin/uv run --env-file .env a2a-mcp --run mcp-server --transport sse --port 10100 > "$LOG_DIR/mcp_server.log" 2>&1 &
pids+=($!)
sleep 2

# 2. Start Orchestrator Agent
echo "[2/6] Starting Orchestrator Agent on port 10101..."
~/.local/bin/uv run --env-file .env src/a2a_mcp/agents/ --agent-card agent_cards/orchestrator_agent.json --port 10101 > "$LOG_DIR/orchestrator_agent.log" 2>&1 &
pids+=($!)
sleep 2

# 3. Start Planner Agent
echo "[3/6] Starting Planner Agent on port 10102..."
~/.local/bin/uv run --env-file .env src/a2a_mcp/agents/ --agent-card agent_cards/planner_agent.json --port 10102 > "$LOG_DIR/planner_agent.log" 2>&1 &
pids+=($!)
sleep 2

# 4. Start Airline Ticketing Agent
echo "[4/6] Starting Air Ticketing Agent on port 10103..."
~/.local/bin/uv run --env-file .env src/a2a_mcp/agents/ --agent-card agent_cards/air_ticketing_agent.json --port 10103 > "$LOG_DIR/airline_agent.log" 2>&1 &
pids+=($!)
sleep 2

# 5. Start Hotel Booking Agent
echo "[5/6] Starting Hotel Booking Agent on port 10104..."
~/.local/bin/uv run --env-file .env src/a2a_mcp/agents/ --agent-card agent_cards/hotel_booking_agent.json --port 10104 > "$LOG_DIR/hotel_agent.log" 2>&1 &
pids+=($!)
sleep 2

# 6. Start Car Rental Agent
echo "[6/6] Starting Car Rental Agent on port 10105..."
~/.local/bin/uv run --env-file .env src/a2a_mcp/agents/ --agent-card agent_cards/car_rental_agent.json --port 10105 > "$LOG_DIR/car_rental_agent.log" 2>&1 &
pids+=($!)

echo ""
echo "================================================"
echo "All agents starting... waiting 5 seconds"
echo "================================================"
sleep 5

echo ""
echo "✓ All agents should now be running!"
echo ""
echo "Agent Status:"
echo "  • MCP Server:       http://localhost:10100"
echo "  • Orchestrator:     http://localhost:10101"
echo "  • Planner:          http://localhost:10102"
echo "  • Air Ticketing:    http://localhost:10103"
echo "  • Hotel Booking:    http://localhost:10104"
echo "  • Car Rental:       http://localhost:10105"
echo ""
echo "📝 Logs are in: $LOG_DIR/"
echo ""
echo "🌐 Open test_client.html in your browser to test"
echo ""
echo "Press Ctrl+C to stop all agents"
echo "================================================"
echo ""

# Wait forever (until interrupted)
while true; do
    sleep 1
done
