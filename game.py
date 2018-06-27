from utils import *
from AI import *

def initBoard():
    '''Initialize the board in the first state and return it.'''
    board = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    #board = chess.Board('6k1/6p1/7b/7R/8/8/8/K7 w KQkq - 0 80')    
    return board

def runGame(AI_option, manual_option):
    game = Game(AI_option)
    print(game)
    if manual_option == True:
        while True:
            i = input('Continue?')
            if i != 'quit':
                ret = game.turnPass()
                if ret:
                    print(ret)
                    print('Gameover.')
                    plt.plot(game.score_list)
                    break
                else:
                    print(game)
            else:
                print('User interrupt.')
                break
    else:
        while True:
                ret = game.turnPass()
                if ret:
                    print(ret)
                    print('Gameover.')
                    print( sum(game.white_timelist) / len(game.white_timelist) )
                    print( sum(game.black_timelist) / len(game.black_timelist))
                    plt.plot(game.score_list)
                    plt.show()
                    break
                elif game.turn >= 80:
                    print('Time out.')
                    print(game.score_list)
                    print(game.white_timelist)
                    print(game.black_timelist)
                    print( sum(game.white_timelist) / len(game.white_timelist) )
                    print( sum(game.black_timelist) / len(game.black_timelist))
                    plt.plot(game.score_list)
                    plt.show()
                    break
                else:
                    print(game)
            

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
        self.score_list = []
        self.white_timelist = []
        self.black_timelist = []
    
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
            start_time = time.time()
            # If it's WHITE's turn:
            #agent = quiescentAgent(self.board, WHITE_AI, 2)
            agent = minimaxAgent(self.board, WHITE_AI, 3)
            move = agent.generateMove()
            end_time = time.time()
            print("Performace: " + str(end_time - start_time) + 'sec.')
            if move:
                self.board.push(move)
                print("Current Score for BLACK:" + str(evaluateBoard(self.board, BLACK)))
            else:
                if self.board.is_checkmate():
                    return 'Checkmate. WHITE loses.'
                elif self.board.is_stalemate():
                    return 'Stalemate.'
            self.score_list.append(evaluateBoard(self.board, BLACK))
            self.white_timelist.append(end_time - start_time)

        if self.turn % 2 == 1:
            start_time = time.time()
            # If it's BLACK's turn:
            agent = alphabetaAgent(self.board, BLACK_AI, 3)
            move = agent.generateMove()
            end_time = time.time()
            print("Performace: " + str(end_time - start_time) + 'sec.')
            if move:
                self.board.push(move)
                print("Current Score for WHITE:" + str(evaluateBoard(self.board, WHITE)))
            else:
                if self.board.is_checkmate():
                    return 'Checkmate. BLACK loses.'
                elif self.board.is_stalemate():
                    return 'Stalemate.'
            self.black_timelist.append(end_time - start_time)

        self.turnIncrement()
        return None