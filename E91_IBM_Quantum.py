# E91 online Simulation
# Importieren der benötigten Bibliotheken:
from qiskit import *
import numpy as np

# Benutzer-Token für die Nutzung der IBM Quantum Quantencomputer einfügen:
IBMQ.save_account(
    "INSERT_IBM_QUANTUM_TOKEN_HERE",
    overwrite=True)
provider = IBMQ.load_account()

# Verfügbares IBM Quantum System auswählen: https://quantum-computing.ibm.com/services/resources
backend = provider.get_backend("ibmq_lima")

# Vorbereiten der zufälligen Basen von Alice und Bob:
num_qubits = 20  # Anzahl der initialen Qubits
alice_bases = np.random.randint(1, 4, size=num_qubits)
bob_bases = np.random.randint(1, 4, size=num_qubits)

# Definition der Funktionen für Alice und Bobs Messbasen
def apply_bases(qc, alice_base, bob_base):
# Alice Basen a1, a2 und a3. Für a3 muss keine Quantenoperation durchgeführt werden.
    if alice_base == 1:
        qc.h(0)
    elif alice_base == 2:
        qc.s(0)
        qc.h(0)
        qc.t(0)
        qc.h(0)
# Bobs Basen b1, b2, b3. Für b2 muss keine Quantenoperation durchgeführt werden
    if bob_base == 1:
        qc.s(1)
        qc.h(1)
        qc.t(1)
        qc.h(1)
    elif bob_base == 3:
        qc.s(1)
        qc.h(1)
        qc.tdg(1)
        qc.h(1)

# Verschränkte Quantenschaltung
def entangled_circuit():
    qc = QuantumCircuit(2, 2)
    qc.x(0)
    qc.x(1)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()
    return qc

# Erstellen der Quantenschaltkreise der Messung von Alice und Bob
circuits = [entangled_circuit() for _ in range(num_qubits)]

for i in range(num_qubits):
    apply_bases(circuits[i], alice_bases[i], bob_bases[i])
    circuits[i].measure([0, 1], [0, 1])
    circuits[i].barrier()

# Simulation der gesamten Quantenschaltung:
simulator = backend
results = [simulator.run(transpile(circ, simulator), shots=1).result() for circ in circuits]

# Extrahieren der Messung
little_endian_results = [list(result.get_counts().keys())[0] for result in results]

# little_endian_results2 = [list(result.get_counts().keys())[1] for result in results]

# Invertieren der Bit-Reihenfolge
measured_results = [result[::-1] for result in little_endian_results]

# measured_results2 = [result[::-1] for result in little_endian_results]

# Generieren des Schlüssels:
alice_key = []
for i in range(num_qubits):
    if (alice_bases[i] == 3 and bob_bases[i] == 2) or (alice_bases[i] == 2 and bob_bases[i] == 1):
        alice_key.append(measured_results[i][0])

# Generieren des Schlüssels2:
bob_key = []
for i in range(num_qubits):
    if (alice_bases[i] == 3 and bob_bases[i] == 2) or (alice_bases[i] == 2 and bob_bases[i] == 1):
        bob_key.append(measured_results[i][1])

# Ausgabe der Basen und des geheimen Schlüssels:
print("Alice Basen:")
print(alice_bases)
print("Bobs Basen:")
print(bob_bases)
print("Alice Schlüssel:")
print('[{}]'.format(' '.join(str(element) for element in alice_key)))
print("Bobs Schlüssel:")
print('[{}]'.format(' '.join(str(element) for element in bob_key)))

# Gesamte Quantenschaltung aus allen verschränkten Schaltungen, Alice Schaltungen und Bobs Schaltungen erstellen
combined_circuit = QuantumCircuit(2, 2)

for circuit in circuits:
    combined_circuit = combined_circuit.compose(circuit)

# Gesamte kombinierte Quantenschaltung in IDE visualisieren
import matplotlib.pyplot as plt
combined_circuit.draw('mpl')
plt.show()

# Gesamte kombinierte Quantenschaltung in Jupyter Notebook visualisieren
# display(combined_circuit.draw('mpl'))

# Verschränlte Schaltung visualisieren:
entanglet_qc = QuantumCircuit(2)
entanglet_qc.x(0)
entanglet_qc.x(1)
entanglet_qc.h(0)
entanglet_qc.cx(0, 1)
entanglet_qc.draw('mpl')
plt.show()

# Alice mögliche Messungen visualisieren:
alice_qc = QuantumCircuit(3)
alice_qc.h(0)
alice_qc.s(1)
alice_qc.h(1)
alice_qc.t(1)
alice_qc.h(1)
alice_qc.measure_all()
alice_qc.draw('mpl')
plt.show()

# Bob mögliche Messungen visualisieren:
bob_qc = QuantumCircuit(3)
bob_qc.s(0)
bob_qc.h(0)
bob_qc.t(0)
bob_qc.h(0)
bob_qc.s(2)
bob_qc.h(2)
bob_qc.tdg(2)
bob_qc.h(2)
bob_qc.measure_all()
bob_qc.draw('mpl')
plt.show()
