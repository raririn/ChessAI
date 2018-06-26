from utils import *
from AI import *

def initBoard():
    '''Initialize the board in the first state and return it.'''
    board = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    return board

def runGame(AI_option):
    game = Game(AI_option)
    print(game)
    while True:
        i = input('Continue?')
        if i != 'quit':
            ret = game.turnPass()
            if ret:
                print(ret)
                print('Gameover.')
                break
            else:
                print(game)
        else:
            print('User interrupt.')
            break

class Game:
    def __init__(self, AI_option):
        if not AI_option in [1,2,3,4]:
            raise ValueError('Inappropiarate AI option.')
        self.AI_option = AI_option
        # Note: the turn counter is about when the operation has not been
        # performed. For example, the first turn is Turn 0 and the turn
        # player is WHITE. After WHITE's operation it's Turn 1 and the 
        # turn player becomes BLACK. In other words, WHITE plays on even
        # turns, and BLACK plays on odd turns.
        self.turn = 0
        self.board = initBoard()
    
    def __str__(self):
        boardInfo = self.board.__str__() + '\n'
        turnInfo = 'Turn:' + str(self.turn) + '\n'
        playerInfo = 'TurnPlayer:' + whichPlayer(self.board.turn)
        return boardInfo + turnInfo + playerInfo

    def turnIncrement(self):
        ''' Increase the turn counter by one. '''
        self.turn = self.turn + 1

    def getLegalMoves(self):
        ''' Return a list of legal moves (for the turn player).'''
        return list(self.board.legal_moves)
    
    def turnPass(self):
        ''' Pass the game by one turn, let AI generate a move if enabled,
            and check if the game is over. Return None if the game is 
            going normally, and return a string containing the state if
            the game is over.'''
        if self.turn % 2 == 0:
            # If it's WHITE's turn:
            agent = greedyAgent(self.board, WHITE_AI, 2)
            move = agent.generateMove()
            if move:
                self.board.push(move)
                print("Current Score for BLACK:" + str(evaluateBoard(self.board, BLACK)))
            else:
                if self.board.is_checkmate():
                    return 'Checkmate. WHITE loses.'
                elif self.board.is_stalemate():
                    return 'Stalemate.'

        if self.turn % 2 == 1:
            # If it's BLACK's turn:
            agent = minimaxAgent(self.board, BLACK_AI, 3)
            move = agent.generateMove()
            if move:
                self.board.push(move)
                print("Current Score for WHITE:" + str(evaluateBoard(self.board, WHITE)))
            else:
                if self.board.is_checkmate():
                    return 'Checkmate. BLACK loses.'
                elif self.board.is_stalemate():
                    return 'Stalemate.'

        self.turnIncrement()
        return None