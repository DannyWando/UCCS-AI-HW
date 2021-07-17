# Daniel Wandeler
# HW3 Character Recognition with Artificial Neural Networks
# April 25, 2021

import random
import math

def accuracy(predicted, actual):
    numCorrect = 0
    length = len(actual)
    for i in range(length):
        if predicted[i] == actual[i]:
            numCorrect += 1

    #Return correct as a percentage
    return numCorrect / float(length) * 100.0


def initNetwork(numInputs, numHidden, numOutputs):
    # Couldn't figure out how to properly initialize the whole network properly
    # Assisted by neural net tutorial from (Brownlee 2016) that was cited in report
    neuralNet = list()
    hiddenLayer = [{'weights': [random.random() for i in range(numInputs+1)]} for j in range(numHidden)]
    neuralNet.append(hiddenLayer)
    outputLayer = [{'weights': [random.random() for i in range(numHidden+1)]} for j in range(numOutputs)]
    neuralNet.append(outputLayer)
    return neuralNet


# Calculates neuron activation for an input
def neuronActivation(weights, inputs):
    # Assuming the bias is the last entry in the weights list
    # Bias
    activation = weights[-1]
    # Calculated as weighted sum of the inputs + bias
    for i in range(len(weights)-1):
        activation += weights[i] * inputs[i]

    return activation


# Transfer neuron activation using sigmoid function
def neuronTransfer(activation):
    return 1.0 / (1.0 + math.exp(-activation))


def forwardPropogate(network, row):
    inputs = row
    for layer in network:
        newInputs = []
        for neuron in layer:
            activation = neuronActivation(neuron['weights'], inputs)
            neuron['output'] = neuronTransfer(activation)
            newInputs.append(neuron['output'])

        inputs = newInputs

    return inputs


def transferDeriv(output):
    return output * (1.0 - output)


# Backpropogates error and stores it in the neurons
# Has no return value, just updates error going backwards through the network
def backpropagateError(network, expected):
    numLayers = len(network)
    for i in reversed(range(numLayers)):
        workingLayer = network[i]
        errors = list()
        if i != numLayers-1:
            for j in range(len(workingLayer)):
                error = 0.0
                for neuron in network[i+1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(workingLayer)):
                neuron = workingLayer[j]
                errors.append(expected[j] - neuron['output'])

        for j in range(len(workingLayer)):
            neuron = workingLayer[j]
            neuron['delta'] = errors[j] * transferDeriv(neuron['output'])


def updateWeights(network, dataRow, learning):
    for i in range(len(network)):
        # Inputs is everything in the new data row except the bias
        inputs = dataRow
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i-1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += learning * neuron['delta'] * inputs[j]
            neuron['weights'][-1] += learning * neuron['delta']


def train(network, trainingSet, learning, numEpoch, numOutputs, answers):
    for epoch in range(numEpoch):
        summedError = 0
        counter = 0
        for row in trainingSet:
            outputs = forwardPropogate(network, row)
            expected = [0,0,0,0,0,0,0]
            expected[answers[counter]] = 1

            # Sum squared error
            summedError += sum([((expected[i] - outputs[i])**2) for i in range(numOutputs)])
            backpropagateError(network, expected)
            updateWeights(network, row, learning)
            counter += 1
        print('Epoch=%d, LearningRate=%.3f, Error=%.3f' % (epoch, learning, summedError))


def predict(network, dataRow):
    outputs = forwardPropogate(network, dataRow)
    #print(outputs)
    # Returns the output index of its prediction, aka which class it belongs to
    return outputs.index(max(outputs))


def backpropagation(training, test, learningRate, numEpoch, numHidden, expectedAnswers):
    numInputs = len(training[0])
    numOutputs = 7
    neuralnetwork = initNetwork(numInputs, numHidden, numOutputs)
    train(neuralnetwork, training, learningRate, numEpoch, numOutputs, expectedAnswers)
    predictions = list()
    for row in test:
        prediction = predict(neuralnetwork, row)
        predictions.append(prediction)

    return predictions


def parseDataset(filename):
    dataset = []
    data = list()
    temp = list()
    temp2 = [0 for i in range(7)]
    myFile = open(filename, 'r')
    inputLines = myFile.read().split('\n')
    for i in range(len(inputLines)):
        temp = [char for char in inputLines[i]]
        for j in range(len(temp)):
            if temp[j] == "#":
                temp2[j] = 1
            else:
                temp2[j] = 0

        data.extend(temp2)
        if ((i+1) % 9 == 0):
            dataset.append(data)
            data = list()

    myFile.close()
    return dataset


# Main
trainingSet = 'D:\AIhw3\HW3_Training.txt'
testingSet = 'D:\AIhw3\HW3_Testing.txt'
parsedTrain = parseDataset(trainingSet)
parsedTest = parseDataset(testingSet)
#print(parsedTest)

#0A, 1B, 2C, 3D, 4E, 5J, 6K
expectedTrainingClasses = [0,1,2,3,4,5,6,0,1,2,3,4,5,6,0,1,2,3,4,5,6]
expectedTestingClasses = [0,1,2,3,4,5,6,0,1,2,3,4,5,6,0,1,2,3,4,5,6]
learningRate = 0.25
epochs = 5000
hiddenLayerNodes = 10
inputNodes = len(parsedTrain[0])
outputNodes = 7

newNetPredict = backpropagation(parsedTrain, parsedTest, learningRate, epochs, hiddenLayerNodes, expectedTestingClasses)

for i in range(len(newNetPredict)):
    print('Expected=%d, Got=%d' % (expectedTestingClasses[i], newNetPredict[i]))
print("\n Test Set Accuracy: %.3f" % accuracy(newNetPredict, expectedTestingClasses))
