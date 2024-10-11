import random


# Inicialização do tabuleiro com 10 posições
# A posição 0 armazena a quantidade de jogadas
# As posições de 1 a 9 representam o tabuleiro
def initialize_board():
    global board
    board = [0] + [0 for _ in range(9)]  # 0 significa posição vazia


def print_board():
    # Exibe o tabuleiro convertendo os números em símbolos
    symbols = {1: "X", -1: "O", 0: " "}
    print("---------")
    for row in [board[i : i + 3] for i in range(1, 10, 3)]:
        print("| " + " | ".join(symbols[cell] for cell in row) + " |")
        print("---------")


def check_winner():
    # Condições de vitória (soma dos elementos)
    win_conditions = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],  # linhas
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],  # colunas
        [1, 5, 9],
        [3, 5, 7],  # diagonais
    ]
    for condition in win_conditions:
        total = sum(board[i] for i in condition)
        if total == 3:  # Vitória do jogador (soma 3)
            return 1
        elif total == -3:  # Vitória da IA (soma -3)
            return -1
    return 0  # Sem vencedor


def check_draw():
    # Verifica se houve empate (todas as posições preenchidas)
    return board[0] == 9


def make_move(player, position):
    # Atualiza o tabuleiro com o movimento
    if board[position] == 0:
        board[position] = player
        board[0] += 1  # Incrementa o número de jogadas
        return True
    return False  # Jogada inválida


def reset_move(position):
    board[position] = 0
    board[0] -= 1


def random_player_move(player):
    # Movimento aleatório do jogador
    available_moves = [i for i in range(1, 10) if board[i] == 0]
    if available_moves:
        move = random.choice(available_moves)
        make_move(player, move)
        # print(f"Jogador {player} escolheu a jogada {move}")


def ai_second_move():
    # Função da IA para tentar vencer ou bloquear
    for i in range(1, 10):
        if board[i] == 0:
            # board[i] = -1
            make_move(-1, i)
            if check_winner() == -1:  # Se a IA vencer com essa jogada
                return
            # board[i] = 0  # Desfaz o movimento
            reset_move(i)
    for i in range(1, 10):
        if board[i] == 0:
            # board[i] = 1
            make_move(1, i)
            if check_winner() == 1:  # Se o jogador vencer com essa jogada
                # board[i] = -1  # Bloqueia o jogador
                reset_move(i)
                make_move(-1, i)
                # board[0] += 1
                # print(f"IA escolhe a jogada {i} para bloquear.")
                return
            # board[i] = 0  # Desfaz o movimento
            reset_move(i)

    if board[0] == 1:
        if not is_cantos_disponiveis():
            make_move(-1, 5)
            return
        else:
            if board[5] == 1 or board[2] == 1 or board[4] == 1:
                make_move(-1, 1)
                return
            make_move(-1, 9)
            return
    if board[0] == 3:
        if board[1] == -1 and board[5] != -1:
            # if board[2] == 1:
            #     make_move(-1, 5)
            #     return

            if board[9] == 1:
                make_move(-1, 3)
                return

            make_move(-1, 5)
            return
        elif board[5] == 0:
            make_move(-1, 5)
            return

        else:
            if board[1] == 1:
                if board[8] == 1:
                    make_move(-1, 8)
                    return
                elif board[6] == 1:
                    make_move(-1, 3)
                    return
                elif board[9] == 1:
                    make_move(-1, 8)
                return
            elif board[3] == 1:
                if board[4] == 1:
                    make_move(-1, 1)
                    return
                elif board[7] == 1:
                    make_move(-1, 8)
                    return
                elif board[8] == 1:
                    make_move(-1, 9)
                    return
            elif board[7] == 1:
                if board[2] == 1:
                    make_move(-1, 1)
                    return
                if board[3] == 1:
                    make_move(-1, 2)
                    return
                if board[6] == 1:
                    make_move(-1, 9)
                return
            elif board[9] == 1:
                if board[4] == 1:
                    make_move(-1, 7)
                    return
                if board[1] == 1:
                    make_move(-1, 2)
                    return
                if board[2] == 1:
                    make_move(-1, 3)
                return
    random_player_move(-1)
    return


def is_cantos_disponiveis():
    if board[1] == 0 and board[3] == 0 and board[7] == 0 and board[9] == 0:
        return True


def ai_move():
    # Função da IA para tentar vencer ou bloquear
    for i in range(1, 10):
        if board[i] == 0:
            # board[i] = -1
            make_move(-1, i)
            if check_winner() == -1:  # Se a IA vencer com essa jogada
                return
            # board[i] = 0  # Desfaz o movimento
            reset_move(i)
    for i in range(1, 10):
        if board[i] == 0:
            # board[i] = 1
            make_move(1, i)
            if check_winner() == 1:  # Se o jogador vencer com essa jogada
                # board[i] = -1  # Bloqueia o jogador
                reset_move(i)
                make_move(-1, i)
                # board[0] += 1
                # print(f"IA escolhe a jogada {i} para bloquear.")
                return
            # board[i] = 0  # Desfaz o movimento
            reset_move(i)

    if board[0] == 0:
        # board[3] = -1
        # board[0] += 1
        make_move(-1, 3)
        return
    else:
        if board[0] == 1 and (
            board[1] == 0 and board[3] == 0 and board[7] == 0 and board[9] == 0
        ):
            pass
        else:
            if board[5] == 0:
                # board[5] = -1
                # board[0] += 1
                make_move(-1, 5)
                return

    if board[6] == 0 and board[9] == 0:
        # board[9] = -1
        # board[0] += 1
        make_move(-1, 9)
        return
    else:
        if board[1] == 0 and board[2] == 0:
            # board[1] = -1
            # board[0] += 1
            make_move(-1, 1)
            return
        else:
            if board[4] == 0 and board[7] == 0:
                # board[7] = -1
                # board[0] += 1
                make_move(-1, 7)
                return


def choose_first_player():
    # Seleciona aleatoriamente quem começa
    choice = random.choice(["jogador", "ia"])
    # print(f"Primeiro a jogar: {choice}")
    return choice


def play_game():
    first_move = "jogador"
    second = True
    while True:
        # print_board()  # Mostrar tabuleiro a cada jogada
        if first_move == "jogador":
            random_player_move(1)
            if check_winner() == 1:
                # print_board()
                # print("Jogador venceu!")
                return 1
            if check_draw():
                # print_board()
                # print("Empate!")
                return 0
            first_move = "ia"
        elif first_move == "ia":
            if second:
                ai_second_move()
            else:
                ai_move()

            if check_winner() == -1:
                # print_board()
                # print("A IA venceu!")
                return -1
            if check_draw():
                # print_board()
                # print("Empate!")
                return 0
            first_move = "jogador"


def main():
    num_games = int(input("Quantas partidas você quer jogar? "))

    ia_wins = 0
    player_wins = 0
    draws = 0

    for game_num in range(1, num_games + 1):
        # print(f"\nPartida {game_num}:")
        initialize_board()
        result = play_game()

        if result == -1:
            ia_wins += 1
        elif result == 1:
            player_wins += 1
        else:
            draws += 1

    # Cálculo e exibição do relatório
    total_games = ia_wins + player_wins + draws
    print("\nResultados após", total_games, "jogos:")
    print(f"Vitórias da IA: {ia_wins} ({ia_wins / total_games * 100:.2f}%)")
    print(
        f"Vitórias do jogador: {player_wins} ({player_wins / total_games * 100:.2f}%)"
    )
    print(f"Empates: {draws} ({draws / total_games * 100:.2f}%)")

    # Exibe o jogador com mais vitórias
    if ia_wins > player_wins:
        print("\nA IA foi a vencedora geral!")
    elif player_wins > ia_wins:
        print("\nO jogador foi o vencedor geral!")
    else:
        print("\nHouve um empate geral!")


if __name__ == "__main__":
    main()
