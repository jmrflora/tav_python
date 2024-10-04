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
        if total == 3:  # Vitória do jogador aleatório (soma 3)
            return 1
        elif total == -3:  # Vitória da IA (soma -3)
            return -1
    return 0  # Sem vencedor


def check_draw():
    # Verifica se houve empate (todas as posições preenchidas)
    return board[0] == 9


def random_player_move():
    # Movimento aleatório do jogador
    available_moves = [i for i in range(1, 10) if board[i] == 0]
    if available_moves:  # Certificar que há movimentos disponíveis
        move = random.choice(available_moves)
        board[move] = 1  # Jogador aleatório é representado por 1
        board[0] += 1  # Incrementa o número de jogadas
        print(f"Jogador aleatório escolheu a jogada {move}")


def ai_move():
    for i in range(1, 10):
        if board[i] == 0:
            board[i] = -1
            if check_winner() == -1:  # Se a IA vencer com essa jogada
                board[0] += 1
                # print(f"IA escolhe a jogada {i} para vencer.")
                return
            board[i] = 0  # Desfaz o movimento
    for i in range(1, 10):
        if board[i] == 0:
            board[i] = 1
            if check_winner() == 1:  # Se o jogador vencer com essa jogada
                board[i] = -1  # Bloqueia o jogador
                board[0] += 1
                # print(f"IA escolhe a jogada {i} para bloquear.")
                return
            board[i] = 0  # Desfaz o movimento

    if board[0] == 0:
        board[3] = -1
        board[0] += 1
        return
    else:
        if board[0] == 1 and (
            board[1] == 0 and board[3] == 0 and board[7] == 0 and board[9] == 0
        ):
            pass
        else:
            if board[5] == 0:
                board[5] = -1
                board[0] += 1
                return

    if board[6] == 0 and board[9] == 0:
        board[9] = -1
        board[0] += 1
        return
    else:
        if board[1] == 0 and board[2] == 0:
            board[1] = -1
            board[0] += 1
            return
        else:
            if board[4] == 0 and board[7] == 0:
                board[7] = -1
                board[0] += 1
                return


def detect_trap():
    # Possíveis armadilhas (o jogador tem dois "X" e uma posição está livre)
    trap_conditions = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],  # Linhas
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],  # Colunas
        [1, 5, 9],
        [3, 5, 7],  # Diagonais
    ]

    # Verifica se há uma armadilha
    for condition in trap_conditions:
        x_count = sum(1 for i in condition if board[i] == 1)  # Contar os X's
        empty_count = sum(
            1 for i in condition if board[i] == 0
        )  # Contar posições vazias

        # Armadilha detectada: duas posições com X e uma vazia
        if x_count == 2 and empty_count == 1:
            for i in condition:
                if board[i] == 0:  # Encontra a posição vazia
                    print(
                        f"Armadilha detectada na posição {i}. IA bloqueará essa posição."
                    )
                    board[i] = -1  # IA bloqueia essa posição
                    board[0] += 1  # Incrementa a contagem de jogadas
                    return True  # Armadilha detectada e bloqueada

    return False  # Nenhuma armadilha detectada


def ai_move_second_player():
    # 1. Detectar armadilhas e bloqueá-las
    if detect_trap():
        return  # Se a IA bloqueou uma armadilha, a jogada está completa

    # 2. Verifica se o jogador pode vencer na próxima jogada e bloqueia
    for i in range(1, 10):
        if board[i] == 0:
            board[i] = 1  # Simula a jogada do jogador
            if check_winner() == 1:  # Se o jogador vencer com essa jogada
                board[i] = -1  # Bloqueia o jogador
                board[0] += 1
                # print(f"IA escolhe a jogada {i} para bloquear.")
                return
            board[i] = 0  # Desfaz a simulação

    # 3. Verifica se a IA pode vencer
    for i in range(1, 10):
        if board[i] == 0:
            board[i] = -1  # Simula a jogada da IA
            if check_winner() == -1:  # Se a IA vencer com essa jogada
                board[0] += 1
                # print(f"IA escolhe a jogada {i} para vencer.")
                return
            board[i] = 0  # Desfaz a simulação

    # 4. Se o centro estiver livre, joga no centro
    if board[5] == 0:
        board[5] = -1
        board[0] += 1
        # print("IA escolhe a jogada 5 (centro).")
        return

    # 5. Joga nos cantos se disponíveis
    for i in [1, 3, 7, 9]:
        if board[i] == 0:
            board[i] = -1  # IA joga em um canto
            board[0] += 1
            # print(f"IA escolhe a jogada {i} (canto).")
            return

    # 6. Se nenhum canto estiver disponível, joga nas laterais
    for i in [2, 4, 6, 8]:
        if board[i] == 0:
            board[i] = -1  # IA joga na lateral
            board[0] += 1
            # print(f"IA escolhe a jogada {i} (lateral).")
            return


def play_game():
    # Pergunta quem deve começar aleatoriamente
    first_move = "ia"
    print(f"Primeiro a jogar: {first_move}")

    # Controle do turno
    while True:
        if first_move == "jogador":
            # Jogada do jogador aleatório
            random_player_move()
            # print_board()
            if check_winner() == 1:
                print("Jogador aleatório venceu!")
                return 1  # Jogador venceu
            if check_draw():
                print("Empate!")
                return 0  # Empate
            first_move = "ia"  # Passa o turno para a IA

        if first_move == "ia":
            # Jogada da IA
            ai_move_second_player()
            # print_board()
            if check_winner() == -1:
                print("A IA venceu!")
                return -1  # IA venceu
            if check_draw():
                print("Empate!")
                return 0  # Empate
            first_move = "jogador"  # Passa o turno para o jogador


def main():
    # Número de jogos
    num_games = int(input("Quantas partidas você quer jogar? "))

    # Variáveis de contagem de vitórias
    ia_wins = 0
    player_wins = 0
    draws = 0

    # Loop de jogos
    for _ in range(num_games):
        initialize_board()
        result = play_game()
        if result == -1:
            ia_wins += 1
        elif result == 1:
            player_wins += 1
        else:
            draws += 1

    # Cálculo do winrate
    print("\nResultados após", num_games, "jogos:")
    print(f"Vitórias da IA: {ia_wins}")
    print(f"Vitórias do jogador: {player_wins}")
    print(f"Empates: {draws}")
    print(f"Winrate da IA: {ia_wins / num_games * 100:.2f}%")
    print(f"Winrate do jogador: {player_wins / num_games * 100:.2f}%")
    print(f"Empates: {draws / num_games * 100:.2f}%")


if __name__ == "__main__":
    main()
