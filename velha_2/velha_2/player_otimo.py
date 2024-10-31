from typing import List, Callable


from .random_player import random_player_move


def is_cantos_disponiveis(board: List[int]):
    if board[1] == 0 and board[3] == 0 and board[7] == 0 and board[9] == 0:
        return True


def ai_second_move(
    player: int,
    make_move: Callable[[int, int], bool],
    check_winner: Callable[[], int],
    reset_move: Callable[[int], None],
    board: List[int],
):
    # Função da IA para tentar vencer ou bloquear
    for i in range(1, 10):
        if board[i] == 0:
            make_move(player, i)
            if check_winner() == player:  # Se a IA vencer com essa jogada
                return
            reset_move(i)
    for i in range(1, 10):
        if board[i] == 0:
            make_move(-player, i)
            if check_winner() == -player:  # Se o jogador vencer com essa jogada
                reset_move(i)
                make_move(player, i)
                return
            reset_move(i)

    if board[0] == 1:
        if not is_cantos_disponiveis(board):
            make_move(player, 5)
            return
        else:
            if board[5] == -player or board[2] == -player or board[4] == -player:
                make_move(player, 1)
                return
            make_move(player, 9)
            return
    if board[0] == 3:
        if board[1] == player and board[5] != player:
            if board[9] == -player and board[5] == -player:
                make_move(player, 3)
                return

            make_move(player, 5)
            return
        elif board[5] == 0:
            make_move(player, 5)
            return
        else:
            if board[1] == -player:
                if board[8] == -player:
                    make_move(player, 9)
                    return
                elif board[6] == -player:
                    make_move(player, 3)
                    return
                elif board[9] == -player:
                    make_move(player, 8)
                return
            elif board[3] == -player:
                if board[4] == -player:
                    make_move(player, 1)
                    return
                elif board[7] == -player:
                    make_move(player, 8)
                    return
                elif board[8] == -player:
                    make_move(player, 9)
                    return
            elif board[7] == -player:
                if board[2] == -player:
                    make_move(player, 1)
                    return
                if board[3] == -player:
                    make_move(player, 2)
                    return
                if board[6] == -player:
                    make_move(player, 9)
                return
            elif board[9] == -player:
                if board[4] == -player:
                    make_move(player, 7)
                    return
                if board[1] == -player:
                    make_move(player, 2)
                    return
                if board[2] == -player:
                    make_move(player, 3)
                return
    if is_cantos_disponiveis(board):
        if board[1] == 0:
            make_move(player, 1)
            return
        elif board[3] == 0:
            make_move(player, 3)
            return
        elif board[7] == 0:
            make_move(player, 7)
            return
        else:
            make_move(player, 9)
            return
    random_player_move(player, make_move, board)
    return


def otimo_move(
    player: int,
    make_move: Callable[[int, int], bool],
    check_winner: Callable[[], int],
    reset_move: Callable[[int], None],
    board: List[int],
) -> None:
    if board[0] % 2 != 0:
        ai_second_move(player, make_move, check_winner, reset_move, board)
        return

    # Função do npc para tentar vencer ou bloquear
    for i in range(1, 10):
        if board[i] == 0:
            make_move(player, i)
            if check_winner() == player:  # Se a IA vencer com essa jogada
                return
            reset_move(i)
    for i in range(1, 10):
        if board[i] == 0:
            make_move(-player, i)
            if check_winner() == -player:  # Se o jogador vencer com essa jogada
                reset_move(i)
                make_move(player, i)
                return
            reset_move(i)

    if board[0] == 0:
        make_move(player, 3)
        return
    else:
        if board[5] == 0:
            make_move(player, 5)
            return

    if board[6] == 0 and board[9] == 0:
        make_move(player, 9)
        return
    else:
        if board[1] == 0 and board[2] == 0:
            make_move(player, 1)
            return
        else:
            if board[4] == 0 and board[7] == 0:
                make_move(player, 7)
                return
    random_player_move(player, make_move, board)
