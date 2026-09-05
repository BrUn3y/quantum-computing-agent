# ⚡ Quantum Computing Agent

Specialist agent in quantum circuit execution on IBM Quantum infrastructure.

## 🎯 Overview

The Quantum Computing Agent executes quantum circuits (QASM and Qiskit code) on IBM Quantum simulators and real quantum hardware, managing automatic transpilation and providing Job IDs for result tracking.

### Key Features

- 🔬 **Circuit Execution**: Runs QASM 2.0/3.0 and Qiskit code on IBM Quantum
- 🖥️ **Simulator Support**: Execute on fast quantum simulators
- ⚛️ **Real Hardware**: Execute on actual quantum computers
- 🔄 **Auto Transpilation**: Automatic circuit optimization for target backend
- 📊 **Job Tracking**: Returns Job IDs for asynchronous result retrieval

## 🏗️ Architecture

- **Model**: Granite 4.2 8B via Ollama (`ollama:granite4.2:8b`)
- **Port**: 8003
- **Type**: AgentStack Server with A2A protocol
- **Tools**: IBMQuantumTool (circuit executor)
- **Framework**: BeeAI + Granite/Ollama + Qiskit + A2A

## 📋 Prerequisites

- Python 3.11+
- IBM Quantum account ([Get one here](https://quantum.cloud.ibm.com/))
- Ollama with `granite4.2:8b` (Watsonx remains an optional fallback)

## 📦 Project Dependencies

### Main Dependencies (pyproject.toml)

```toml
[project]
requires-python = ">=3.11,<4.0"
dependencies = [
    "agentstack-sdk==0.4.0rc1",      # Framework for creating agents
    "beeai_framework>=0.1.76",        # BeeAI Framework for agents
    "qiskit>=1.0.0",                  # IBM Quantum SDK
    "qiskit-ibm-runtime>=0.20.0",    # IBM Quantum Runtime
    "python-dotenv>=1.0.0",           # Environment variable management
]
```

### System Dependencies

1. **Python 3.11+**
   ```bash
   python --version  # Must be 3.11 or higher
   ```

2. **uv** (Package Manager - Recommended)
   ```bash
   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Verify installation
   uv --version
   ```

3. **IBM Watsonx** (Credentials required)
   - Watsonx API Key
   - Watsonx Project ID
   - Get them at: https://cloud.ibm.com/

4. **IBM Quantum** (Credentials required)
   - IBM Quantum Token
   - Get it at: https://quantum.ibm.com/

## 🎯 Specific Purpose

This agent is the **circuit execution specialist** of the multi-agent system:

**Responsibilities:**
- ✅ Execute QASM 2.0/3.0 code on IBM Quantum
- ✅ Execute Qiskit code on simulators and real hardware
- ✅ Automatically transpile circuits for specific backends
- ✅ Manage execution parameters (shots, backend, optimization)
- ✅ Return Job IDs for asynchronous tracking
- ✅ Handle execution and transpilation errors

**Does NOT:**
- ❌ Does not generate quantum code (use Developer Agent for that)
- ❌ Does not query job results (use Status Agent for that)
- ❌ Does not list available backends (use Status Agent for that)
- ❌ Only executes, does not query or generate

**Communication:**
- Receives requests via A2A from Operations Agent (port 8000)
- Responds with Job ID, backend used, and execution details
- Can be invoked directly on port 8003

**Available tool:**
- `IBMQuantumTool` - Executes circuits on IBM Quantum

**Supported backends:**
- **Simulators**: ibm_kyiv, ibm_sherbrooke, simulator_statevector
- **Real Hardware**: ibm_brisbane, ibm_osaka, ibm_torino, ibm_kyoto

- `uv` package manager (recommended) or `pip`

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd quantum-computing-agent

# Install dependencies
uv sync
# or
pip install -e .
```

### 2. Configure Environment

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# IBM Quantum
QISKIT_IBM_TOKEN=your_ibm_quantum_token_here

# Watsonx
WATSONX_API_KEY=your_watsonx_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_API_URL=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29

# Computing Agent Configuration
OLLAMA_API_BASE=http://127.0.0.1:11434
COMPUTING_MODEL=ollama:granite4.2:8b
COMPUTING_HOST=127.0.0.1
COMPUTING_PORT=8003
```

### 3. Start the Agent

**Option A: Using the start script (recommended)**
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
python -m quantum_computing_agent.agent
```

### 4. Verify Agent is Running

```bash
curl http://localhost:8003/.well-known/agent-card.json
```

## 💬 Usage Examples

### Example 1: Execute Bell State on Simulator

```bash
curl -X POST http://localhost:8003 \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{
      "role": "user",
      "content": "Execute this QASM code on ibm_kyiv:\nOPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q -> c;"
    }]
  }'
```

**Response includes:**
- Job ID for tracking
- Backend used (ibm_kyiv)
- Transpilation details
- Execution confirmation

### Example 2: Execute on Real Quantum Hardware

```bash
curl -X POST http://localhost:8003 \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{
      "role": "user",
      "content": "Execute this circuit on ibm_brisbane (real hardware):\nOPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[3];\ncreg c[3];\nh q[0];\nh q[1];\nh q[2];\nmeasure q -> c;"
    }]
  }'
```

**Response includes:**
- Job ID (critical for real hardware)
- Confirmation of real hardware execution
- Queue position (if applicable)
- Instructions to check results later

### Example 3: Execute Qiskit Python Code

```bash
curl -X POST http://localhost:8003 \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{
      "role": "user",
      "content": "Execute this Qiskit code:\nfrom qiskit import QuantumCircuit\nqc = QuantumCircuit(2, 2)\nqc.h(0)\nqc.cx(0, 1)\nqc.measure_all()"
    }]
  }'
```

**What happens:**
1. Agent detects Qiskit Python code
2. Converts to QASM automatically
3. Transpiles for target backend
4. Executes and returns Job ID

## 🔧 Tool: IBMQuantumTool

The agent uses a single powerful tool for circuit execution:

### Parameters

- `qasm_code` (required): QASM 2.0/3.0 or Qiskit Python code
- `use_real_device` (optional): `true` for real hardware, `false` for simulator
- `backend_name` (optional): Specific backend (e.g., "ibm_brisbane")
- `wait_for_results` (optional): `true` to wait for completion
- `max_wait_time` (optional): Maximum wait time in seconds (default: 300)

### Supported Backends

**Simulators:**
- `ibm_kyiv` - Fast simulator
- `ibmq_qasm_simulator` - QASM simulator
- `simulator_statevector` - Statevector simulator

**Real Hardware:**
- `ibm_brisbane` - 127 qubits
- `ibm_osaka` - 127 qubits
- `ibm_torino` - 133 qubits
- And more...

## 🔄 Transpilation

The agent automatically transpiles circuits for the target backend:

1. **Optimization**: Reduces gates and circuit depth
2. **Mapping**: Maps logical qubits to physical qubits
3. **Basis Gates**: Converts to backend-supported gates
4. **Connectivity**: Respects backend topology

**Optimization Level:** 3 (maximum optimization)

## 🔗 Integration with Other Agents

This agent is designed to work as part of the Quantum Lab Agent System:

- **Invoked by**: Quantum Lab Agent (Port 8000)
- **Communication**: A2A protocol (Agent-to-Agent)
- **Purpose**: Execute quantum circuits when requested by the orchestrator

### Standalone Usage

While designed for A2A communication, the agent can also be used standalone:

```python
import requests

qasm_code = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;
"""

response = requests.post(
    "http://localhost:8003",
    json={
        "messages": [{
            "role": "user",
            "content": f"Execute this circuit: {qasm_code}"
        }]
    }
)

print(response.json())
```

## 📊 Job Tracking

After execution, use the Job ID to check results:

```bash
# The Job ID is returned in the response
# Use the Status Agent (port 8002) to check results:
curl -X POST http://localhost:8002 \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{
      "role": "user",
      "content": "What is the status of job abc123xyz?"
    }]
  }'
```

## 🐛 Troubleshooting

### Agent Won't Start

**Problem:** Port already in use

```bash
lsof -i :8003
kill -9 <PID>
```

**Problem:** Missing dependencies

```bash
uv sync --reinstall
```

### Execution Errors

**Problem:** IBM Quantum connection errors

- Verify your IBM Quantum token in `.env`
- Check if you have access to the backend
- Try using a simulator instead

**Problem:** Transpilation errors

- Circuit may be too complex for the backend
- Try a simpler circuit or different backend
- Use a simulator for testing

### Code Format Issues

**Problem:** "Invalid QASM code"

- Ensure QASM includes `OPENQASM 2.0;` and `include "qelib1.inc";`
- Verify all qubits are defined before use
- Include measurements

## 🔗 Related Repositories

This agent is part of the Quantum Computing Multi-Agent System. Here are the related repositories:

- **[Quantum Computing Agent](https://github.com/BrUn3y/quantum-computing-agent)** - Circuit execution specialist (this repository)
- **[Quantum Status Agent](https://github.com/BrUn3y/quantum-status-agent)** - Status monitoring and job tracking
- **[Quantum Developer Agent](https://github.com/BrUn3y/quantum-developer-agent)** - Code generation and algorithm implementation
- **[Quantum Operations Agent](https://github.com/BrUn3y/quantum-lab-agent)** - Main orchestrator coordinating all agents

## 📚 Additional Resources

- [BeeAI Framework Documentation](https://github.com/i-am-bee/beeai-framework)
- [IBM Quantum Documentation](https://docs.quantum.ibm.com/)
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Watsonx Documentation](https://www.ibm.com/products/watsonx-ai)

## 🤝 Contributing

This agent is part of the Quantum Lab Agent System. For contributions, please refer to the main system repository.

## 📄 License

Apache 2.0 License

## 🙏 Acknowledgments

- Built with [BeeAI Framework](https://github.com/i-am-bee/beeai-framework)
- Powered by [IBM Watsonx](https://www.ibm.com/products/watsonx-ai)
- Quantum computing via [IBM Quantum](https://quantum.ibm.com/)
- LLM: Granite 4.2 8B via Ollama

---

**Made with ❤️ using BeeAI, Qiskit, and IBM Quantum**
