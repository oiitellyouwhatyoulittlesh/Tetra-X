"""
Tetra-X

File:
    screen.py

Purpose:
    Provides the base screen class and screen manager.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graphics.renderer import Renderer
    from settings import Settings


class Screen:
    """
    Base class for all Tetra-X screens.
    """

    def __init__(
        self,
        settings: "Settings"
    ) -> None:

        self.settings = settings


    def handle_events(
        self,
        events
    ) -> None:
        """
        Handles input events.
        """


    def update(
        self,
        delta_time: float
    ) -> None:
        """
        Updates the screen.
        """


    def draw(
        self,
        renderer: "Renderer"
    ) -> None:
        """
        Draws the screen.
        """


class ScreenManager:
    """
    Controls the currently active screen.
    """

    def __init__(
        self,
        renderer: "Renderer",
        settings: "Settings"
    ) -> None:

        self.renderer = renderer
        self.settings = settings

        self.current_screen: Screen | None = None


    # ====================
    # Screen Control
    # ====================

    def set_screen(
        self,
        screen: Screen
    ) -> None:
        """
        Changes the active screen.
        """

        self.current_screen = screen


    # ====================
    # Update
    # ====================

    def handle_events(
        self,
        events
    ) -> None:
        """
        Passes events to the active screen.
        """

        if self.current_screen is None:
            return

        self.current_screen.handle_events(
            events
        )


    def update(
        self,
        delta_time: float
    ) -> None:
        """
        Updates the active screen.
        """

        if self.current_screen is None:
            return

        self.current_screen.update(
            delta_time
        )


    # ====================
    # Drawing
    # ====================

    def draw(self) -> None:
        """
        Draws the active screen.
        """

        if self.current_screen is None:
            return

        self.current_screen.draw(
            self.renderer
        )
