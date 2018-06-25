from param import *

def evaluateBoard(board, side):
    KING_SCORE = 1000
    QUEEN_SCORE = 9
    ROOK_SCORE = 5
    BISHOP_SCORE = 3
    KNIGHT_SCORE = 3
    PAWN_SCORE = 1
    boardString = board.__str__()

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

    white_score = white_piece_score
    black_score = black_piece_score
    if side == WHITE:
        score = white_score - black_score
    elif side == BLACK:
        score = black_score - white_score
    else:
        raise ValueError('Bad side value.')
    return score