import sys
import pygame
import numpy as np

from constants import *

#PyGame
pygame.init()

screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill( BG_COLOR )

# Tic Tac Toe Board

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))

    def mark_sqr(self, row, col, palyer):
        self.squares[row][col] = palyer

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

class Game: 

    def __init__(self):
        self.board = Board()
        self.player = 1 # Player 1 = X & Player 2 = ◯
        self.show_lines()

    def show_lines(self):

        # Virtical Lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Horizontal Lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1: # Draw X

            # Desc. Line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # Asce. Line
            start_asce = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asce = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asce, end_asce, CROSS_WIDTH)


        elif self.player == 2: # Draw ◯
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def change_player(self):
        self.player = self.player % 2 + 1

def main():

    #Game Object
    game = Game()
    board = game.board

    # Main Loop
    while True:
        game.show_lines()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col):  
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.change_player()

        
        pygame.display.update()

main()