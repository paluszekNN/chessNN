import torch
from state import Game
from NNtorch import Net
import random
import min_max
import min_max_NN
import chess
import os
import shutil
import time


class AI:
    def __init__(self):
        vals = torch.load("model\model0.12635714165782896.pth", map_location=lambda storage, loc: storage)
        self.model = Net()
        self.model.load_state_dict(vals)

    def __call__(self, game):
        board = game.transform()[None]
        output = self.model(torch.tensor(board).float())
        return float(output.data[0][0])


def random_player(moves):
    moves_rand = []
    for i in moves:
        moves_rand.append(i)
    if moves_rand != []:
        return random.choice(moves_rand)
    else:
        return None


def best_move(game, ai, whose_move):
    max = -1.1
    min = 1.1
    best_move = None

    if whose_move:
        for move in game.moves():
            game.board_state.push(move)
            if ai(game) > max:
                max = ai(game)
                best_move = move
            game.board_state.pop()
        print(best_move, max)
        return best_move
    else:
        for move in game.moves():
            game.board_state.push(move)
            if ai(game) < min:
                min = ai(game)
                best_move = move
            game.board_state.pop()
        print(best_move, min)
        return best_move


def game_ai(player1, player2, game):
    while True:
        board_state = game.board_state.copy()
        move = min_max.min_max_player(board_state, player1, game)
        game.board_state = board_state
        game.board_state.push(move)
        print('ai move \n')
        print(game.board_state)
        if game.board_state.is_checkmate():
            return 1
        if game.board_state.is_game_over():
            break

        board_state = game.board_state.copy()
        move = min_max.min_max_player(board_state, player2, game)
        game.board_state = board_state
        game.board_state.push(move)
        print('ai move \n')
        print(game.board_state)
        if game.board_state.is_checkmate():
            return -1
        if game.board_state.is_game_over():
            break
    return 0


def score_ai():
    wyniki = [0, 0, 0, 0]
    ai = []
    for fn in os.listdir("wyniki_model"):
        print(fn)
        path = os.path.join("wyniki_model", fn)
        ai.append(AI(path))
    for _ in range(1):

        game = Game()
        wynik = game_ai(ai[1], ai[0], game)
        if wynik == 0:
            wyniki[1] += 0.5
            wyniki[0] += 0.5
        elif wynik == -1:
            wyniki[0] += 1
        else:
            wyniki[1] += 1

        game = Game()
        wynik = game_ai(ai[0], ai[1], game)
        if wynik == 0:
            wyniki[1] += 0.5
            wyniki[0] += 0.5
        elif wynik == -1:
            wyniki[1] += 1
        else:
            wyniki[0] += 1

        game = Game()
        wynik = game_ai(ai[2], ai[0], game)
        if wynik == 0:
            wyniki[2] += 0.5
            wyniki[0] += 0.5
        elif wynik == -1:
            wyniki[0] += 1
        else:
            wyniki[2] += 1

        game = Game()
        wynik = game_ai(ai[0], ai[2], game)
        if wynik == 0:
            wyniki[0] += 0.5
            wyniki[2] += 0.5
        elif wynik == -1:
            wyniki[2] += 1
        else:
            wyniki[0] += 1

        game = Game()
        wynik = game_ai(ai[3], ai[0], game)
        if wynik == 0:
            wyniki[3] += 0.5
            wyniki[0] += 0.5
        elif wynik == -1:
            wyniki[0] += 1
        else:
            wyniki[3] += 1

        game = Game()
        wynik = game_ai(ai[0], ai[3], game)
        if wynik == 0:
            wyniki[3] += 0.5
            wyniki[0] += 0.5
        elif wynik == -1:
            wyniki[3] += 1
        else:
            wyniki[0] += 1

        game = Game()
        wynik = game_ai(ai[1], ai[2], game)
        if wynik == 0:
            wyniki[1] += 0.5
            wyniki[2] += 0.5
        elif wynik == -1:
            wyniki[2] += 1
        else:
            wyniki[1] += 1

        game = Game()
        wynik = game_ai(ai[2], ai[1], game)
        if wynik == 0:
            wyniki[1] += 0.5
            wyniki[2] += 0.5
        elif wynik == -1:
            wyniki[1] += 1
        else:
            wyniki[2] += 1

        game = Game()
        wynik = game_ai(ai[2], ai[3], game)
        if wynik == 0:
            wyniki[2] += 0.5
            wyniki[3] += 0.5
        elif wynik == -1:
            wyniki[3] += 1
        else:
            wyniki[2] += 1

        game = Game()
        wynik = game_ai(ai[3], ai[2], game)
        if wynik == 0:
            wyniki[3] += 0.5
            wyniki[2] += 0.5
        elif wynik == -1:
            wyniki[2] += 1
        else:
            wyniki[3] += 1

        game = Game()
        wynik = game_ai(ai[3], ai[1], game)
        if wynik == 0:
            wyniki[3] += 0.5
            wyniki[1] += 0.5
        elif wynik == -1:
            wyniki[1] += 1
        else:
            wyniki[3] += 1

        game = Game()
        wynik = game_ai(ai[1], ai[3], game)
        if wynik == 0:
            wyniki[3] += 0.5
            wyniki[1] += 0.5
        elif wynik == -1:
            wyniki[3] += 1
        else:
            wyniki[1] += 1


if __name__ == '__main__':
    # for fn in os.listdir("model"):
    #     path = os.path.join("model", fn)
        ai = AI()
        game = Game()
        while True:
            # try:
            #     game.board_state.push(best_move(game, ai, game.board_state.turn))
            # except:
            #     break
            # print('ai move \n')
            # print(game.board_state)
            # if game.board_state.is_checkmate():
            #     shutil.copyfile(path, "random_"+path)
            # if game.board_state.is_game_over():
            #     break
            time_move = time.time()
            # try:
            board_state = game.board_state.copy()
            move = min_max_NN.min_max_player(board_state, ai, game)
            game.board_state = board_state

            game.board_state.push(move)
            print('ai move \n')
            print(game.board_state)
            # if game.board_state.is_checkmate():
            #     shutil.copyfile(path, "NN_" + path)
            if game.board_state.is_game_over():
                break
            # except:
            #     break

            print(time.time() - time_move)
            # input('wcisnij enter')
            # board_state = game.board_state.copy()
            # move = min_max.min_max_player(board_state, ai, game)
            # game.board_state = board_state
            # game.board_state.push(move)
            # print('ai move \n')
            # print(game.board_state)
            # if game.board_state.is_game_over():
            #     break

            # game.board_state.push(random_player(game.board_state.legal_moves))
            # print('random move\n')
            # print(game.board_state)

            while True:
                try:
                    move = input("move human")
                    if chess.Move.from_uci(move) in game.board_state.legal_moves:
                        break
                except:
                    pass
            game.board_state.push(chess.Move.from_uci(move))
            print(game.board_state)
            if game.board_state.is_game_over():
                break

        # print(wyniki)