import random

import matplotlib.pyplot as plt


from typing import Callable, List

# Parâmetros do Q-Learning
ALPHA = 0.1  # Taxa de aprendizado
GAMMA = 0.9  # Fator de desconto
EPSILON = 0.2  # Taxa de exploração


def make_move(player: int, position: int, board: List[int]) -> bool:
    # Atualiza o tabuleiro com o movimento
    if board[position] == 0:
        board[position] = player
        board[0] += 1  # Incrementa o número de jogadas
        return True
    print("invalida")
    print(position)
    return False  # Jogada inválida


def initialize_board():

    board = [0] + [0 for _ in range(9)]  # posição 0 para o contador de jogadas
    return board


def check_winner(board):
    win_conditions = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],  # Linhas
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],  # Colunas
        [1, 5, 9],
        [3, 5, 7],  # Diagonais
    ]
    for condition in win_conditions:
        total = sum(board[i] for i in condition)
        if total == 3:
            return 1  # Jogador 1 vence
        if total == -3:
            return -1  # Jogador 2 vence
    return 0  # Sem vencedor


# Define se é empate
def check_draw(board):
    return board[0] == 9


# Inicializa o tabuleiro com 10 posições (posição 0 é a contagem de jogadas)

# Inicializa a Q-Table
Q_table = {}


def available_moves(board):
    return [i for i in range(1, 10) if board[i] == 0]


def get_Q_value(state, action):
    return Q_table.get((tuple(state), action), 0)


def update_Q_table(state, action, reward, next_state):
    old_value = get_Q_value(state, action)
    future_rewards = max(
        [get_Q_value(next_state, a) for a in available_moves(next_state)], default=0
    )
    new_value = old_value + ALPHA * (reward + GAMMA * future_rewards - old_value)
    Q_table[(tuple(state), action)] = new_value


# Função de recompensa
def get_reward(board, player):
    winner = check_winner(board)
    if winner == player:
        return 10  # Recompensa para vitória
    elif winner == -player:
        return -10  # Penalidade para derrota
    elif check_draw(board):
        return 5  # Recompensa menor para empate
    else:
        return 0  # Nenhuma recompensa ainda


# Escolhe uma ação baseada em epsilon-greedy
def choose_action(board, player):
    if random.uniform(0, 1) < EPSILON:
        return random.choice(available_moves(board))
    else:
        q_values = {a: get_Q_value(board, a) for a in available_moves(board)}
        max_q = max(q_values.values(), default=0)
        best_actions = [a for a, q in q_values.items() if q == max_q]
        return random.choice(best_actions)


# Treina o agente jogando várias partidas
def train_agent(num_games):
    for _ in range(num_games):
        board = initialize_board()
        player = 1  # O agente começa como jogador 1
        state = board[:]
        done = False

        while not done:
            # Agente escolhe a ação
            action = choose_action(state, player)
            make_move(player, action, board)

            # Calcula a recompensa e atualiza a Q-Table
            reward = get_reward(board, player)
            next_state = board[:]
            update_Q_table(state, action, reward, next_state)

            # Muda para o próximo estado
            state = next_state

            # Alterna jogador
            player *= -1
            if reward != 0 or check_draw(board):
                done = True  # Termina o jogo ao vencer, perder ou empatar


def plot_results(results):
    labels = ["Vitórias", "Derrotas", "Empates"]
    sizes = [results["win"], results["loss"], results["draw"]]
    colors = ["lightblue", "salmon", "lightgray"]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, sizes, color=colors)
    plt.xlabel("Resultados")
    plt.ylabel("Quantidade")
    plt.title("Resultados do Agente no Jogo da Velha")
    plt.grid(axis="y", linestyle="--")
    plt.show()


# Testa o agente treinado
def test_agent(num_games):
    results = {"win": 0, "loss": 0, "draw": 0}
    for _ in range(num_games):
        board = initialize_board()
        player = 1
        done = False

        while not done:
            if player == 1:
                action = choose_action(board, player)
            else:
                action = random.choice(available_moves(board))  # Oponente aleatório
            make_move(player, action, board)

            reward = get_reward(board, player)
            if reward == 10:
                results["win" if player == 1 else "loss"] += 1
                done = True
            elif reward == -10:
                results["loss" if player == 1 else "win"] += 1
                done = True
            elif check_draw(board):
                results["draw"] += 1
                done = True

            player *= -1  # Alterna jogador

    print("Resultados do teste:", results)
    return results


# Executa o treinamento e teste do agente
# train_agent()
# test_agent()
