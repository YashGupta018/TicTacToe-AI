import sys
import pygame

from constants import *

#PyGame
pygame.init()

screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(( 28, 170, 156 ))

def main():

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()

main()