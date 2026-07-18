from ursina import Entity, Text, camera, application, destroy

from ui.glow_text import GlowText
from ui.menu_button import MenuTextButton
from ui.animations import stagger_slide_in
from ui.rotating_cube import RotatingCube
from ui.theme import (
    FONT_TITLE,
    FONT_REGULAR,
    GLOW_TEXT_COLOR,
    GLOW_HALO_RGB,
    TITLE_GLOW_RINGS,
    TITLE_SCALE,
    MENU_ITEM_SCALE,
    MENU_ITEM_SPACING,
    GRAY,
    FOOTER_SCALE,
)
from ui.layout import (
    MENU_X,
    TITLE_Y,
    MENU_LIST_START_Y,
    FOOTER_Y,
    BACKGROUND_SCALE,
    CUBE_OFFSET_X,
    CUBE_OFFSET_Y,
)


class MenuScene(Entity):
    def __init__(self, on_play, on_solve):
        super().__init__()

        self.on_play = on_play
        self.on_solve = on_solve

        self.background = Entity(
            parent=self,
            model="quad",
            texture="assets/sprites/night.jpg",
            scale=BACKGROUND_SCALE,
            double_sided=True,
        )

        self.ui_root = Entity(parent=camera.ui)

        # ------------------------------------------------
        # Tiêu đề - chữ pixel, glow cam, căn trái tại MENU_X
        # ------------------------------------------------

        self.title = GlowText(
            text="BLOXORZ",
            font=FONT_TITLE,
            parent=self.ui_root,
            origin=(-0.5, 0),
            position=(MENU_X, TITLE_Y, -0.01),
            main_color=GLOW_TEXT_COLOR,
            glow_rgb=GLOW_HALO_RGB,
            rings=TITLE_GLOW_RINGS,
            scale=TITLE_SCALE,
        )

        # Cube xoay cạnh logo - dùng đúng texture + tỉ lệ khối đứng
        # (STANDING) trong game: scale (1, 2, 1) - cao gấp đôi rộng/sâu,
        # xem game/block_renderer.py -> get_transform(). Không phải
        # cube vuông đều, mà là khối chữ nhật giống hệt trong gameplay.
        self.logo_cube = RotatingCube(
            parent=self.ui_root,
            position=(
                MENU_X + CUBE_OFFSET_X,
                TITLE_Y + CUBE_OFFSET_Y,
                -0.02,
            ),
            scale=(0.11, 0.22, 0.11),
        )

        self.subtitle = Text(
            text="Puzzle Solver",
            parent=self.ui_root,
            font=FONT_REGULAR,
            origin=(-0.5, 0),
            position=(MENU_X, TITLE_Y - 0.09, -0.01),
            scale=1,
            color=GRAY,
        )

        # ------------------------------------------------
        # Danh sách menu - căn trái cùng trục MENU_X, tự thẳng hàng
        # ------------------------------------------------
        #
        # Chỉ cần thêm 1 dòng vào list này để có thêm mục menu mới,
        # không cần tự tính toạ độ Y bằng tay.

        menu_entries = [
            ("PLAY", self.on_play),
            ("SOLVE", self.on_solve),
            ("QUIT", application.quit),
        ]

        self.menu_buttons = []

        for index, (label, callback) in enumerate(menu_entries):
            item_y = MENU_LIST_START_Y - index * MENU_ITEM_SPACING

            button = MenuTextButton(
                text=label,
                font=FONT_REGULAR,
                position=(MENU_X, item_y),
                on_click=callback,
                text_scale=MENU_ITEM_SCALE,
                parent=self.ui_root,
            )

            self.menu_buttons.append(button)

        self.footer = Text(
            text="Foundations of AI - BFS / IDS / UCS / A*",
            parent=self.ui_root,
            font=FONT_REGULAR,
            origin=(-0.5, 0),
            position=(MENU_X, FOOTER_Y, -0.01),
            scale=FOOTER_SCALE,
            color=GRAY,
        )

        # Hiệu ứng vào menu: các dòng menu trượt lên lần lượt
        stagger_slide_in(self.menu_buttons)

    def on_destroy(self):
        destroy(self.ui_root)