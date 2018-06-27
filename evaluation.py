from param import *
from utils import *

def evaluateBoard(board, side):
    KING_SCORE = 80
    QUEEN_SCORE = 9
    ROOK_SCORE = 5
    BISHOP_SCORE = 3
    KNIGHT_SCORE = 3
    PAWN_SCORE = 1
    MOB_SCORE = 0.2
    CHECKMATE = 2
    boardString = board.fen().split(' ')[0]

    white_rook = boardString.count('R')
    white_king = boardString.count('K')
    white_pawn = boardString.count('P')
    white_queen = boardString.count('Q')
    white_knight = boardString.count('N')
    white_bishop = boardString.count('B')

    white_piece_score = KING_SCORE * white_king + \
    QUEEN_SCORE * white_queen + \
    ROOK_SCORE * white_rook + \
    BISHOP_SCORE * white_bishop + \
    KNIGHT_SCORE * white_knight + \
    PAWN_SCORE * white_pawn


    black_rook = boardString.count('r')
    black_king = boardString.count('k')
    black_pawn = boardString.count('p')
    black_queen = boardString.count('q')
    black_knight = boardString.count('n')
    black_bishop = boardString.count('b')

    black_piece_score = KING_SCORE * black_king + \
    QUEEN_SCORE * black_queen + \
    ROOK_SCORE * black_rook + \
    BISHOP_SCORE * black_bishop + \
    KNIGHT_SCORE * black_knight + \
    PAWN_SCORE * black_pawn

    white_checkmate = 0
    black_checkmate = 0

    if board.turn == WHITE:
        white_mob_score = MOB_SCORE*board.legal_moves.count()
        board.push(chess.Move.null())
        black_mob_score = MOB_SCORE*board.legal_moves.count()
        board.pop()
        if board.is_checkmate():
            black_checkmate = CHECKMATE
    else:
        black_mob_score = MOB_SCORE*board.legal_moves.count()
        board.push(chess.Move.null())
        white_mob_score = MOB_SCORE*board.legal_moves.count()
        board.pop()
        if board.is_checkmate():
            white_checkmate = CHECKMATE


    if side == WHITE:
        #print(white_piece_score)
        #print(black_piece_score)
        #print(white_king)
        #print(black_king)
        score = white_piece_score - black_piece_score + white_mob_score - black_mob_score + \
        white_checkmate - black_checkmate
        #score = white_piece_score - black_piece_score
    elif side == BLACK:
        score = -(white_piece_score - black_piece_score + white_mob_score - black_mob_score + \
        white_checkmate - black_checkmate)
        #score = -(white_piece_score - black_piece_score)
    else:
        raise ValueError('Bad side value.')
    if board.is_stalemate():
        return 0
    
    return score