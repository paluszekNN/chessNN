import chess
import numpy as np


class Game:
    def __init__(self, board = None):
        if board is None:
            self.board_state = chess.Board()
        else:
            self.board_state = board

    def transform(self):
        bstate = np.zeros(64, np.uint8)
        bstate_dict = {'P': 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6,
                     'p': 7, "n": 8, "b": 9, "r": 10, "q": 11, "k": 0}

        bstate = bstate.reshape(8, 8)

        state = np.zeros((20, 8, 8), np.uint8)

        for i in range(8):
            for j in range(8):
                pp = self.board_state.piece_at(i*8+j)
                if pp is not None:
                    state[bstate_dict[pp.symbol()], i, j] = 1

        state[12] = self.board_state.turn * 1.0
        # if self.board_state.is_check():
        #     state[4] = 1
        if self.board_state.has_kingside_castling_rights(chess.WHITE):
            state[13] = 1
        if self.board_state.has_queenside_castling_rights(chess.WHITE):
            state[14] = 1
        if self.board_state.has_kingside_castling_rights(chess.BLACK):
            state[15] = 1
        if self.board_state.has_queenside_castling_rights(chess.BLACK):
            state[16] = 1
        if self.board_state.has_legal_en_passant():
            state[17] = 1
        if self.board_state.is_fivefold_repetition():
            state[18] = 1
        # if self.board_state.is_stalemate():
        #     state[10] = 1

        # if self.board_state.is_insufficient_material():
        #     state[12] = 1
        # if self.board_state.is_checkmate():
        #     state[13] = 1
        # if self.board_state.can_claim_draw():
        #     state[14] = 1
        # if self.board_state.can_claim_fifty_moves():
        #     state[15] = 1
        if self.board_state.can_claim_threefold_repetition():
            state[19] = 1
        # if self.board_state.has_pseudo_legal_en_passant():
        #     state[17] = 1

        # j_P, j_p, j_N, j_n, j_B, j_b, j_R, j_r, j_Q, j_q, j_K, j_k = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        # for i in range(64):
        #     if self.board_state.piece_at(i) == chess.Piece(1, chess.WHITE):
        #         j_P += 1
        #         state[18+j_P] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(1, chess.BLACK):
        #         j_p += 1
        #         state[26+j_p] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(2, chess.WHITE):
        #         j_N += 1
        #         if j_N > 2:
        #             continue
        #         state[34+j_N] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(2, chess.BLACK):
        #         j_n += 1
        #         if j_n > 2:
        #             continue
        #         state[36+j_n] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(3, chess.WHITE):
        #         j_B += 1
        #         if j_B > 2:
        #             continue
        #         state[38+j_B] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(3, chess.BLACK):
        #         j_b += 1
        #         if j_b > 2:
        #             continue
        #         state[40+j_b] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(4, chess.WHITE):
        #         j_R += 1
        #         if j_R > 3:
        #             continue
        #         state[42+j_R] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(4, chess.BLACK):
        #         j_r += 1
        #         if j_r > 3:
        #             continue
        #         state[45+j_r] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(6, chess.WHITE):
        #         j_K += 1
        #         state[48+j_K] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(6, chess.BLACK):
        #         j_k += 1
        #         state[49+j_k] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(5, chess.WHITE):
        #         j_Q += 1
        #         if j_Q > 2:
        #             continue
        #         state[50+j_Q] = 1
        #     if self.board_state.piece_at(i) == chess.Piece(5, chess.BLACK):
        #         j_q += 1
        #         if j_q > 2:
        #             continue
        #         state[52+j_q] = 1

        return state

    def moves(self):
        return list(self.board_state.legal_moves)


if __name__ == '__main__':
    s = Game()
    suma= 0
    # print(s.transform())
    for i in s.transform():
        for j in i:
            for k in j:
                if k == 1:
                    suma+=1

    print(suma)