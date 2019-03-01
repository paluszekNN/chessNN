import sys
import chess
from state import Game


def score_(pawn):
    if pawn == chess.Piece(1, chess.BLACK):
        return -1
    if pawn == chess.Piece(2, chess.BLACK):
        return -3
    if pawn == chess.Piece(3, chess.BLACK):
        return -3
    if pawn == chess.Piece(4, chess.BLACK):
        return -5
    if pawn == chess.Piece(5, chess.BLACK):
        return -9
    if pawn == chess.Piece(6, chess.BLACK):
        return -1000
    if pawn == chess.Piece(1, chess.WHITE):
        return 1
    if pawn == chess.Piece(2, chess.WHITE):
        return 3
    if pawn == chess.Piece(3, chess.WHITE):
        return 3
    if pawn == chess.Piece(4, chess.WHITE):
        return 5
    if pawn == chess.Piece(5, chess.WHITE):
        return 9
    if pawn == chess.Piece(6, chess.WHITE):
        return 1000
    if not pawn:
        return 0


def best_move(new_board, game, ai):
    score = 0
    for i in range(64):
        score += score_(new_board.piece_at(i))
    return score


def min_max(board_state, ai, game, max_depth, alpha=-sys.float_info.max, beta=sys.float_info.max):
    best_score_move = None
    new_board = board_state.copy()
    new_game = Game()
    new_game.board_state = new_board
    if not new_board.legal_moves:
        return 0, None

    for move in new_board.legal_moves:
        new_board = board_state.copy()
        new_board.push(move)

        if board_state.turn and new_board.is_checkmate():
            return 10000, move
        if not board_state.turn and new_board.is_checkmate():
            return -10000, move
        if board_state.turn and new_board.is_game_over():
            return -10, move
        if not board_state.turn and new_board.is_game_over():
            return 10, move
        if max_depth <= 1:
            score = best_move(new_board, new_game, ai)
        else:
            score, _ = min_max(new_board, ai, new_game, max_depth -1, alpha, beta)

        if board_state.turn:
            if score > alpha:
                # print(score, ' ', best_score, ' ', best_score_move)
                alpha = score
                best_score_move = move
        else:
            if score < beta:
                beta = score
                best_score_move = move
    # print(best_score_move)
        if alpha >= beta:
            break
    return alpha if not game.board_state.turn else beta, best_score_move


def min_max_player(board, ai, game):
    return min_max(board, ai, game, 2)[1]
