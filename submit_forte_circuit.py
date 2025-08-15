#!/usr/bin/env python3
"""
Script to submit a 3-qubit entangled circuit to IonQ Forte QPU via qBraid
Creates a GHZ (Greenberger-Horne-Zeilinger) state: |000⟩ + |111⟩
"""

import qbraid
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def create_3qubit_entangled_circuit():
    """Create a 3-qubit GHZ entangled state circuit"""
    # Create quantum and classical registers
    qreg = QuantumRegister(3, 'q')
    creg = ClassicalRegister(3, 'c')
    circuit = QuantumCircuit(qreg, creg)
    
    # Create GHZ state: |000⟩ + |111⟩
    circuit.h(qreg[0])      # Put first qubit in superposition
    circuit.cx(qreg[0], qreg[1])  # Entangle first and second qubits
    circuit.cx(qreg[1], qreg[2])  # Entangle second and third qubits
    
    # Measure all qubits
    circuit.measure(qreg, creg)
    
    return circuit

def submit_to_forte():
    """Submit the circuit to IonQ Forte QPU"""
    try:
        # Create the circuit
        circuit = create_3qubit_entangled_circuit()
        print("Created 3-qubit GHZ entangled circuit:")
        print(circuit)
        
        # Get IonQ Forte device
        device = qbraid.get_device("ionq_forte")
        print(f"\nDevice: {device}")
        print(f"Device status: {device.status()}")
        
        # Submit job with 1000 shots
        shots = 1000
        job = device.run(circuit, shots=shots)
        print(f"\nJob submitted to IonQ Forte with {shots} shots")
        print(f"Job ID: {job.id}")
        
        # Wait for completion and get results
        print("Waiting for job completion...")
        result = job.result()
        
        print(f"\nJob Status: {job.status()}")
        print("Results:")
        print(f"Counts: {result.measurement_counts()}")
        
        # Calculate cost
        cost_credits = 8 * shots + 30  # 8 credits per shot + 30 per task
        print(f"\nEstimated cost: {cost_credits} credits")
        
        return result
        
    except Exception as e:
        print(f"Error submitting to IonQ Forte: {e}")
        return None

if __name__ == "__main__":
    print("=== Submitting 3-Qubit Entangled Circuit to IonQ Forte ===")
    result = submit_to_forte()
    
    if result:
        print("\n=== Job completed successfully! ===")
    else:
        print("\n=== Job failed ===")