import hillClimbing
import geneticAlgo
import particleSwarmOptimization
import random
import time

# i is the row index
# j is the column the queen is in that row

# Prints a board given a certain solution state
# 1s represent spaces with a Queen on it, 0s represent empty spaces
def printBoardFromState(size, state):
    for i in range(size):
        for j in range(size):
            if state[i] == j:
                print("1", end=" ")
            else:
                print("0", end=" ")
        print()


# Prints the board that is passed as a parameter
# 1s represent spaces with a Queen on it, 0s represent empty spaces
def printBoard(chessBoard):
    for i in range(len(chessBoard)):
        for j in range(len(chessBoard)):
            print(chessBoard[i][j], end=" ")
        print()


# Creates a 2D array to represent a board. All values set to 0
def emptyBoard(size):
    board = [[0 for i in range(size)] for j in range(size)]
    return board


# Returns a randomly generated solution state
def makeRandomState(size):
    solState = []
    for i in range(size):
        number = random.randint(0,size-1)
        solState.append(number)

    return solState


# Given a state, returns a corresponding 2D array board
def makeBoard(state):
    currentSize = len(state)
    newBoard = emptyBoard(currentSize)
    for i in range(currentSize):
        newBoard[i][state[i]] = 1

    return newBoard;


# Given a solution state, checks to see if it is accepted
# Always returns the number of collisions in the present state
def checkSolution(solution):
    attackingPairs = 0
    workingBoard = makeBoard(solution)
    n = len(solution)

    # Checking each row, only 1 queen per row in initialization
    for i in range(0,n):
        # Vertical check first, then diagonal check
        # No horizontal check since states can only have 1 queen per row initially

        # Check up in the column, row decreasing
        row = i-1
        column = solution[i]
        while (row >= 0 and workingBoard[row][column] != 1):
            row = row-1

        if (row >= 0 and workingBoard[row][column] == 1):
            attackingPairs = attackingPairs + 1

        # Check down in the column, row increasing
        row = i+1
        column = solution[i]
        while (row < n and workingBoard[row][column] != 1):
            row = row + 1

        if (row < n and workingBoard[row][column] == 1):
            attackingPairs = attackingPairs + 1


        # Check up left diag, row and column decreasing
        row = i-1
        column = solution[i]-1
        while (row >= 0 and column >= 0 and workingBoard[row][column] != 1):
            row = row-1
            column = column - 1

        if (row >= 0 and column >= 0 and workingBoard[row][column] == 1):
            attackingPairs = attackingPairs + 1


        # Check up right diag, row decreasing column increasing
        row = i-1
        column = solution[i] + 1
        while (row >= 0 and column < n and workingBoard[row][column] != 1):
            row = row - 1
            column = column + 1

        if (row >= 0 and column < n and workingBoard[row][column] == 1):
            attackingPairs = attackingPairs + 1


        # Check down right diag, row and column increasing
        row = i+1
        column = solution[i] + 1
        while (row < n and column < n and workingBoard[row][column] != 1):
            row = row + 1
            column = column + 1

        if (row < n and column < n and workingBoard[row][column] == 1):
            attackingPairs = attackingPairs + 1


        # Check down left diag, row increasing  column decreasing
        row = i+1
        column = solution[i] - 1
        while (row < n and column >= 0 and workingBoard[row][column] != 1):
            row = row + 1
            column = column - 1

        if (row < n and column >= 0 and workingBoard[row][column] == 1):
            attackingPairs = attackingPairs + 1

    return attackingPairs/2


def compareStates(state1, state2):
    for i in range(len(state1)):
        if (state1[i] != state2[i]):
            return False

    return True


# Makes state1 contents now have the contents of state2
# Returns new state1
def copyState(state1, state2):
    for i in range(len(state2)):
        state1[i] = state2[i]

    return state1


# Main driver code
def main():
    startTime = time.time()

    initial = makeRandomState(8)
    print("Starting state: ", initial)
    boundsPSO = [(0,7), (0,7), (0,7), (0,7), (0,7), (0,7), (0,7), (0,7)]

    #hillClimbing.hillClimbing(initial)
    #geneticAlgo.geneticAlgo()
    particleSwarmOptimization.PSO(checkSolution, initial, boundsPSO, numParticles=100, maxIteration=1000)

    print("Execution time: %s ms" % ((time.time()-startTime)*1000))
    return 0


if __name__ == '__main__':
    main()

'''
Recorded from tests in paper report since all starts were randomly initialized

Hill-Climbing Test Start States
7,5,5,6,3,6,3,4
1,6,2,0,1,0,7,4
5,7,3,6,3,4,5,1
7,7,0,6,0,6,4,7
6,1,6,4,5,5,6,2

GA Test Start States
3,0,4,5,1,5,2,5
7,4,1,7,5,0,7,6
2,2,0,2,5,6,5,0
1,5,7,5,2,5,7,7
2,2,3,5,2,4,4,7

PSO Test Start States
2,7,1,5,5,6,0,4
7,0,1,4,6,6,4,7
4,4,6,0,7,1,1,2
5,2,1,5,6,3,1,0
0,4,3,6,6,6,6,3
'''
