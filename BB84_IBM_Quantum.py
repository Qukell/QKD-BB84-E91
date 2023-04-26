# BB84 online Simulation
# Importieren der benötigten Bibliotheken:
from qiskit import *
import numpy as np

# Benutzer-Token für die Nutzung der IBM Quantum Quantencomputer einfügen:
IBMQ.save_account(
    "INSERT_IBM_QUANTUM_TOKEN_HERE",
    overwrite=True)
provider = IBMQ.load_account()

# Verfügbares IBM Quantum System auswählen: https://quantum-computing.ibm.com/services/resources
backend = provider.get_backend("ibmq_qasm_simulator")

# Vorbereiten der zufälligen Bits und Basen von Alice:
num_qubits = 20  # Anzahl der initialen Qubits
alice_bits = np.random.randint(2, size=num_qubits)
alice_bases = np.random.randint(2, size=num_qubits)

# Vorbereiten der zufälligen Basen von Bob:
bob_bases = np.random.randint(2, size=num_qubits)

# Alice präperiert Qubits |0> oder |1> mit Not-Gate.
# Das Senden in der 45°-Achse wird mit dem Hadamard-Gate realisiert:
def send_qubits(alice_bits, alice_bases):
    qr = QuantumRegister(num_qubits, name="q")
    cr = ClassicalRegister(num_qubits, name="c")
    qc = QuantumCircuit(qr, cr)

    for i in range(num_qubits):
        if alice_bits[i] == 1:
            qc.x(i)
        if alice_bases[i] == 1:
            qc.h(i)
    qc.barrier()  # Visuelle Barriere im Plot für Alice
    return qc

# Bob misst in 90°-Achse (+) oder mit dem Hadamard-Gate in 45°-Achse (x):
def measure_qubits(qc, bob_bases):
    for i in range(num_qubits):
        if bob_bases[i] == 1:
            qc.h(i)

    qc.barrier()  # Visuelle Barriere im Plot für Bob

    for i in range(num_qubits):
        qc.measure(i, i)
    return qc

# Die Quantenschaltung mit Alice Qubits erstellen und so das Senden von Alice simulieren:
alice_qc = send_qubits(alice_bits, alice_bases)

# Die Quantenschaltung von ALice um das Messen von Bob erweitern:
measured_qc = measure_qubits(alice_qc, bob_bases)

# Simulieren der Quantenschaltung auf dem IBM Quantum: https://quantum-computing.ibm.com/jobs
simulator = backend
t_qc = transpile(measured_qc, simulator)
result = simulator.run(t_qc, shots=1).result()

# Extrahieren der Messung in Little Endian
little_endian_results = [int(bit) for bit in list(result.get_counts().keys())[0]]

# Invertieren der Bit-Reihenfolge
bob_results = little_endian_results[::-1]

# Basenvergleich zwischen Bob und Alice um gemeinsamen Schlüssel zu generieren:
shared_key = []
for i in range(num_qubits):
    if alice_bases[i] == bob_bases[i]:
        shared_key.append(bob_results[i])

# Ausgabe der Bits, Basen und des geheimen Schlüssels:
print("Alice Bits:")
print(alice_bits)
print("Alice Basen:")
print(alice_bases)
print("Bobs Basen:")
print(bob_bases)
print("Schlüssel:")
print('[{}]'.format(' '.join(str(element) for element in shared_key)))

# Plotten des gesamten Quantengitters in einem Jupyter Notebook:
# display(measured_qc.draw(output='mpl'))

# Plotten des gesamten Quantengitters in einer IDE:
import matplotlib.pyplot as plt
measured_qc.draw(output='mpl')
plt.show()