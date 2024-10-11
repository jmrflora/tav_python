import random
import matplotlib.pyplot as plt


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
    print("invalida")
    print(position)
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
        # if board[0] == 1:
        #     print("random move")
        #     print(move)
        # print(f"Jogador {player} escolheu a jogada {move}")


def is_cantos_disponiveis():
    if board[1] == 0 and board[3] == 0 and board[7] == 0 and board[9] == 0:
        return True


def ai_second_move(player):
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
        if not is_cantos_disponiveis():
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
    if is_cantos_disponiveis():
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
    random_player_move(player)
    return


def ai_move(player):
    if board[0] % 2 != 0:
        ai_second_move(player)
        return

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
    random_player_move(player)


def choose_first_player():
    # Seleciona aleatoriamente quem começa
    choice = random.choice(["jogador", "ia"])
    # print(f"Primeiro a jogar: {choice}")
    return choice


def play_game(mode):
    if mode == "ia_vs_ia":
        first_move = "ia1"
        while True:
            if first_move == "ia1":
                ai_move(1)  # IA 1 joga como jogador 1 (X)

                if check_winner() == 1:
                    return 1  # IA 1 venceu
                if check_draw():
                    return 0  # Empate
                first_move = "ia2"
            elif first_move == "ia2":
                ai_move(-1)  # IA 2 joga como jogador -1 (O)

                if check_winner() == -1:
                    return -1  # IA 2 venceu
                if check_draw():
                    return 0  # Empate
                first_move = "ia1"
    elif mode == "random_vs_ia":
        first_move = "jogador"
        while True:
            if first_move == "jogador":
                random_player_move(1)  # Jogador aleatório joga como jogador 1 (X)
                if check_winner() == 1:
                    return 1  # Jogador aleatório venceu
                if check_draw():
                    return 0  # Empate
                first_move = "ia"
            elif first_move == "ia":
                ai_move(-1)  # IA joga como jogador -1 (O)
                if check_winner() == -1:
                    return -1  # IA venceu
                if check_draw():
                    return 0  # Empate
                first_move = "jogador"
    elif mode == "random_vs_random":
        first_move = "jogador1"
        while True:
            if first_move == "jogador1":
                random_player_move(1)  # Jogador 1 joga como X
                if check_winner() == 1:
                    return 1  # Jogador 1 venceu
                if check_draw():
                    return 0  # Empate
                first_move = "jogador2"
            elif first_move == "jogador2":
                random_player_move(-1)  # Jogador 2 joga como O
                if check_winner() == -1:
                    return -1  # Jogador 2 venceu
                if check_draw():
                    return 0  # Empate
                first_move = "jogador1"


def main():
    num_games = int(input("Quantas partidas você quer jogar? "))
    game_mode = input(
        "Escolha o modo (ia_vs_ia, random_vs_ia ou random_vs_random): "
    ).strip()

    ia1_wins = 0
    ia2_wins = 0
    player_wins = 0
    draws = 0

    for game_num in range(1, num_games + 1):
        initialize_board()
        result = play_game(game_mode)

        if result == 1:  # Jogador aleatório ou IA 1 venceu
            if game_mode == "random_vs_ia":
                player_wins += 1  # Jogador aleatório venceu
            elif game_mode == "random_vs_random":
                player_wins += 1  # Jogador 1 venceu
            else:
                ia1_wins += 1  # IA 1 venceu
        elif result == -1:  # IA 2 venceu
            ia2_wins += 1
        else:
            draws += 1

    total_games = ia1_wins + ia2_wins + player_wins + draws
    print("\nResultados após", total_games, "jogos:")

    if game_mode == "ia_vs_ia":
        print(f"Vitórias da IA 1 (X): {ia1_wins} ({ia1_wins / total_games * 100:.2f}%)")
        print(f"Vitórias da IA 2 (O): {ia2_wins} ({ia2_wins / total_games * 100:.2f}%)")
    elif game_mode == "random_vs_ia":
        print(
            f"Vitórias do jogador: {player_wins} ({player_wins / total_games * 100:.2f}%)"
        )
        print(f"Vitórias da IA: {ia2_wins} ({ia2_wins / total_games * 100:.2f}%)")
    elif game_mode == "random_vs_random":
        print(
            f"Vitórias do Jogador 1: {player_wins} ({player_wins / total_games * 100:.2f}%)"
        )
        print(
            f"Vitórias do Jogador 2: {ia2_wins} ({ia2_wins / total_games * 100:.2f}%)"
        )

    print(f"Empates: {draws} ({draws / total_games * 100:.2f}%)")

    if game_mode == "ia_vs_ia":
        if ia1_wins > ia2_wins:
            print("\nA IA 1 (X) foi a vencedora geral!")
        elif ia2_wins > ia1_wins:
            print("\nA IA 2 (O) foi a vencedora geral!")
        else:
            print("\nHouve um empate geral!")
    elif game_mode == "random_vs_random":
        if player_wins > ia2_wins:
            print("\nO Jogador 1 foi o vencedor geral!")
        elif ia2_wins > player_wins:
            print("\nO Jogador 2 foi o vencedor geral!")
        else:
            print("\nHouve um empate geral!")
    else:
        if player_wins > ia2_wins:
            print("\nO jogador foi o vencedor geral!")
        elif ia2_wins > player_wins:
            print("\nA IA foi a vencedora geral!")
        else:
            print("\nHouve um empate geral!")

    # Gráfico de resultados
    labels = []
    sizes = []

    # Adiciona apenas quem jogou
    if game_mode == "random_vs_ia":
        labels = ["Jogador", "IA"]
        sizes = [player_wins, ia2_wins]
    elif game_mode == "random_vs_random":
        labels = ["Jogador 1", "Jogador 2"]
        sizes = [player_wins, ia2_wins]
    elif game_mode == "ia_vs_ia":
        labels = ["IA 1", "IA 2"]
        sizes = [ia1_wins, ia2_wins]

    # Adicionando empates como última label
    sizes.append(draws)
    labels.append("Empates")

    colors = ["lightblue", "lightgreen", "salmon", "lightgray"]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, sizes, color=colors)
    plt.xlabel("Resultados")
    plt.ylabel("Quantidade de Vitórias")
    plt.title("Resultados do Jogo da Velha (com Empates)")
    plt.grid(axis="y", linestyle="--")
    plt.show()


if __name__ == "__main__":
    main()
