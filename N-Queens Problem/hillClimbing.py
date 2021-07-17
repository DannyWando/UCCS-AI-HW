# This function is the hill climbing algorithm to be used in CS4820 HW2.
#
# Assisted via tutorials from Geeks4Geeks and lecture slides

import nQueens
import random

# Returns the state of the best move from currentState
# Best move is least collisions of queens
def getNeighbor(currentState):
    # Initialize variables before computation
    neighborBoard = nQueens.makeBoard(currentState)
    optimalState = [2,2,2,2,2,2,2,2]
    size = len(currentState)

    # Optimal state starts as the current state
    optimalState = nQueens.copyState(optimalState, currentState)

    objective = nQueens.checkSolution(optimalState)

    neighborState = [0,0,0,0,0,0,0,0]
    neighborState = nQueens.copyState(neighborState, optimalState)

    # Iterate through all possible neighbors of the board
    for i in range(size):
        for j in range(size):
            # Skip state if this condition is false
            if (j != currentState[i]):
                # Checks each possible move from the current state
                neighborState[i] = j
                neighborBoard[i][neighborState[i]] = 1
                neighborBoard[i][currentState[i]] = 0

                tempScore = nQueens.checkSolution(neighborState)

                if (tempScore < objective):
                    # Better score means making a new optimal state
                    objective = tempScore
                    optimalState = nQueens.copyState(optimalState, neighborState)

                # Reset the board to before adjustments
                neighborBoard[i][neighborState[i]] = 0
                neighborState[i] = currentState[i]
                neighborBoard[i][currentState[i]] = 1

    return optimalState


# Hill Climbing state space search algo
def hillClimbing(currState):
    # Initialize variables before computation
    stateChecks = 0
    neighborState = [0, 0, 0, 0, 0, 0, 0, 0]
    neighborState = nQueens.copyState(neighborState, currState)

    while True:
        currState = nQueens.copyState(currState, neighborState)

        # Optimal state returned from getNeighbor
        opState = getNeighbor(neighborState)
        stateChecks = stateChecks + 1
        neighborState = nQueens.copyState(neighborState, opState)

        # If there does not exist a better scoring neighbor
        # Return current state since it's the current optimal state
        if (nQueens.compareStates(currState, opState)):
            print("No better states found...")
            print("Final state: ", opState)
            nQueens.printBoardFromState(len(opState), opState)
            print("Final fitness: ", nQueens.checkSolution(opState))
            print("Total states checked: ", stateChecks)
            break

        # If there exists a new neighbor with the same score, but not better
        # Jump to a random state to avoid local optimum
        elif (nQueens.checkSolution(currState) == nQueens.checkSolution(neighborState)):
            print("Jumped to random state...")
            neighborState[random.randint(0,7)] = random.randint(0,7)
            continue

        print('Jumped to new neighbor...')

