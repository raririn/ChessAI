from MoveTree import *
from random import choice as randChoice
from param import *
from utils import *
from operator import attrgetter
from operator import methodcaller

class AI:
    def __init__(self, board, side, depth):
        self.board = board
        # Depth is not used unless we run a minimax/negamax. But
        # still we keep the parameter here in the basic AI.
        self.depth = depth
        self.side = side
        #if self.side != self.board.turn:
        #    raise ValueError('Not correct side assigned to agent.')
    
    def getLegalMoves(self):
        return list(self.board.legal_moves)
    
    def generateMove(self):
        ''' Pick the first move. '''
        legalMoves = self.getLegalMoves()
        if len(legalMoves) == 1:
            return legalMoves
        else:
            return legalMoves[0]

class randomAgent(AI):
    def generateMove(self):
        legalMoves = self.getLegalMoves()
        if len(legalMoves) == 1:
            return legalMoves
        else:
            return randChoice(legalMoves)

class greedyAgent(AI):
    def generateMoveTree(self):
        moveTree = []
        legalMoves = self.getLegalMoves()
        for move in legalMoves:
            moveTree.append(MoveNode(move, [], move))
        for node in moveTree:
            self.board.push(node.move)
            self.getPoint(node)
            self.board.pop()
        return moveTree

    def getPoint(self, node):
        node.pointAdvantage = evaluateBoard(self.board, self.side)
    
    def generateMove(self):
        moveTree = self.generateMoveTree()
        bestNode = max(moveTree, key = lambda x: x.pointAdvantage)
        return bestNode.move


class minimaxAgent(AI):
    def generateMoveTree(self):
        moveTree = []
        for move in self.getLegalMoves():
            moveTree.append(MoveNode(move, [], move))
        for node in moveTree:
            self.board.push(node)
            self.populateNodeChildren(node)
            self.board.pop()
    
    def populateNodeChildren(self, node):
        node.pointAdvantage = evaluateBoard(self.board, self.side)
        node.depth = node.getDepth()
        if node.depth == self.maxDepth:
            return
        legalMoves = self.getLegalMoves()
        if not legalMoves:
            if self.board.is_checkmate():
                # set checkmate variable?
                return
            elif self.board.is_stalemate():
                node.pointAdvantage = 0
                # set stalemate variable?
                return
        for move in legalMoves:
            node.children.append(MoveNode(move, [], node))
            self.board.push(move)
            self.populateNodeChildren(node)
            self.board.pop()
        
