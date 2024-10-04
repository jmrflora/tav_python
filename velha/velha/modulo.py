import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
BOARD_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)  # White
CIRCLE_COLOR = (255, 255, 255)  # White
CROSS_COLOR = (255, 255, 255)  # Blue
CIRCLE_RADIUS = 35  # Reduced radius
CIRCLE_WIDTH = 6  # Reduced width
CROSS_WIDTH = 15
SPACE = 30

# Font settings
font = pygame.font.Font(pygame.font.match_font("arial"), 30)
font_big = pygame.font.Font(pygame.font.match_font("arial"), 50)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")


def draw_board():
    screen.fill(BOARD_COLOR)
    # Horizontal lines
    pygame.draw.line(
        screen, LINE_COLOR, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), LINE_WIDTH
    )
    pygame.draw.line(
        screen, LINE_COLOR, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), LINE_WIDTH
    )
    # Vertical lines
    pygame.draw.line(
        screen, LINE_COLOR, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), LINE_WIDTH
    )
    pygame.draw.line(
        screen, LINE_COLOR, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), LINE_WIDTH
    )


def draw_x(row, col):
    start_x = col * WIDTH // 3 + SPACE
    start_y = row * HEIGHT // 3 + SPACE
    end_x = (col + 1) * WIDTH // 3 - SPACE
    end_y = (row + 1) * HEIGHT // 3 - SPACE
    pygame.draw.line(
        screen, CROSS_COLOR, (start_x, start_y), (end_x, end_y), CROSS_WIDTH
    )
    pygame.draw.line(
        screen, CROSS_COLOR, (start_x, end_y), (end_x, start_y), CROSS_WIDTH
    )


def draw_o(row, col):
    center_x = (col * WIDTH // 3 + (col + 1) * WIDTH // 3) // 2
    center_y = (row * HEIGHT // 3 + (row + 1) * HEIGHT // 3) // 2
    pygame.draw.circle(
        screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH
    )


def draw_marks(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                draw_x(row, col)
            elif board[row][col] == "O":
                draw_o(row, col)


def draw_message(message):
    text = font_big.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Draw background rectangle
    background_rect = pygame.Rect(
        text_rect.left - 10,
        text_rect.top - 10,
        text_rect.width + 20,
        text_rect.height + 20,
    )
    pygame.draw.rect(
        screen, (0, 0, 0, 180), background_rect
    )  # Semi-transparent black background

    screen.blit(text, text_rect)


def check_winner(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != "":
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    return None


def is_board_full(board):
    return all(cell != "" for row in board for cell in row)


def main():
    board = [["" for _ in range(3)] for _ in range(3)]
    player = "X"
    game_over = False

    draw_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                row = y // (HEIGHT // 3)
                col = x // (WIDTH // 3)

                if board[row][col] == "":
                    board[row][col] = player
                    player = "O" if player == "X" else "X"
                    draw_board()
                    draw_marks(board)
                    winner = check_winner(board)
                    if winner:
                        draw_message(f"Player {winner} wins!")
                        game_over = True
                    elif is_board_full(board):
                        draw_message("It's a draw!")
                        game_over = True

        pygame.display.update()


if __name__ == "__main__":
    main()
