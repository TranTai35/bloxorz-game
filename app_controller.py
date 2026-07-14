from ursina import Entity, destroy

from scenes.menu_scene import MenuScene
from scenes.level_select_scene import LevelSelectScene
from game.game import Game


class AppController(Entity):
    def __init__(self):
        super().__init__()

        self.current_screen = None

        self.show_main_menu()

    def clear_screen(self):
        if self.current_screen is not None:
            destroy(self.current_screen)
            self.current_screen = None

    def show_main_menu(self):
        self.clear_screen()

        self.current_screen = MenuScene(
            on_play=lambda: self.show_level_select("play"),
            on_solve=lambda: self.show_level_select("solve")
        )

    def show_level_select(self, mode):
        self.clear_screen()

        self.current_screen = LevelSelectScene(
            mode=mode,
            on_level_selected=self.handle_level_selected,
            on_back=self.show_main_menu
        )

    def handle_level_selected(self, level_path, mode, algorithm=None):
        if mode == "play":
            self.start_game(
                level_path=level_path,
                mode="play",
                algorithm=None
            )

        elif mode == "solve" and algorithm is not None:
            self.start_game(
                level_path=level_path,
                mode="solve",
                algorithm=algorithm
            )

    def start_game(self, level_path, mode, algorithm):
        self.clear_screen()

        self.current_screen = Game(
            level_path=level_path,
            mode=mode,
            algorithm=algorithm,
            on_back=lambda: self.show_level_select(mode)
        )