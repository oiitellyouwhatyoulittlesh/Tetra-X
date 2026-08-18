"""
Tetra-X

File:
    main.py

Purpose:
    Starts the game and runs the main loop.
"""

import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)

import pygame

from constants import FPS
from graphics.renderer import Renderer
from screens.main_menu import MainMenu
from screens.screen import ScreenManager
from settings import Settings


def main() -> None:
    """
    Runs the game.
    """

    settings = Settings()

    renderer = Renderer()

    screen_manager = ScreenManager(
        renderer,
        settings
    )

    screen_manager.set_screen(
        MainMenu(
            screen_manager,
            settings
        )
    )

    clock = pygame.time.Clock()

    running = True

    while running:

        delta_time = (
            clock.tick(FPS) / 1000
        )

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:

                running = False

        screen_manager.handle_events(
            events
        )

        screen_manager.update(
            delta_time
        )

        renderer.clear()

        screen_manager.draw()

        renderer.update()

    pygame.quit()


if __name__ == "__main__":

    main()
