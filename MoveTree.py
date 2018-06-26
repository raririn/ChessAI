from utils import *

class MoveNode:
    def __init__(self, move, children, parent):
        # Given attributes.
        self.move = move
        self.children = children
        self.parent = parent
        # is_terminal.
        self.is_checkmate = False
        self.is_stalemate = False
        # Inherent attributes.
        self.pointAdvantage = None
        self.depth = 1 

    # --- OLD NOTICE ---
    # Notice on the overloading of camparison operators:
    # If two nodes have equal pointAdvantage, we do NOT
    # treat them as equal, as we want our AI has a random
    # behavior among best strategies. Instead, we set a 
    # 50% chance for the operator to choose one from the
    # two equal values. Two nodes are only equal if both
    # are checkmate state.
    # --- END ---

    def __gt__(self, other):
        if not isinstance(other, MoveNode):
            raise TypeError('Invalid camparison target.')
        if self.is_checkmate and (not other.is_checkmate):
            return True
        elif (not self.is_checkmate) and other.is_checkmate:
            return False
        elif self.is_checkmate and other.is_checkmate:
            return False
        return self.pointAdvantage > other.pointAdvantage
    
    def __lt__(self, other):
        if not isinstance(other, MoveNode):
            raise TypeError('Invalid camparison target.')
        if self.is_checkmate and (not other.is_checkmate):
            return False
        elif (not self.is_checkmate) and other.is_checkmate:
            return True
        elif self.is_checkmate and other.is_checkmate:
            return False
        return self.pointAdvantage > other.pointAdvantage

    def __eq__(self, other):
        if not isinstance(other, MoveNode):
            raise TypeError('Invalid camparison target.')
        if self.is_checkmate and other.is_checkmate:
            return True
        return self.pointAdvantage == other.pointAdvantage

    def findRoot(self):
        root = self
        while root.parent:
            root = root.parent
        return root

    def getDepth(self):
        depth = 1
        root = self
        while True:
            if root.parent:
                if not isinstance(root.parent, MoveNode):
                    raise TypeError('Bad argument type.')
                root = root.parent
                depth = depth + 1
            else:
                return depth