# Daniel Wandeler
# This function is the particle swarm optimization algorithm to be used in CS4820 HW2.


import random
import nQueens


# Particle class to hold variables per instance
class Particle:
    def __init__(self, initialX):
        self.position = []
        self.velocity = []
        self.error = 100
        self.bestPos = []
        self.bestErr = 100

        for i in range(0, dimensions):
            self.velocity.append(random.randint(-3, 3))
            self.position.append(int(initialX[i]))


    # Updates the velocity based on cognitive and social constants
    def updateVelocity(self, gBestPos):
        inertia = 0.7288994
        cog = 0.5
        soc = 1

        for i in range(0, dimensions):
            temp1 = random.random()
            temp2 = random.random()
            Cvelocity = cog * temp1 * (self.bestPos[i] - self.position[i])
            Svelocity = soc * temp2 * (gBestPos[i] - self.position[i])
            self.velocity[i] = inertia * self.velocity[i] + Cvelocity + Svelocity


    # Updates the position of the particle by adding it to its velocity
    # Keeps the position within the bounds of the problem
    def updatePosition(self, bounds):
        for i in range(0, dimensions):
            self.position[i] = int(self.position[i] + self.velocity[i])

            if self.position[i] > bounds[i][1]:
                self.position[i] = int(bounds[i][1])

            if self.position[i] < bounds[i][0]:
                self.position[i] = int(bounds[i][0])


    # Passes the particle to the fitness checker to be given a score
    def evaluate(self, fitnessFunc):
        self.error = fitnessFunc(self.position)
        if self.error < self.bestErr:
            self.bestPos = self.position
            self.bestErr = self.error


class PSO:
    def __init__(self, fitnessFunc, start, bounds, numParticles, maxIteration):
        # Initialize the variables before computation
        global dimensions
        dimensions = len(start)
        gBestError = 100
        gBestPos = [0,0,0,0,0,0,0,0]

        # Create the swarm
        swarm = []
        for i in range(0, numParticles):
            swarm.append(Particle(start))

        # Check each swarm members' fitness
        count = 0
        while count < maxIteration and gBestError != 0:
            for i in range(0, numParticles):
                swarm[i].evaluate(fitnessFunc)

                # Sets new best particle
                if swarm[i].error < gBestError:
                    nQueens.copyState(gBestPos, swarm[i].position)
                    gBestError = swarm[i].error

            # Updates velocities and positions based on best scoring particle in the iteration
            for i in range(0, numParticles):
                swarm[i].updateVelocity(gBestPos)
                swarm[i].updatePosition(bounds)

            count = count + 1


        print("Final best state:", gBestPos, "Fitness:", gBestError)
        nQueens.printBoardFromState(dimensions, gBestPos)
        print("Total iterations:", count)