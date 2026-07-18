from ursina import Button, color, curve

from ui.theme import (
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    PRIMARY,
    WHITE,
    HOVER_SCALE,
    PRESS_SCALE,
    HOVER_ANIM_DURATION,
    PRESS_ANIM_DURATION,
)
from ui.ui_sound import play_click, play_hover

"""
==========================================================
MENU BUTTON (dạng nút có nền - khối bo góc)

Dùng cho các nút "nặng" hơn MenuTextButton: Back, Restart,
Level Select grid, Algorithm panel,... nơi cần 1 khối nền rõ
ràng thay vì chỉ chữ trần.

Cũng có animation hover/press + tiếng click/hover giống
MenuTextButton để đồng bộ cảm giác trên toàn bộ game.
==========================================================
"""


class MenuButton(Button):

    def __init__(self, text="", **kwargs):

        super().__init__()

        self.text = text

        self.scale = (BUTTON_WIDTH, BUTTON_HEIGHT)

        self.color = color.rgba(25, 25, 25, 180)

        self.highlight_color = PRIMARY

        self.pressed_color = color.rgb(35, 35, 35)

        self.text_color = WHITE

        self.text_entity.scale = 1.2

        self.text_entity.color = WHITE

        self.model = "quad"

        self.radius = .08

        # scale gốc lưu lại để animate hover/press dựa trên đúng
        # kích thước ban đầu, tránh cộng dồn scale qua nhiều lần
        self.base_scale = self.scale

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.base_scale = self.scale

    def on_mouse_enter(self):

        self.animate_scale(
            (
                self.base_scale[0] * HOVER_SCALE,
                self.base_scale[1] * HOVER_SCALE,
            ),
            duration=HOVER_ANIM_DURATION,
            curve=curve.out_quad,
        )

        self.text_entity.color = PRIMARY

        play_hover()

    def on_mouse_exit(self):

        self.animate_scale(
            self.base_scale,
            duration=HOVER_ANIM_DURATION,
            curve=curve.out_quad,
        )

        self.text_entity.color = WHITE

    def input(self, key):
        # Lưu ý: Button.on_click trong Ursina là 1 thuộc tính do người
        # gọi gán trực tiếp (vd: MenuButton(on_click=self.foo)), nên
        # không thể override bằng cách định nghĩa method on_click() ở
        # đây - nó sẽ bị đè mất. Thay vào đó ta chèn tiếng click + hiệu
        # ứng bóp nhỏ ngay tại input(), rồi gọi super().input(key) để
        # Ursina vẫn tự xử lý việc gọi self.on_click như bình thường.
        if self.hovered and key == "left mouse down":
            self.animate_scale(
                (
                    self.base_scale[0] * PRESS_SCALE,
                    self.base_scale[1] * PRESS_SCALE,
                ),
                duration=PRESS_ANIM_DURATION,
            )

        if self.hovered and key == "left mouse up":
            self.animate_scale(
                (
                    self.base_scale[0] * HOVER_SCALE,
                    self.base_scale[1] * HOVER_SCALE,
                ),
                duration=HOVER_ANIM_DURATION,
                curve=curve.out_quad,
            )
            play_click()

        super().input(key)
