import random

# Inicialização do tabuleiro com 10 posições
# A posição 0 armazena a quantidade de jogadas
# As posições de 1 a 9 representam o tabuleiro
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
                print(f"IA escolhe a jogada {i} para vencer.")
                return
            board[i] = 0  # Desfaz o movimento
    for i in range(1, 10):
        if board[i] == 0:
            board[i] = 1
            if check_winner() == 1:  # Se o jogador vencer com essa jogada
                board[i] = -1  # Bloqueia o jogador
                board[0] += 1
                print(f"IA escolhe a jogada {i} para bloquear.")
                return
            board[i] = 0  # Desfaz o movimento

    if board[0] == 0:
        board[3] = -1
        board[0] += 1
        return
    else:
        if board[0] == 1 and (
            board[1] == 1 or board[3] == 1 or board[7] == 1 or board[9] == 1
        ):
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


def main():
    print(
        "Bem-vindo ao Jogo da Velha: Jogador Aleatório vs IA com Estratégia de Cantos!"
    )

    # Pergunta quem deve começar
    first_move = "ia"

    # Controle do turno
    while True:
        if first_move == "jogador":
            # Jogada do jogador aleatório
            random_player_move()
            print_board()
            if check_winner() == 1:
                print("Jogador aleatório venceu!")
                break
            if check_draw():
                print("Empate!")
                break
            first_move = "ia"  # Passa o turno para a IA

        if first_move == "ia":
            # Jogada da IA
            ai_move()
            print_board()
            if check_winner() == -1:
                print("A IA venceu!")
                break
            if check_draw():
                print("Empate!")
                break
            first_move = "jogador"  # Passa o turno para o jogador


if __name__ == "__main__":
    main()
