from board import Board
from agent import Agent

import time
import pygame

FPS = 3
clock = pygame.time.Clock()

def main():
    pygame.init()
    board = Board()
    agent = Agent(board.square_width, board.square_high, board.fields[board.first_ground].rect.center[0], board.fields[board.first_ground].rect.center[1], board.first_ground)
    first = True

    while True:
        board.full_board_display(first)
        board.game_display.blit(agent.image_scaled, agent.rect)
        if first == True:
            pygame.display.update()
            time.sleep(2)
        first = False
        board.board_events(agent)
        board.automove_agent(agent)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()