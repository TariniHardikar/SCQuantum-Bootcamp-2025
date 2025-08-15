#!/usr/bin/env python3
"""
Script to submit a 3-qubit entangled circuit to IonQ Aria QPU via qBraid
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

def submit_to_aria():
    """Submit the circuit to IonQ Aria QPU"""
    try:
        # Create the circuit
        circuit = create_3qubit_entangled_circuit()
        print("Created 3-qubit GHZ entangled circuit:")
        print(circuit)
        
        # Get IonQ Aria device (try both Aria-1 and Aria-2)
        try:
            device = qbraid.get_device("ionq_aria_1")
            device_name = "IonQ Aria-1"
        except:
            device = qbraid.get_device("ionq_aria_2")
            device_name = "IonQ Aria-2"
            
        print(f"\nDevice: {device_name}")
        print(f"Device status: {device.status()}")
        
        # Submit job with 2500 shots (minimum for error mitigation)
        shots = 2500
        job = device.run(circuit, shots=shots)
        print(f"\nJob submitted to {device_name} with {shots} shots")
        print(f"Job ID: {job.id}")
        print("Note: Using 2500 shots (minimum for error mitigation on Aria)")
        
        # Wait for completion and get results
        print("Waiting for job completion...")
        result = job.result()
        
        print(f"\nJob Status: {job.status()}")
        print("Results:")
        print(f"Counts: {result.measurement_counts()}")
        
        # Calculate cost
        cost_credits = 3 * shots + 30  # 3 credits per shot + 30 per task
        print(f"\nEstimated cost: {cost_credits} credits")
        
        return result
        
    except Exception as e:
        print(f"Error submitting to IonQ Aria: {e}")
        return None

def submit_to_aria_basic():
    """Submit the circuit to IonQ Aria QPU with basic shots (no error mitigation)"""
    try:
        # Create the circuit
        circuit = create_3qubit_entangled_circuit()
        print("Created 3-qubit GHZ entangled circuit:")
        print(circuit)
        
        # Get IonQ Aria device
        try:
            device = qbraid.get_device("ionq_aria_1")
            device_name = "IonQ Aria-1"
        except:
            device = qbraid.get_device("ionq_aria_2")
            device_name = "IonQ Aria-2"
            
        print(f"\nDevice: {device_name}")
        print(f"Device status: {device.status()}")
        
        # Submit job with 1000 shots (basic run without error mitigation)
        shots = 1000
        job = device.run(circuit, shots=shots)
        print(f"\nJob submitted to {device_name} with {shots} shots")
        print(f"Job ID: {job.id}")
        print("Note: Basic run without error mitigation")
        
        # Wait for completion and get results
        print("Waiting for job completion...")
        result = job.result()
        
        print(f"\nJob Status: {job.status()}")
        print("Results:")
        print(f"Counts: {result.measurement_counts()}")
        
        # Calculate cost
        cost_credits = 3 * shots + 30  # 3 credits per shot + 30 per task
        print(f"\nEstimated cost: {cost_credits} credits")
        
        return result
        
    except Exception as e:
        print(f"Error submitting to IonQ Aria: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    print("=== Submitting 3-Qubit Entangled Circuit to IonQ Aria ===")
    
    # Check if user wants error mitigation or basic run
    if len(sys.argv) > 1 and sys.argv[1] == "--error-mitigation":
        print("Running with error mitigation (2500 shots minimum)")
        result = submit_to_aria()
    else:
        print("Running basic version (1000 shots)")
        print("Use --error-mitigation flag for error mitigation (2500 shots)")
        result = submit_to_aria_basic()
    
    if result:
        print("\n=== Job completed successfully! ===")
    else:
        print("\n=== Job failed ===")