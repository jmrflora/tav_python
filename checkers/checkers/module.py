import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# Create the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


# Piece class
class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(
            win,
            self.color,
            (
                self.col * SQUARE_SIZE + SQUARE_SIZE // 2,
                self.row * SQUARE_SIZE + SQUARE_SIZE // 2,
            ),
            radius,
        )
        if self.king:
            pygame.draw.circle(
                win,
                BLUE,
                (
                    self.col * SQUARE_SIZE + SQUARE_SIZE // 2,
                    self.row * SQUARE_SIZE + SQUARE_SIZE // 2,
                ),
                radius - 5,
            )

    def move(self, row, col):
        self.row = row
        self.col = col


# Board class
class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    self.board[row].append(0)  # Empty square
                elif row < 3:
                    self.board[row].append(Piece(row, col, WHITE))  # White piece
                elif row > 4:
                    self.board[row].append(Piece(row, col, RED))  # Red piece
                else:
                    self.board[row].append(0)  # Empty square

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(
                    win,
                    GREY,
                    (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )

    def get_piece(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None

    def move_piece(self, piece, row, col):
        self.board[piece.row][piece.col] = 0
        piece.move(row, col)
        self.board[row][col] = piece
        if piece.color == WHITE and row == 0:
            piece.make_king()
        elif piece.color == RED and row == ROWS - 1:
            piece.make_king()

    def capture_piece(self, start_row, start_col, end_row, end_col):
        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2
        captured_piece = self.get_piece(middle_row, middle_col)
        if (
            captured_piece
            and captured_piece.color != self.get_piece(start_row, start_col).color
        ):
            self.board[middle_row][middle_col] = 0

    def valid_move(self, piece, row, col):
        # Check bounds
        if not (0 <= row < ROWS and 0 <= col < COLS):
            return False

        # Check if destination is empty
        if self.get_piece(row, col) != 0:
            return False

        # Check if the move is diagonal
        row_diff = abs(row - piece.row)
        col_diff = abs(col - piece.col)
        if row_diff != col_diff:
            return False

        # Check for simple move
        if row_diff == 1:
            return True

        # Check for capturing move
        if row_diff == 2:
            middle_row = (piece.row + row) // 2
            middle_col = (piece.col + col) // 2
            middle_piece = self.get_piece(middle_row, middle_col)
            if middle_piece and middle_piece.color != piece.color:
                return True

        return False

    def get_valid_moves(self, piece):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece.king:
            directions.extend([(-d[0], -d[1]) for d in directions])
        for d in directions:
            row, col = piece.row + d[0], piece.col + d[1]
            if self.valid_move(piece, row, col):
                moves.append((row, col))
            row, col = piece.row + 2 * d[0], piece.col + 2 * d[1]
            if self.valid_move(piece, row, col):
                moves.append((row, col))
        return moves

    def check_win(self):
        white_left = red_left = 0
        for row in self.board:
            for piece in row:
                if piece != 0:
                    if piece.color == WHITE:
                        white_left += 1
                    else:
                        red_left += 1
        if white_left == 0:
            return "Red wins!"
        elif red_left == 0:
            return "White wins!"
        return None


# Helper function to get row and column from mouse click
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


# Main game loop
def main():
    clock = pygame.time.Clock()
    board = Board()
    selected_piece = None
    turn = WHITE  # White goes first
    running = True

    while running:
        clock.tick(60)
        win_message = board.check_win()
        if win_message:
            print(win_message)
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)

                # Selecting a piece
                if selected_piece:
                    if board.valid_move(selected_piece, row, col):
                        if abs(selected_piece.row - row) == 2:
                            board.capture_piece(
                                selected_piece.row, selected_piece.col, row, col
                            )
                        board.move_piece(selected_piece, row, col)
                        selected_piece = None
                        turn = RED if turn == WHITE else WHITE
                    else:
                        selected_piece = None
                else:
                    piece = board.get_piece(row, col)
                    if piece != 0 and piece.color == turn:
                        if board.get_valid_moves(piece):
                            selected_piece = piece

        board.draw(WIN)
        pygame.display.update()


if __name__ == "__main__":
    main()
