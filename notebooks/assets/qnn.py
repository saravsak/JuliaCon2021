# Import Braket libraries
from braket.circuits import Circuit
from braket.aws import AwsDevice

# A function that converts a bit string bitStr into a quantum circuit
def bit_string_to_circuit(bitStr):  
    circuit = Circuit()
    for ind in range(len(bitStr)):
        if bitStr[ind]=='1':
            circuit.x(ind)
            
    return circuit
    
# provide a feature string to test the function above
feature = '11010'

# print quantum circuit that prepares corresponding quantum state 
print(bit_string_to_circuit(feature))

# import standard numpy libraries and optimizers
import numpy as np
from scipy.optimize import minimize

# Braket imports
from braket.circuits import Circuit, Gate, Instruction, circuit, Observable
from braket.aws import AwsDevice, AwsQuantumTask
from braket.devices import LocalSimulator

# set Braket backend to local simulator (can be changed to other backends)
device = LocalSimulator()

# Quantum Neural Net from the QNN figure implemented in Braket
# Inputs: bitStr - data bit string (e.g. '01010101')
#         pars - array of parameters theta (see the QNN figure for more details)

def QNN(bitStr,pars):
    ## size of the quantum neural net circuit
    nQbts = len(bitStr) + 1 # extra qubit is allocated for the label

    ## initialize the circuit
    qnn = Circuit()

    ## add single-qubit X rotation to the label qubit,
    ## initialize the input state to the one specified by bitStr
    ## add single-qubit Y rotations to data qubits,
    ## add XX gate between qubit i and the label qubit,
    qnn.rx(nQbts-1, pars[0])
    for ind in range(nQbts-1):
        angles = pars[2*ind + 1:2*ind+1+2]
        if bitStr[ind] == '1': # by default Braket sets input states to '0',
                               # qnn.x(ind) flips qubit number ind to state |1\
            qnn.x(ind)
        qnn.ry(ind, angles[0]).xx(ind, nQbts-1, angles[1])

    ## add Z observable to the label qubit
    observZ = Observable.Z()
    qnn.expectation(observZ, target=[nQbts-1])

    return qnn

## Function that computes the label of a given feature bit sting bitStr

def parity(bitStr):
    return bitStr.count('1') % 2

## Log loss function L(theta,phi) for a given training set trainSet
## inputs: trainSet - array of feature bit strings e.g. ['0101','1110','0000']
##         pars - quantum neural net parameters theta (See the QNN figure)
##         device -  Braket backend that will compute the log loss
def loss(trainSet, pars, device):
    loss = 0.0
    for ind in range(np.size(trainSet)):
        ## run QNN on Braket device
        task = device.run(QNN(trainSet[ind], pars), shots=0)
        ## retrieve the run results <Z>
        result = task.result()

        if parity(trainSet[ind])==0:
            loss += -np.log2(1.0-0.5*(1.0-result.values[0]))
        else:
            loss += -np.log2(0.5*(1.0-result.values[0]))
    print ("Current value of the loss function: ", loss)
    return loss

nBits = 10 # number of bits per data string

## Please explore other training sets
trainSet = ['1101011010',
            '1000110011',
            '0101001001',
            '0010000110',
            '0101111010',
            '0000100010',
            '1001010000',
            '1100110001',
            '1000010001',
            '0000111101',
            '0000000001']

## Initial assignment of QNN parameters theta and phi (random angles in [-pi,pi])
pars0 = 2 * np.pi * np.random.rand(2*nBits+1) - np.pi

## Run minimization
res = minimize(lambda pars: loss(trainSet, pars, device), pars0, method='BFGS', options={'disp':True})

## Print the predicted label values for all N-bit data points using the optimal QNN parameters res.x
#for ind in range(2**nBits):
#    data = format(ind, '0'+str(nBits)+'b')
#    task = device.run(QNN(data, res.x), shots=100)
#    result = task.result()
#    if (data in trainSet):
#        inSet = 'in the training set'
#    else:
#        inSet = 'NOT in the training set'
#    print('Feature:', data, '| QNN predicted parity: ', 0.5*(1-result.values[0]), ' | ', inSet)
#    print('---------------------------------------------------')
