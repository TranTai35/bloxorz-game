from ursina import Entity, Text

from ui.menu_button import MenuTextButton
from ui.theme import (
    FONT_BOLD,
    FONT_REGULAR,
    WHITE,
)

"""
==========================================================
ALGORITHM SELECT PANEL

Dùng chung MenuTextButton với Main Menu / Level Select (xem
ghi chú trong scenes/level_select_scene.py) - cùng 1 component
nút cho toàn bộ game, thay vì MenuButton (dựa trên Button gốc
của Ursina) đã từng gây lỗi chữ biến mất.

LƯU Ý VỀ NỀN PANEL: bản trước dùng 1 quad màu phẳng (không có
texture) làm nền tối cho panel. Khi kiểm thử, quad-chỉ-màu-không-
texture render sai (ra trắng xoá bất kể màu gì) trong môi trường
test - một kiểu lỗi render đặc thù, KHÁC với các bug chữ đã gặp.
Main Menu (đã chạy ổn trên máy bạn) không hề dùng quad-chỉ-màu
nào cả, chỉ dùng quad CÓ texture (night.jpg). Để an toàn, nền
panel ở đây dùng lại đúng texture đó (tint tối hơn qua color),
thay vì quad-chỉ-màu chưa được kiểm chứng.
==========================================================
"""


class AlgorithmSelectPanel(Entity):
    def __init__(
        self,
        parent,
        on_algorithm_selected,
        on_close
    ):
        super().__init__(parent=parent)

        self.on_algorithm_selected = on_algorithm_selected
        self.on_close = on_close

        self.background = Entity(
            parent=self,
            model="quad",
            texture="assets/sprites/night.jpg",
            color=(0.15, 0.15, 0.18, 1),
            scale=(0.65, 0.7),
            z=-0.05
        )

        self.title = Text(
            parent=self,
            text="SELECT ALGORITHM",
            font=FONT_BOLD,
            origin=(0, 0),
            position=(0, 0.25, -0.06),
            scale=1.7,
            color=WHITE,
        )

        algorithms = [
            ("BFS", "BFS"),
            ("IDS", "IDS"),
            ("UCS", "UCS"),
            ("A*", "ASTAR")
        ]

        for index, (display_name, algorithm_name) in enumerate(algorithms):
            MenuTextButton(
                text=display_name,
                font=FONT_REGULAR,
                parent=self,
                position=(0, 0.12 - index * 0.12, -0.06),
                text_scale=1.3,
                label_origin=(0, 0),
                hitbox_origin=(0, 0),
                hitbox_width=0.3,
                on_click=(
                    lambda name=algorithm_name:
                    self.select_algorithm(name)
                ),
            )

        self.close_button = MenuTextButton(
            text="CANCEL",
            font=FONT_REGULAR,
            parent=self,
            position=(0, -0.37, -0.06),
            text_scale=0.9,
            label_origin=(0, 0),
            hitbox_origin=(0, 0),
            hitbox_width=0.35,
            on_click=self.on_close,
        )

    def select_algorithm(self, algorithm_name):
        self.on_algorithm_selected(algorithm_name)