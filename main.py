# ---------
# CONSTANTS
# ---------

WIDTH = 600 # Screen Size
HEIGHT = 600 # Screen Size

ROWS = 3 # Board Verticle Line
COLS = 3 # Board Verticle Line
SQSIZE = WIDTH // COLS

LINE_WIDTH = 15 # Line Size
CIRC_WIDTH = 15 # Circle Size (Player 2)
CROSS_WIDTH = 20 # Cross Size (Player 1)

RADIUS = SQSIZE // 4 # Circle Size (Player 2)

OFFSET = 50

# Colors

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRC_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# ----------------------------------------------------------------------- #

import copy
import sys
import pygame
import random
import numpy as np

# PyGame
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TicTacToe AI')
screen.fill( BG_COLOR )

# Classes
class Board:
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares # Squares
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # Vertical Wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # Horizontal Wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # Desc Diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # Asce Diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # No Win Yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # Random
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # row, col

    # Minimax Algorithm
    def minimax(self, board, maximizing):
        
        # Terminal Cases
        case = board.final_state()

        # Player 1 Wins
        if case == 1:
            return 1, None # eval, move

        # Player 2 Wins
        if case == 2:
            return -1, None

        # Draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # Main Eval
    def eval(self, main_board):
        if self.level == 0:
            # Random Choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # Minimax Algorithm Choice
            eval, move = self.minimax(main_board, False)

        print(f'AI marked the square in pos {move} with an eval of: {eval}')
        return move # row, col

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   # Player 1 - X (Cross)  # Player 2 - ○ (Circles)
        self.gamemode = 'ai' # Pvp or Ai
        self.running = True
        self.show_lines()

    # TicTacToe Board
    def show_lines(self):
        # Background
        screen.fill( BG_COLOR )

        # Vertical Lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # Player 1 - X (Cross)
            # Desc Line ( ╲ )
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # Asce line ( ╱ )
            start_asce = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asce = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asce, end_asce, CROSS_WIDTH)

            # Desc Line ( ╲ ) + Asce Line ( ╱ ) = Ace line ( ╳ )
        
        elif self.player == 2:
            # Player 2 - ○ (Circle)
            # Draw Circle ( ○ )
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # Other Methods

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():

    # Game Objects

    game = Game()
    board = game.board
    ai = game.ai

    # Main Loop

    while True:
        
        # PyGame Events
        for event in pygame.event.get():

            # Quit Event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keydown(Pressed) Events
            if event.type == pygame.KEYDOWN:

                # Game Mode (Press G)
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # Restart (Press R)
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # Random AI (Press 0)
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # Pro AI (Press 1)
                if event.key == pygame.K_1:
                    ai.level = 1

            # Click Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                # Human Marked Squares
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False


        # AI Initial Call
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # Update Screen
            pygame.display.update()

            # Eval
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
            
        pygame.display.update()

main()
