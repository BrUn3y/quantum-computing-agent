"""
Quantum Computing Agent - Specialist in Quantum Circuit Execution

This agent specializes in:
- Execute QASM/Qiskit code on IBM quantum computers
- Manage execution on simulators and real hardware
- Provide detailed information on executed jobs
- Automatic circuit transpilation

Model: mistralai/mistral-small-3-1-24b-instruct-2503 (Watsonx)
Port: 8003
Type: AgentStack Server with A2A (ReActAgent with IBMQuantumTool)
"""

from .tools import IBMQuantumTool

__all__ = ["IBMQuantumTool"]
__version__ = "1.0.0"
__author__ = "Edgar Bruney"
