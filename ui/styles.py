from ursina import Button, color

from ui.theme import *


class MenuButton(Button):

    def __init__(self, text="", **kwargs):

        super().__init__()

        self.text = text

        self.scale = (BUTTON_WIDTH, BUTTON_HEIGHT)

        self.color = color.rgba(25, 25, 25, 180)

        self.highlight_color = PRIMARY

        self.pressed_color = color.rgb(35, 35, 35)

        self.text_color = WHITE

        self.text_entity.scale = BUTTON_TEXT_SCALE

        self.text_entity.color = WHITE

        self.model = "quad"

        self.radius = .08

        for key, value in kwargs.items():
            setattr(self, key, value)

    def on_mouse_enter(self):

        self.animate_scale(
            (BUTTON_WIDTH * BUTTON_HOVER_SCALE,
             BUTTON_HEIGHT * BUTTON_HOVER_SCALE),
            duration=.12
        )

        self.text_entity.color = PRIMARY

    def on_mouse_exit(self):

        self.animate_scale(
            (BUTTON_WIDTH, BUTTON_HEIGHT),
            duration=.12
        )

        self.text_entity.color = WHITE