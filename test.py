import chess
from evaluation import *

board = chess.Board('r1b1kbn1/pppp1ppr/2n1p3/8/4P3/8/PPPPBPPN/RNB1K2R w KQkq - 0 80')
print(evaluateBoard(board, 1))
print(board.fen().split(' ')[0])