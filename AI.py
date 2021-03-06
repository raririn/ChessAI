from MoveTree import *
from param import *
from utils import *

class AI:
    ''' Basic AI class. The default is a trival one, which always
        chooses the first move given in the legal move list.'''
    def __init__(self, board, side, depth):
        self.board = board
        # Depth is not used unless we run a minimax/negamax. But
        # still we keep the parameter here in the basic AI.
        self.depth = depth
        self.side = side
        if self.side != self.board.turn:
            raise ValueError('Not correct side assigned to agent.')
    
    def getLegalMoves(self):
        return list(self.board.legal_moves)
    
    def generateMove(self):
        ''' Pick the first move. Return None if there is no legal move.'''
        legalMoves = self.getLegalMoves()
        if legalMoves:
            return legalMoves[0]
        else:
            return None

class randomAgent(AI):
    ''' An agent that randomly pick a legal move.'''
    def generateMove(self):
        legalMoves = self.getLegalMoves()
        if legalMoves:
            return randChoice(legalMoves)
        else:
            return None

class greedyAgent(AI):
    ''' An agent that greedily choose the move with greatest score. 
        In other words, it's a search agent with depth = 1. '''
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
        def pickMax(moveTree):
            if not isinstance(moveTree, list):
                raise TypeError('Can only pick max from a moveTree.')
            maxNode = moveTree[0]
            for i in moveTree:
                if i > maxNode:
                    maxNode = i
                elif i == maxNode:
                    if rand() > 0.5:
                        maxNode = i
                else:
                    pass
            return maxNode

        moveTree = self.generateMoveTree()
        #bestNode = max(moveTree, key = lambda x: x.pointAdvantage)
        if moveTree:
            bestNode = pickMax(moveTree)
            return bestNode.move
        else:
            return None


class minimaxAgent(AI):
    ''' An agent searching in a minimax tree with given depth. '''
    def generateMoveTree(self):
        moveTree = []
        for move in self.getLegalMoves():
            moveTree.append(MoveNode(move, [], None))
        for node in moveTree:
            if not isinstance(node, MoveNode):
                raise TypeError('Bad argument given.')
            self.board.push(node.move)
            self.populateNodeChildren(node)
            self.board.pop()
        return moveTree

    def populateNodeChildren(self, node):
        if not isinstance(node, MoveNode):
            raise TypeError('Bad argument given.')
        #node.pointAdvantage = evaluateBoard(self.board, self.side)
        node.depth = node.getDepth()
        if node.depth == self.depth:
            node.pointAdvantage = evaluateBoard(self.board, self.side)
            return
        else:
            node.pointAdvantage = 0
        legalMoves = self.getLegalMoves()
        if not legalMoves:
            # No legal move means a terminal state is reached.
            # Therefore we stop searching, and return immediately.
            # Note that we handle terminal state HERE, so every node
            # without children is guaranteed to be in terminal state.
            if self.board.is_checkmate():
                # set checkmate variable?
                return
            elif self.board.is_stalemate():
                node.pointAdvantage = 0
                # set stalemate variable?
                return
            else:
                raise TypeError('Invalid board status.')
        for move in legalMoves:
            node.children.append(MoveNode(move, [], node))
            self.board.push(move)
            self.populateNodeChildren(node.children[-1])
            self.board.pop()

    def calculatePoint(self, node):
        def max_value(node):
            v = - float('inf')
            for i in node.children:
                v = max(v, i.pointAdvantage)
            return v
        def min_value(node):
            #print("min_value called on")
            #print(node)
            v = float('inf')
            for i in node.children:
                v = min(v, i.pointAdvantage)
            #    print(i.pointAdvantage)
            #return v
            #print(node)
            #print(min(node.children), min(node.children).pointAdvantage)
            #print("Finish a call")
            return min(node.children).pointAdvantage
        if node.children:
            # If the node has children, traverse the tree and run
            # minimax on all children.
            for child in node.children:
                child.pointAdvantage = self.calculatePoint(child)
            if node.children[0].depth % 2 == 1:
                # If the node's children has an odd depth, i.e.
                # the node has an even depth. Therefore it is 
                # a max state.
                return max_value(node)
            else:
                return min_value(node)
        else:
            # If the node has no child, return the node's utility.
            return node.pointAdvantage

    def getMove(self, moveTree):
        ''' Return all moves with highest point. '''
        bestNodes = []
        for node in moveTree:
            node.pointAdvantage = self.calculatePoint(node)
            if not bestNodes:
                bestNodes.append(node)
            elif node > bestNodes[0]:
                bestNodes = [node]
            elif node == bestNodes[0]:
                bestNodes.append(node)
        return [node.move for node in bestNodes]

    
    def generateMove(self):
        #print('generating,')
        moveTree = self.generateMoveTree()
        #print("moveTree")
        #for i in moveTree:
        #    print(i)
        bestMoves = self.getMove(moveTree)
        #print("bestMoves")
        #for i in bestMoves:
        #    print(i)
        if bestMoves:
            return randChoice(bestMoves)
        else:
            return None
        
class alphabetaAgent(minimaxAgent):
    ''' Minimax Agent with Alpha-beta prunning. Overrides 
        calculatePoint() method to implement prunning. '''

    def calculatePoint(self, node, alpha, beta):
        def max_value(node, alpha, beta):
            v = - float('inf')
            for i in node.children:
                v = max(v, i.pointAdvantage)
                if v >= beta:
                    return v, alpha, beta
                alpha = max(alpha, v)
            return v, alpha, beta
        def min_value(node, alpha, beta):
            v = float('inf')
            for i in node.children:
                v = min(v, i.pointAdvantage)
                if v <= alpha:
                    return v, alpha, beta
                beta = min(beta, v)
            return v, alpha, beta

        # Main body
        if node.children:
            # If the node has children, traverse the tree and run
            # minimax on all children.
            for child in node.children:
                child.pointAdvantage, alpha, beta = self.calculatePoint(child, alpha, beta)
            if node.children[0].depth % 2 == 1:
                # If the node's children has an odd depth, i.e.
                # the node has an even depth. Therefore it is 
                # a max state.
                v, alpha, beta = max_value(node, alpha, beta)
                return v, alpha, beta
            else:
                v, alpha, beta = min_value(node, alpha, beta)
                return v, alpha, beta
        else:
            # If the node has no child, return the node's utility.
            return node.pointAdvantage, alpha, beta

    def getMove(self, moveTree):
        ''' Return all moves with highest point. '''
        bestNodes = []
        for node in moveTree:
            alpha = - float('inf')
            beta = float('inf')
            node.pointAdvantage, alpha, beta = self.calculatePoint(node, alpha, beta)
            if not bestNodes:
                bestNodes.append(node)
            elif node > bestNodes[0]:
                bestNodes = [node]
            elif node == bestNodes[0]:
                bestNodes.append(node)
        return [node.move for node in bestNodes]

class quiescentAgent(minimaxAgent):
    ''' An agent performs a quiescent search, but limiting the
        upper bound of level of searching to 4.'''
    def populateNodeChildren(self, node):
        if not isinstance(node, MoveNode):
            raise TypeError('Bad argument given.')
        node.depth = node.getDepth()
        # Change: The depth may exceed the search level.
        if node.depth >= self.depth + 2:
            node.pointAdvantage = evaluateBoard(self.board, self.side)
            return
        elif node.depth >= self.depth:
            has_child = 0
            legalMoves = self.getLegalMoves()
            if not legalMoves:
                if self.board.is_checkmate():
                    return
                elif self.board.is_stalemate():
                    node.pointAdvantage = 0
                    return
                else:
                    raise TypeError('Invalid board status.')
            for move in legalMoves:
                if self.board.is_capture(move):
                    has_child = 1
                    node.children.append(MoveNode(move, [], node))
                    self.board.push(move)
                    self.populateNodeChildren(node.children[-1])
                    self.board.pop()
            if has_child == 0:
                node.pointAdvantage = evaluateBoard(self.board, self.side)
                return
            else:
                node.pointAdvantage = 0
        else:
            node.pointAdvantage = 0
        legalMoves = self.getLegalMoves()
        if not legalMoves:
            if self.board.is_checkmate():
                return
            elif self.board.is_stalemate():
                node.pointAdvantage = 0
                return
            else:
                raise TypeError('Invalid board status.')
        for move in legalMoves:
            node.children.append(MoveNode(move, [], node))
            self.board.push(move)
            self.populateNodeChildren(node.children[-1])
            self.board.pop()