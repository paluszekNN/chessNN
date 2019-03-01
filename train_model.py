import os
import chess.pgn
import numpy as np
from state import Game


def train():
    input_states = []
    output_states = []
    values = {'1/2-1/2': 0, '0-1': -1, '1-0': 1}
    game_nr = 0
    file_nr = 1
    for fn in os.listdir("KingBase2019-pgn"):
        pgn = open(os.path.join("KingBase2019-pgn", fn))

        while True:
            try:
                game = chess.pgn.read_game(pgn)
            except Exception:
                break

            try:
                result = game.headers['Result']
            except:
                break
            if result not in values:
                continue
            value = values[result]
            if value == 0:
                continue
            board = game.board()
            game_nr += 1
            print('game number ', game_nr)
            for i, move in enumerate(game.mainline_moves()):
                board.push(move)
                ser = Game(board).transform()
                input_states.append(ser)
                output_states.append(value)
            if game_nr % 2000 == 0:
                input_states = np.array(input_states)
                output_states = np.array(output_states)
                path = "train/train_" + str(file_nr) + ".npz"
                np.savez(path, input_states, output_states)
                input_states = []
                output_states = []
                file_nr += 1
    input_states = np.array(input_states)
    output_states = np.array(output_states)
    path = "train/train_" + str(file_nr) + ".npz"
    np.savez(path, input_states, output_states)


if __name__ == '__main__':
    train()
