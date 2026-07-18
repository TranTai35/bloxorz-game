from pathlib import Path
import re

from ursina import Entity, Text, camera, color, destroy

from scenes.algorithm_select_panel import AlgorithmSelectPanel
from ui.menu_button import MenuTextButton
from ui.theme import (
    FONT_BOLD,
    FONT_REGULAR,
    WHITE,
)
from ui.layout import BACKGROUND_SCALE

"""
==========================================================
LEVEL SELECT SCENE

Dùng chung MenuTextButton với Main Menu (thay vì MenuButton
dựa trên Button gốc của Ursina, từng dính bug chữ bị co biến
mất do đụng vào text_entity nội bộ của Button). MenuTextButton
đã chạy ổn ở Main Menu nên tái dùng ở đây để:
  - Cùng 1 component cho toàn bộ nút trong game -> dễ bảo trì,
    sửa 1 chỗ là toàn bộ nút đều được lợi.
  - Đồng bộ giao diện (cùng font, cùng hiệu ứng hover/click).
==========================================================
"""


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

        # Nền tối đồng bộ với Main Menu, thay vì để trống/đen trơn
        self.background = Entity(
            parent=self,
            model="quad",
            texture="assets/sprites/night.jpg",
            scale=BACKGROUND_SCALE,
            double_sided=True,
        )

        self.ui_root = Entity(parent=camera.ui)

        title_text = (
            "SELECT LEVEL"
            if mode == "play"
            else "SELECT LEVEL TO SOLVE"
        )

        self.title = Text(
            parent=self.ui_root,
            text=title_text,
            font=FONT_BOLD,
            origin=(0, 0),
            y=0.42,
            scale=2,
            color=WHITE,
        )

        self.back_button = MenuTextButton(
            text="BACK",
            font=FONT_REGULAR,
            parent=self.ui_root,
            position=(-0.85, 0.44),
            text_scale=1,
            on_click=self.on_back,
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
                font=FONT_REGULAR,
                origin=(0, 0),
                y=0.1,
                color=color.red
            )
            return

        columns = 5

        # Khoảng cách giữa các ô lưới - phải LỚN HƠN hitbox_width bên
        # dưới để 2 nút cạnh nhau không chồng vùng bắt click lên nhau.
        spacing_x = 0.26
        spacing_y = 0.18

        text_scale = 1.1
        hitbox_width = 0.2

        for index, level_path in enumerate(level_files):
            row = index // columns
            col = index % columns

            x = (col - (columns - 1) / 2) * spacing_x
            y = 0.2 - row * spacing_y

            level_number = get_level_number(level_path)

            button = MenuTextButton(
                text=f"LV.{level_number}",
                font=FONT_REGULAR,
                parent=self.level_container,
                position=(x, y),
                text_scale=text_scale,
                # Căn giữa cho hợp với lưới nhiều cột, thay vì căn
                # trái như danh sách menu dọc.
                label_origin=(0, 0),
                hitbox_origin=(0, 0),
                hitbox_width=hitbox_width,
                on_click=(
                    lambda path=str(level_path):
                    self.select_level(path)
                ),
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