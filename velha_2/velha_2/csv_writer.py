import csv


def write_to_csv(game_num, winner, player1_wins, player2_wins, draws):
    # Abre (ou cria) o arquivo CSV e escreve uma linha com os resultados da partida atual
    with open("game_results.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([game_num, winner, player1_wins, player2_wins, draws])
