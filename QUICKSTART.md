# 🚀 Quick Start Guide - Quantum Computing Agent

## ⚡ Fast Setup (5 minutes)

### 1. Prerequisites
```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### 2. Clone & Configure
```bash
# Navigate to the project
cd quantum-computing-agent

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

### 3. Required Environment Variables
```env
# IBM Quantum Token (REQUIRED)
QISKIT_IBM_TOKEN=your_ibm_quantum_token_here

# Watsonx Credentials (REQUIRED)
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here

# Local Granite model
OLLAMA_API_BASE=http://127.0.0.1:11434
COMPUTING_MODEL=ollama:granite4.2:8b
COMPUTING_HOST=127.0.0.1
COMPUTING_PORT=8003
```

### 4. Run the Agent

**Option A: Using start script (Recommended)**
```bash
chmod +x start.sh
./start.sh
```

**Option B: Using uv directly**
```bash
uv run server
```

**Option C: Using Python**
```bash
uv sync
python -m quantum_computing_agent.agent
```

### 5. Verify Agent is Running
```bash
# Check agent card
curl http://localhost:8003/.well-known/agent-card.json

# Test with a simple circuit
curl -X POST http://localhost:8003/jsonrpc/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "kind": "message",
        "messageId": "7dc531b3-233a-489f-a4a4-1f42a53ef42c",
        "role": "user",
        "parts": [{"kind": "text", "text": "Execute this QASM code:\nOPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q -> c;"}]
      }
    }
  }'
```

## 🐳 Docker Quick Start

```bash
# Build
docker build -t quantum-computing-agent .

# Run
docker run -p 8003:8003 --env-file .env quantum-computing-agent

# Run in background
docker run -d -p 8003:8003 --env-file .env --name quantum-computing quantum-computing-agent
```

## 📝 Usage Examples

### Execute Bell State on Simulator
```bash
curl -X POST http://localhost:8003/jsonrpc/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "kind": "message",
        "messageId": "d62730b7-c0b7-4dae-9323-ed12f2e56b3c",
        "role": "user",
        "parts": [{"kind": "text", "text": "Execute this Bell state circuit on ibm_kyiv:\nOPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q -> c;"}]
      }
    }
  }'
```

### Execute on Real Quantum Hardware
```bash
curl -X POST http://localhost:8003/jsonrpc/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "kind": "message",
        "messageId": "1f9089ce-9ead-4e93-86c7-edd30237ad5f",
        "role": "user",
        "parts": [{"kind": "text", "text": "Execute this superposition circuit on ibm_brisbane (real hardware):\nOPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[3];\ncreg c[3];\nh q[0];\nh q[1];\nh q[2];\nmeasure q -> c;"}]
      }
    }
  }'
```

### Execute Qiskit Python Code
```bash
curl -X POST http://localhost:8003/jsonrpc/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "kind": "message",
        "messageId": "599dc9d0-dc5d-4266-a0ee-e008c1b075bb",
        "role": "user",
        "parts": [{"kind": "text", "text": "Execute this Qiskit code:\nfrom qiskit import QuantumCircuit\nqc = QuantumCircuit(2, 2)\nqc.h(0)\nqc.cx(0, 1)\nqc.measure_all()"}]
      }
    }
  }'
```

### Execute with Specific Backend
```bash
curl -X POST http://localhost:8003/jsonrpc/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "kind": "message",
        "messageId": "7d0b7669-e30e-4b4e-9a71-9f5e822526a7",
        "role": "user",
        "parts": [{"kind": "text", "text": "Execute this circuit on ibm_osaka:\nOPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q -> c;"}]
      }
    }
  }'
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8003
lsof -i :8003

# Kill the process
kill -9 <PID>
```

### Missing Dependencies
```bash
# Reinstall all dependencies
uv sync --reinstall
```

### IBM Quantum Connection Errors
- Verify your IBM Quantum token is correct
- Check you have access to IBM Quantum services
- Test connection: `python -c "from qiskit_ibm_runtime import QiskitRuntimeService; print(QiskitRuntimeService(token='YOUR_TOKEN').backends())"`

### Watsonx API Errors
- Verify your API key is correct
- Check project ID matches your Watsonx project
- For local inference, run `ollama pull granite4.2:8b`
- Check Watsonx service status

### Circuit Execution Errors
- **Invalid QASM**: Ensure code includes `OPENQASM 2.0;` and `include "qelib1.inc";`
- **Backend not found**: Use Status Agent to list available backends
- **Transpilation failed**: Circuit may be too complex, try a simpler version
- **Queue timeout**: Real hardware may have long queues, use simulator for testing

## 📚 What This Agent Does

✅ **Executes quantum circuits** - Runs QASM 2.0/3.0 and Qiskit code
✅ **Supports simulators** - Fast execution on quantum simulators
✅ **Real hardware access** - Execute on actual quantum computers
✅ **Auto transpilation** - Automatic circuit optimization for target backend
✅ **Job tracking** - Returns Job IDs for asynchronous result retrieval
✅ **Multiple backends** - Supports various IBM Quantum backends

## 🔗 Integration

This agent can work:
- **Standalone**: Direct HTTP requests
- **A2A Protocol**: Agent-to-Agent communication
- **Part of Quantum Lab System**: Orchestrated by main agent

## 🛠️ Supported Formats

1. **QASM 2.0** - OpenQASM 2.0 code
2. **QASM 3.0** - OpenQASM 3.0 code (converted to 2.0)
3. **Qiskit Python** - Qiskit QuantumCircuit code (auto-converted)

## 📊 Job Tracking

After execution, the agent returns a Job ID. Use the Status Agent (port 8002) to check results:

```bash
curl -X POST http://localhost:8002/jsonrpc/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "kind": "message",
        "messageId": "81d59919-f709-4497-9d47-9a1ad7409e9c",
        "role": "user",
        "parts": [{"kind": "text", "text": "What is the status of job YOUR_JOB_ID?"}]
      }
    }
  }'
```

## 🎯 Backend Selection

- **Simulators** (fast, free): `ibm_kyiv`, `simulator_statevector`
- **Real Hardware** (slow, queue): `ibm_brisbane`, `ibm_osaka`, `ibm_torino`

Use Status Agent to see all available backends and their queue status.

## 📖 Full Documentation

See [README.md](README.md) for complete documentation.

---
