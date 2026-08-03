"""
Tetra-X

File:
    main.py

Purpose:
    Starts the game and runs the main loop.

"""

import pygame

import sys
import os


sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)


from constants import FPS

from game.game import Game
from graphics.renderer import Renderer



def main() -> None:
    """
    Runs the game.
    """

    game = Game()

    renderer = Renderer()

    clock = pygame.time.Clock()


    game.start()


    running = True


    while running:

        delta_time = (
            clock.tick(FPS) / 1000
        )


        events = pygame.event.get()


        for event in events:

            if event.type == pygame.QUIT:

                running = False


        game.update(
            delta_time,
            events
        )


        renderer.clear()

        renderer.draw_board(
            game.get_board()
        )

        renderer.update()



    pygame.quit()



if __name__ == "__main__":

    main()
