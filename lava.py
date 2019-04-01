
"""Solution Code for Upstart Puzzle: Fighting for Lava

Program Source Code written by Chris Achenbach

Original Problem and Article by Dennis Shasha

This program solves the Fighting For Lava Problem by creating a tree
to represent each move in the game. This tree loosely resembles a binary
heap in the way that nodes are appeneded.

The nodes of this game tree represent moves that a player
takes. Optimal moves do not depend on the player who takes them (as
far as I can tell).  As a result, moves are not tagged with a player
until after the game tree has been built.

Static Analysis of the game tree reveals more insights about the
nature of this game.

"""

class Node:
    def __init__(self, used, free):
        self.used = used
        self.free = free

        
def makeNode(L, x):
    if x>L:
        used = L
        free = 0
    else:
        used = x
        free = float(L - x) / 2
    return Node(used, free)


def currentParentNode(tree):
    currentIndex = len(tree) - 1
    parentIndex = currentIndex >> 1
    return tree[parentIndex]
    
        
def buildTree(L):    
    tree = []
    tree.append(makeNode(L, 1))
    n = currentParentNode(tree)
    x = 2
    while (n.free > 0):
        tree.append(makeNode(n.free, x))
        tree.append(makeNode(n.free, x + 1))
        n = currentParentNode(tree)
        x += 2
    return tree



# ====================================================================

# Handling Scores and extracting information from the game tree.  This
# part is static analysis. It can be done after the game tree has
# already been built.


def getScores(tree, nPlayers):
    scores = [0] * nPlayers
    for i, node in enumerate(tree):
        player = (i % nPlayers)
        points = node.used
        scores[player] += points
    return scores


def getWinners(scores):
    highest = 0
    winners = [None]
    for i, score in enumerate(scores):
        if score > highest:
            winners = [i]
            highest = score
        elif score == highest:
            winners.append(i)
    return winners


# ====================================================================

# The Experiment class is simply an organized way to run various
# experiments. The most common variables are the initial Length, L,
# and the number of players, nPlayers. Putting this into a class makes
# it easier to keep the data together and output it in different
# forms.


class Experiment:
    def __init__(self, L, nPlayers):
        self.L = L
        self.nPlayers = nPlayers
        self.tree = []
        self.scores = []
        self.winners = []

        
    def run(self):
        self.tree = buildTree(self.L)
        self.scores = getScores(self.tree, self.nPlayers)
        self.winners = getWinners(self.scores)

        
    def printSummary(self):
        print("L: {}, k: {} \tWins: {},\tScores: {}".format(
            self.L,
            self.nPlayers,
            self.winners,
            self.scores,
        ))
        
        

# ====================================================================

def main():
    for L in range(5, 102):
        for k in range(2, 70):
            exp = Experiment(L, k)
            exp.run()
            if exp.scores[-1] == 0:
                print("Maxed out on players.")
                break
            exp.printSummary()
            

if __name__ == "__main__":
    main()
