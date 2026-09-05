#!/bin/bash

echo "=========================================="
echo "🚀 Starting Quantum Computing Agent"
echo "=========================================="
echo ""
echo "📋 Agent Information:"
echo "  🔹 Name: Quantum Computing Agent"
echo "  🔹 Port: 8003"
echo "  🔹 Model: Granite 4 Small H (Ollama)"
echo "  🔹 Role: Quantum Circuit Execution"
echo ""
echo "=========================================="
echo ""

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "⚠️  Warning: Port $1 is already in use"
        return 1
    fi
    return 0
}

# Check port before starting
echo "🔍 Checking port 8003..."
check_port 8003
echo ""

# Start Computing Agent
echo "🚀 Starting Quantum Computing Agent on port 8003..."
echo "📦 Using uv to run the agent..."
echo ""
uv run server

echo ""
echo "=========================================="
echo "✅ Quantum Computing Agent started!"
echo "=========================================="
echo ""
echo "📊 Agent Details:"
echo "  🔹 URL: http://127.0.0.1:8003"
echo "  🔹 Model: Granite 4 Small H (Ollama)"
echo "  🔹 Specialty: Circuit Execution on IBM Quantum"
echo ""
echo "=========================================="
echo ""
echo "💡 Tips:"
echo "  - This agent executes QASM/Qiskit code"
echo "  - Supports simulators and real quantum hardware"
echo "  - Automatic circuit transpilation"
echo "  - Press Ctrl+C to stop the agent"
echo ""
echo "=========================================="
