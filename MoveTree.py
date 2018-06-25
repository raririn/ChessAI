class MoveNode:
    def __init__(self, move, children, parent):
        self.move = move
        self.children = children
        self.parent = parent
        pointAdvantage = None
        depth = 1    

    def getDepth(self):
        return self.depth