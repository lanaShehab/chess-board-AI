import pygame
import os
import time
import copy

# Constants
BOARD_SIZE = 600
MARGIN = 50
WIDTH = BOARD_SIZE + MARGIN
HEIGHT = BOARD_SIZE + MARGIN + 50  # Extra space for messages
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_SIZE // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (100, 100, 100)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Chessboard notation mapping
COL_MAP = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
ROW_MAP = {str(i): 8 - i for i in range(1, 9)}

# Get the directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load images
PAWN_WHITE = pygame.image.load(os.path.join(BASE_DIR, "pawn_white.png"))
PAWN_BLACK = pygame.image.load(os.path.join(BASE_DIR, "pawn_black.png"))

# Scale images
PAWN_WHITE = pygame.transform.scale(PAWN_WHITE, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
PAWN_BLACK = pygame.transform.scale(PAWN_BLACK, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Flags Game")

# Font settings
FONT_SIZE = 24
FONT = pygame.font.SysFont(None, FONT_SIZE)

# Game state
board = [
    ["", "", "", "", "", "", "", ""],
    ["W", "W", "W", "W", "W", "W", "W", "W"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["B", "B", "B", "B", "B", "B", "B", "B"],
    ["", "", "", "", "", "", "", ""],
]

running = True
message = ""
message_color = GREEN
message_time = 0
turn = "W"  # White starts first


def draw_board():
    """Draws the chessboard and axis labels."""
    for row in range(ROWS):
        for col in range(COLS):
            x = MARGIN + col * SQUARE_SIZE
            y = MARGIN + row * SQUARE_SIZE
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(WIN, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))


def draw_pawns():
    """Draws pawns on the board."""
    for row in range(ROWS):
        for col in range(COLS):
            x = MARGIN + col * SQUARE_SIZE + 5
            y = MARGIN + row * SQUARE_SIZE + 5
            if board[row][col] == "W":
                WIN.blit(PAWN_WHITE, (x, y))
            elif board[row][col] == "B":
                WIN.blit(PAWN_BLACK, (x, y))


def draw_message():
    """Displays a message on the game screen."""
    global message, message_color, message_time

    if time.time() - message_time < 2:
        text_surface = FONT.render(message, True, message_color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        WIN.blit(text_surface, text_rect)


def move_pawn(start, end):
    """Moves a pawn from start to end if valid."""
    global message, message_color, message_time, turn

    # Convert notation to board indexes
    start_x, start_y = ROW_MAP[start[0]], COL_MAP[start[1]]
    end_x, end_y = ROW_MAP[end[0]], COL_MAP[end[1]]

    if board[start_x][start_y] == "":
        message = "No pawn there! Choose another position."
        message_color = RED
        message_time = time.time()
        return False

    if board[start_x][start_y] != turn:
        message = f"Invalid! It's {turn}'s turn."
        message_color = RED
        message_time = time.time()
        return False

    if board[end_x][end_y] in ["W", "B"]:
        message = "Invalid move! Destination occupied."
        message_color = RED
        message_time = time.time()
        return False

    # Move pawn
    board[end_x][end_y] = board[start_x][start_y]
    board[start_x][start_y] = ""
    
    # Switch turn
    turn = "B" if turn == "W" else "W"

    message = f"Move {start}{end} executed!"
    message_color = GREEN
    message_time = time.time()
    return True


def get_possible_moves(color):
    """Returns all possible moves for the given color."""
    moves = []
    direction = -1 if color == "W" else 1

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == color:
                new_row = row + direction
                if 0 <= new_row < ROWS and board[new_row][col] == "":
                    moves.append(((row, col), (new_row, col)))
    return moves


def ai_move():
    """Executes AI move."""
    global turn
    possible_moves = get_possible_moves("B")
    if possible_moves:
        best_move = possible_moves[0]  # AI picks first available move
        move_pawn(best_move[0], best_move[1])
        turn = "W"


def main():
    """Main game loop."""
    global running

    while running:
        WIN.fill((0, 0, 0))
        draw_board()
        draw_pawns()
        draw_message()
        pygame.display.update()

        if turn == "W":
            move = input("Enter your move (e.g., 2h3h) or 'exit': ").strip()
            if move.lower() == "exit":
                pygame.quit()
                return
            if len(move) == 4 and move_pawn(move[:2], move[2:]):
                time.sleep(1)  # Small delay to see AI move
                ai_move()


if __name__ == "__main__":
    main()
