import random
import csv

import matplotlib.pyplot as plt

from .play_game import Mode, play_game


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


def make_move(player: int, position: int) -> bool:
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


#
# def random_player_move(player):
#     # Movimento aleatório do jogador
#     available_moves = [i for i in range(1, 10) if board[i] == 0]
#     if available_moves:
#         move = random.choice(available_moves)
#         make_move(player, move)
#         # if board[0] == 1:
#         #     print("random move")
#         #     print(move)
#         # print(f"Jogador {player} escolheu a jogada {move}")
#


def write_to_csv(game_num, winner, player1_wins, player2_wins, draws):
    # Abre (ou cria) o arquivo CSV e escreve uma linha com os resultados da partida atual
    with open("game_results.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([game_num, winner, player1_wins, player2_wins, draws])


def main():
    initial_first_move = "jogador"
    num_games = int(input("Quantas partidas você quer jogar? "))

    # Prompt the user to select the game mode based on Mode options
    game_mode_input = input("Escolha o modo (RVR, RVO, OVR, OVO): ").strip().upper()

    # Initialize mode with default if invalid input is given
    mode = Mode.RVR
    match game_mode_input:
        case "RVR":
            mode = Mode.RVR
        case "RVO":
            mode = Mode.RVO
        case "OVR":
            mode = Mode.OVR
        case "OVO":
            mode = Mode.OVO
        case _:
            print("Modo inválido, usando o modo padrão: random_vs_random")

    ia1_wins = 0
    ia2_wins = 0
    player_wins = 0
    draws = 0

    # Cabeçalho do arquivo CSV
    with open("game_results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Número da Partida",
                "Vencedor (1 ou 2)",
                "Vitórias Jogador 1",
                "Vitórias Jogador 2",
                "Empates",
            ]
        )

    for game_num in range(1, num_games + 1):
        initialize_board()
        result = play_game(mode, make_move, board, check_winner, check_draw, reset_move)

        if result == 1:
            match mode:
                case Mode.RVO | Mode.RVR:
                    player_wins += 1
                case _:
                    ia1_wins += 1

        elif result == -1:
            ia2_wins += 1
        else:
            draws += 1

        # Salva o resultado no arquivo CSV
        with open("game_results.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([game_num, result, player_wins, ia2_wins, draws])

    total_games = ia1_wins + ia2_wins + player_wins + draws
    print("\nResultados após", total_games, "jogos:")

    # Output game results based on mode
    if mode == Mode.OVO:
        print(f"Vitórias da IA 1 (X): {ia1_wins} ({ia1_wins / total_games * 100:.2f}%)")
        print(f"Vitórias da IA 2 (O): {ia2_wins} ({ia2_wins / total_games * 100:.2f}%)")
    elif mode == Mode.RVO:
        print(
            f"Vitórias do jogador: {player_wins} ({player_wins / total_games * 100:.2f}%)"
        )
        print(f"Vitórias da IA: {ia2_wins} ({ia2_wins / total_games * 100:.2f}%)")
    elif mode == Mode.RVR:
        print(
            f"Vitórias do Jogador 1: {player_wins} ({player_wins / total_games * 100:.2f}%)"
        )
        print(
            f"Vitórias do Jogador 2: {ia2_wins} ({ia2_wins / total_games * 100:.2f}%)"
        )

    print(f"Empates: {draws} ({draws / total_games * 100:.2f}%)")

    # Determine overall winner based on mode
    if mode == Mode.OVO:
        if ia1_wins > ia2_wins:
            print("\nA IA 1 (X) foi a vencedora geral!")
        elif ia2_wins > ia1_wins:
            print("\nA IA 2 (O) foi a vencedora geral!")
        else:
            print("\nHouve um empate geral!")
    elif mode == Mode.RVR:
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

    # Gráfico de barras de resultados
    labels = []
    sizes = []

    # Adiciona apenas quem jogou
    if mode == Mode.RVO:
        if initial_first_move == "ia":
            labels = ["IA", "aleatorio"]
            sizes = [ia2_wins, player_wins]
        else:
            labels = ["aleatorio", "IA"]
            sizes = [player_wins, ia2_wins]
    elif mode == Mode.RVR:
        labels = ["Jogador 1", "Jogador 2"]
        sizes = [player_wins, ia2_wins]
    elif mode == Mode.OVO:
        labels = ["IA 1", "IA 2"]
        sizes = [ia1_wins, ia2_wins]

    # Adicionando empates
    labels.append("Empates")
    sizes.append(draws)

    colors = ["lightblue", "lightgreen", "salmon", "lightgray"]

    # Gráfico de barras
    plt.figure(figsize=(8, 6))
    plt.bar(labels, sizes, color=colors)
    plt.xlabel("Resultados")
    plt.ylabel("Quantidade de Vitórias")
    plt.title("Resultados do Jogo da Velha (com Empates)")
    plt.grid(axis="y", linestyle="--")
    plt.show()


if __name__ == "__main__":
    main()
