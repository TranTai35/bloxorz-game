from pathlib import Path
import re

from ursina import (
    Entity,
    Text,
    Button,
    camera,
    color,
    destroy
)

from scenes.algorithm_select_panel import AlgorithmSelectPanel


def get_level_number(path):
    match = re.search(r"\d+", path.stem)

    if match:
        return int(match.group())

    return 999999


class LevelSelectScene(Entity):
    def __init__(self, mode, on_level_selected, on_back):
        super().__init__()

        self.mode = mode
        self.on_level_selected = on_level_selected
        self.on_back = on_back

        self.selected_level_path = None

        self.ui_root = Entity(parent=camera.ui)

        title_text = (
            "SELECT LEVEL"
            if mode == "play"
            else "SELECT LEVEL TO SOLVE"
        )

        self.title = Text(
            parent=self.ui_root,
            text=title_text,
            origin=(0, 0),
            y=0.4,
            scale=2
        )

        self.back_button = Button(
            parent=self.ui_root,
            text="Back",
            position=(-0.78, 0.43),
            scale=(0.16, 0.07),
            on_click=self.on_back
        )

        self.level_container = Entity(
            parent=self.ui_root
        )

        self.algorithm_panel = None

        self.create_level_buttons()

    def get_level_files(self):
        level_files = list(Path("maps").glob("*.json"))

        level_files.sort(
            key=get_level_number
        )

        return level_files

    def create_level_buttons(self):
        level_files = self.get_level_files()

        if not level_files:
            Text(
                parent=self.level_container,
                text="Không tìm thấy level trong thư mục maps",
                origin=(0, 0),
                y=0.1,
                color=color.red
            )
            return

        columns = 5
        button_width = 0.18
        button_height = 0.1

        spacing_x = 0.22
        spacing_y = 0.14

        for index, level_path in enumerate(level_files):
            row = index // columns
            col = index % columns

            x = (col - (columns - 1) / 2) * spacing_x
            y = 0.25 - row * spacing_y

            level_number = get_level_number(level_path)

            button = Button(
                parent=self.level_container,
                text=f"Level {level_number}",
                position=(x, y),
                scale=(button_width, button_height)
            )

            button.on_click = (
                lambda path=str(level_path):
                self.select_level(path)
            )

    def select_level(self, level_path):
        if self.mode == "play":
            self.on_level_selected(
                level_path,
                "play",
                None
            )

        elif self.mode == "solve":
            self.open_algorithm_panel(level_path)

    def open_algorithm_panel(self, level_path):
        self.selected_level_path = level_path

        if self.algorithm_panel is not None:
            destroy(self.algorithm_panel)

        self.algorithm_panel = AlgorithmSelectPanel(
            parent=self.ui_root,
            on_algorithm_selected=self.select_algorithm,
            on_close=self.close_algorithm_panel
        )

    def select_algorithm(self, algorithm):
        if self.selected_level_path is None:
            return

        level_path = self.selected_level_path

        self.close_algorithm_panel()

        self.on_level_selected(
            level_path,
            "solve",
            algorithm
        )

    def close_algorithm_panel(self):
        if self.algorithm_panel is not None:
            destroy(self.algorithm_panel)
            self.algorithm_panel = None

    def on_destroy(self):
        if hasattr(self, "algorithm_panel"):
            if self.algorithm_panel is not None:
                destroy(self.algorithm_panel)
                self.algorithm_panel = None

        if hasattr(self, "ui_root"):
            destroy(self.ui_root)