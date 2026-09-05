import unittest

from quantum_computing_agent.agent import _execution_parameters
from quantum_computing_agent.tools.quantum_tool import IBMQuantumTool


BELL_QASM = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;
"""


class ExecutionParameterTests(unittest.TestCase):
    def test_internal_policy_does_not_force_hardware(self):
        request = (
            "Create a Bell state on the simulator\n\n"
            "Execute exactly once. If the user requested real hardware, select a real backend."
        )
        parameters = _execution_parameters(request)
        self.assertFalse(parameters["use_real_device"])
        self.assertEqual(parameters["job_tags"], ["quantum-lab", "bell-state"])

    def test_named_backend_and_shots(self):
        parameters = _execution_parameters("Run a CX circuit on ibm_fez with 256 shots")
        self.assertTrue(parameters["use_real_device"])
        self.assertEqual(parameters["backend_name"], "ibm_fez")
        self.assertEqual(parameters["shots"], 256)
        self.assertEqual(parameters["job_tags"], ["quantum-lab", "cx-gate"])

    def test_least_busy_real_ibm_quantum_backend_is_hardware(self):
        parameters = _execution_parameters(
            "Create a Bell state and execute it once on the least busy real IBM Quantum backend"
        )
        self.assertTrue(parameters["use_real_device"])
        self.assertEqual(parameters["backend_name"], "")

    def test_quantum_machine_in_spanish_defaults_to_real_hardware(self):
        parameters = _execution_parameters(
            "dame un ejemplo del algoritmo de grover y ejecuto en una maquina cuantica"
        )
        self.assertTrue(parameters["use_real_device"])
        self.assertEqual(parameters["backend_name"], "")
        self.assertEqual(parameters["job_tags"], ["quantum-lab", "grover-search"])

    def test_execution_without_backend_defaults_to_real_hardware(self):
        parameters = _execution_parameters("Execute this Grover circuit")
        self.assertTrue(parameters["use_real_device"])

    def test_explicit_spanish_simulation_uses_local_simulator(self):
        parameters = _execution_parameters("Ejecuta Grover en el simulador local")
        self.assertFalse(parameters["use_real_device"])

    def test_negated_simulator_request_uses_real_hardware(self):
        parameters = _execution_parameters("Run Grover without a simulator")
        self.assertTrue(parameters["use_real_device"])

    def test_qaoa_maxcut_job_tag(self):
        parameters = _execution_parameters("Execute this optimized QAOA Max-Cut circuit")
        self.assertEqual(parameters["job_tags"], ["quantum-lab", "qaoa-maxcut"])


class LocalSimulationTests(unittest.IsolatedAsyncioTestCase):
    async def test_results_and_tags(self):
        output = await IBMQuantumTool().run(
            {
                "qasm_code": BELL_QASM,
                "backend_name": "simulator",
                "shots": 128,
                "job_tags": ["quantum-lab", "bell-state"],
            }
        )
        response = output.get_text_content()
        self.assertIn("local_statevector_simulator", response)
        self.assertIn("Local simulation completed", response)
        self.assertIn("`quantum-lab`, `bell-state`", response)


if __name__ == "__main__":
    unittest.main()
