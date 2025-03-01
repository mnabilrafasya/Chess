import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Ukuran layar
WIDTH = 650
HEIGHT = 480
SQ_SIZE = 60

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CATUR NABIL")

# Load gambar buah catur
pieces = {}
colors = ['w', 'b']
for color in colors:
    for piece in ['R', 'N', 'B', 'Q', 'K', 'P']:
        pieces[color + piece] = pygame.transform.scale(
            pygame.image.load(f'img/{color}{piece}.png'), (SQ_SIZE, SQ_SIZE))

# Papan catur awal
board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP']*8,
    ['']*8,
    ['']*8,
    ['']*8,
    ['']*8,
    ['wP']*8,
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

# Variabel game
selected = None
turn = 'w'
move_log = []

def draw_board():
    for row in range(8):
        for col in range(8):
            color = GREEN if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(screen, color, (col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                screen.blit(pieces[piece], (col*SQ_SIZE, row*SQ_SIZE))

def get_valid_moves(row, col):
    valid_moves = []
    piece = board[row][col]
    if not piece:
        return []
    
    color = piece[0]
    type_piece = piece[1]

    # Gerakan Pion
    if type_piece == 'P':
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        
        # Gerakan maju 1 langkah
        if 0 <= row + direction < 8 and not board[row + direction][col]:
            valid_moves.append((row + direction, col))
            
            # Gerakan awal 2 langkah
            if row == start_row and not board[row + 2*direction][col]:
                valid_moves.append((row + 2*direction, col))
        
        # Makan diagonal
        for dc in [-1, 1]:
            if 0 <= col + dc < 8 and 0 <= row + direction < 8:
                target = board[row + direction][col + dc]
                if target and target[0] != color:
                    valid_moves.append((row + direction, col + dc))

    # Gerakan Kuda
    elif type_piece == 'N':
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                 (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in moves:
            if 0 <= row + dr < 8 and 0 <= col + dc < 8:
                target = board[row + dr][col + dc]
                if not target or target[0] != color:
                    valid_moves.append((row + dr, col + dc))

    # Gerakan Gajah
    elif type_piece == 'B':
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if not target:
                    valid_moves.append((r, c))
                elif target[0] != color:
                    valid_moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    # Gerakan Benteng
    elif type_piece == 'R':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if not target:
                    valid_moves.append((r, c))
                elif target[0] != color:
                    valid_moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    # Gerakan Menteri
    elif type_piece == 'Q':
        # Kombinasi gerakan benteng dan gajah
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1),
                      (-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if not target:
                    valid_moves.append((r, c))
                elif target[0] != color:
                    valid_moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    # Gerakan Raja
    elif type_piece == 'K':
        moves = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),          (0, 1),
                 (1, -1),  (1, 0), (1, 1)]
        for dr, dc in moves:
            if 0 <= row + dr < 8 and 0 <= col + dc < 8:
                target = board[row + dr][col + dc]
                if not target or target[0] != color:
                    valid_moves.append((row + dr, col + dc))

    return valid_moves

def draw_highlights(valid_moves):
    if selected:
        row, col = selected
        pygame.draw.rect(screen, BLUE, (col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)
    for move in valid_moves:
        pygame.draw.rect(screen, RED, (move[1]*SQ_SIZE, move[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)

def handle_move(start_row, start_col, end_row, end_col):
    global turn
    piece = board[start_row][start_col]
    
    # Handle promosi pion
    if piece[1] == 'P':
        if (piece[0] == 'w' and end_row == 0) or (piece[0] == 'b' and end_row == 7):
            piece = piece[0] + 'Q'
    
    board[end_row][end_col] = piece
    board[start_row][start_col] = ''
    move_log.append(((start_row, start_col), (end_row, end_col)))
    turn = 'b' if turn == 'w' else 'w'

def show_game_info():
    font = pygame.font.SysFont('arial', 20)
    text = font.render(f"Giliran: {'Putih' if turn == 'w' else 'Hitam'}", True, BLACK)
    screen.blit(text, (WIDTH - 150, 10))
    
    y = 50
    for i, move in enumerate(move_log[-5:]):
        text = font.render(f"{i+1}. {chr(move[0][1]+65)}{8-move[0][0]}->{chr(move[1][1]+65)}{8-move[1][0]}", True, BLACK)
        screen.blit(text, (WIDTH - 150, y))
        y += 30

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // SQ_SIZE
            row = y // SQ_SIZE
            
            if 0 <= row < 8 and 0 <= col < 8:
                if selected is None:
                    if board[row][col] and board[row][col][0] == turn:
                        selected = (row, col)
                        valid_moves = get_valid_moves(row, col)
                else:
                    if (row, col) in valid_moves:
                        handle_move(selected[0], selected[1], row, col)
                        selected = None
                        valid_moves = []
                    else:
                        selected = None
                        valid_moves = []
    
    screen.fill(WHITE)
    draw_board()
    
    if selected:
        draw_highlights(valid_moves)
    
    draw_pieces()
    show_game_info()
    
    pygame.display.flip()

pygame.quit()
sys.exit()