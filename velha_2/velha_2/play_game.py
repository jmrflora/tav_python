from collections.abc import Callable
from enum import Enum
from typing import List

from .random_player import random_player_move
from .player_otimo import otimo_move


class Mode(Enum):
    RVR = "random_vs_random"
    RVO = "random_vs_otimo"
    OVO = "otimo_vs_otimo"
    OVR = "otimo_vs_random"


def play_game(
    mode: Mode,
    make_move: Callable[[int, int], bool],
    board: List[int],
    check_winner: Callable[[], int],
    check_draw: Callable[[], int],
    reset_move: Callable[[int], None],
):
    match mode:
        case Mode.RVR:
            first_move = "jogador1"
            while True:
                if first_move == "jogador1":
                    random_player_move(1, make_move, board)  # Jogador 1 joga como X
                    if check_winner() == 1:
                        return 1  # Jogador 1 venceu
                    if check_draw():
                        return 0  # Empate
                    first_move = "jogador2"
                elif first_move == "jogador2":
                    random_player_move(-1, make_move, board)  # Jogador 2 joga como O
                    if check_winner() == -1:
                        return -1  # Jogador 2 venceu
                    if check_draw():
                        return 0  # Empate
                    first_move = "jogador1"
        case Mode.RVO:

            first_move = "jogador"

            while True:
                if first_move == "jogador":
                    random_player_move(
                        1, make_move, board
                    )  # Jogador aleatório joga como jogador 1 (X)
                    if check_winner() == 1:
                        return 1  # Jogador aleatório venceu
                    if check_draw():
                        return 0  # Empate
                    first_move = "ia"
                elif first_move == "ia":
                    otimo_move(
                        -1, make_move, check_winner, reset_move, board
                    )  # IA joga como jogador -1 (O)
                    if check_winner() == -1:
                        return -1  # IA venceu
                    if check_draw():
                        return 0  # Empate
                    first_move = "jogador"
        case mode.OVO:

            first_move = "ia1"
            while True:
                if first_move == "ia1":
                    otimo_move(
                        1, make_move, check_winner, reset_move, board
                    )  # IA 1 joga como jogador 1 (X)

                    if check_winner() == 1:
                        return 1  # IA 1 venceu
                    if check_draw():
                        return 0  # Empate
                    first_move = "ia2"
                elif first_move == "ia2":
                    otimo_move(
                        -1, make_move, check_winner, reset_move, board
                    )  # IA 2 joga como jogador -1 (O)

                    if check_winner() == -1:
                        return -1  # IA 2 venceu
                    if check_draw():
                        return 0  # Empate
                    first_move = "ia1"
        case mode.OVR:

            first_move = "ia"

            while True:
                if first_move == "jogador":
                    random_player_move(
                        1, make_move, board
                    )  # Jogador aleatório joga como jogador 1 (X)
                    if check_winner() == 1:
                        return 1  # Jogador aleatório venceu
                    if check_draw():
                        return 0  # Empate
                    first_move = "ia"
                elif first_move == "ia":
                    otimo_move(
                        -1, make_move, check_winner, reset_move, board
                    )  # IA joga como jogador -1 (O)
                    if check_winner() == -1:
                        return -1  # IA venceu
                    if check_draw():
                        return 0  # Empate
                    first_move = "jogador"
