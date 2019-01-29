from qiskit import IBMQ
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, BasicAer

import sys
import os

import random
import numpy as np

import logging
import logging.handlers

import matplotlib as mpl
import matplotlib.pyplot as plt

#### Set up logger
logger = logging.getLogger(__name__)
formatter = logging.Formatter('[%(levelname)s] %(name)s - %(message)s')
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(formatter)
log_level = logging.DEBUG
logger.addHandler(log_handler)
logger.setLevel(log_level)


def get_catlapse(input_vector, ibm=False):
	"""
	Input: 14 length binary string (which cats chosen)
	Output: 14 length binary string (which cats dies or lives)
	"""
	result = {}
	if ibm:
		IBMQ.enable_account('1d4d99cccb3d406da3580c6dfe20a681169b7d76f14fa11bbc34868c3f6b3988a911bd6bab95e012d2c829901a894b45b2d47432431a252cb5d6f3a84d700245')
		backend = IBMQ.get_backend('ibmq_16_melbourne')
		logger.info(backend.status())
		logger.info(backend.name())
	else:
		# Use Aer's qasm_simulator
		backend = BasicAer.get_backend('qasm_simulator')
		logger.info(backend.status())
	for x in range(len(input_vector)):
		if input_vector[x] == "1":
			# Create a Quantum Register with 3 qubits.
			q = QuantumRegister(3, 'q')

			# Create a Quantum Circuit acting on the q register
			circ = QuantumCircuit(q)

			# Create the GHZ state...

			# Add a H gate on qubit 0, putting this qubit in superposition.
			circ.h(q[0])
			# Add a CX (CNOT) gate on control qubit 0 and target qubit 1, putting
			# the qubits in a Bell state.
			circ.cx(q[0], q[1])
			# Add a CX (CNOT) gate on control qubit 0 and target qubit 2, putting
			# the qubits in a GHZ state.
			circ.cx(q[0], q[2])


			# Create a Classical Register with 3 bits.
			c = ClassicalRegister(3, 'c')
			# Create a Quantum Circuit
			meas = QuantumCircuit(q, c)
			meas.barrier(q)
			# map the quantum measurement to the classical bits
			meas.measure(q,c)

			# The Qiskit circuit object supports composition using
			# the addition operator.
			circuits = []
			qc = circ+meas
			print(qc.draw())

			# Execute the circuit on the qasm simulator.
			job = execute(qc, backend, shots=1)
			logger.info(job.status())

			# Grab the results from the job.
			job_result = job.result()

			if "000" in job_result.get_counts():
				result[x] = "Alive"
			else:
				result[x] = "Dead"

	return result


def randomize_pairs_ibmq():
    pairs = []
    for i in range(1,7):
        index1 = i
        flip = random.sample([0,1], 1)
        if flip[0] and (not(pairs) or i not in pairs[-1]):
            pairs.append((index1, i+1))
    return pairs


def get_entangle_results(n, pairs):
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)
    qp = QuantumCircuit(qr,cr)

    qp.rx( np.pi/2,qr[0])
    qp.cx(qr[0],qr[1])

    qp.measure(qr,cr)

    qr = QuantumRegister(n)
    cr = ClassicalRegister(n)
    qp = QuantumCircuit(qr,cr)

    for pair in pairs:
        qp.ry((1+2*random.random())*np.pi/4,qr[pair[0]]) # angle generated randonly between pi/4 and 3pi/4
        qp.cx(qr[pair[0]],qr[pair[1]])

    qp.measure(qr,cr)

    print(qp.draw())
    qp.draw(output='latex_source', filename="entanglement.tex")
    os.system("pdflatex entanglement.tex")

    backend=BasicAer.get_backend('qasm_simulator')
    job = execute(qp,backend)
    results = job.result().get_counts()
    return results


def calculate_probs(n, raw_stats):
    """
    Given a counts dictionary as the input `raw_stats`,
    a dictionary of probabilities is returned.
    The keys for these are either integers (referring to qubits) or
    strings (referring to links of neighbouring qubits). For the qubit entries,
    the corresponding value is the probability that the qubit is in state `1`.
    For the pair entries, the values are the probabilities that the two qubits
    disagree (so either the outcome `01` or `10`.
    """
    Z = 0
    for string in raw_stats:
        Z += raw_stats[string]
    stats = {}
    for string in raw_stats:
        stats[string] = raw_stats[string]/Z


    probs = {}
    adja = []
    for i in range(0,n):
        adja += [[0] * n]
    for n in range(0,n):
        probs[n] = 0

    for string in stats:
        for n in range(n):
            if string[n]=='1':
                probs[n] += stats[string]
        for i in range(0,n):
            for j in range(0,n):
                if string[i] != string[j]:
                    adja[i][j] += 1

    return probs, np.matrix(adja)


def find_pairs(results):
    thepairs = []
    for i in range(0,len(res)-1):
        for j in range(i+1,len(res)):
            if abs(res[i] - res[j]) < 10 ** (-5):
                thepairs += [(i,j)]
    return thepairs


def get_catangle(n):
    pairs = randomize_pairs_ibmq()
    results = get_entangle_results(n, pairs)
    res, adja = calculate_probs(n, results)
    return res, adja
