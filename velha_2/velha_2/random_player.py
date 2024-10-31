import random
from typing import List, Callable


def random_player_move(
    player: int, movement_func: Callable[[int, int], bool], board: List[int]
) -> None:
    # Movimento aleatório do jogador

    available_moves = [i for i in range(1, 10) if board[i] == 0]
    if available_moves:
        move = random.choice(available_moves)
        movement_func(player, move)
