from ursina import Button, Entity, Text, color, curve, invoke

from ui.glow_text import GlowText
from ui.theme import (
    FONT_REGULAR,
    GLOW_TEXT_COLOR,
    GLOW_HALO_RGB,
    MENU_ITEM_GLOW_RINGS,
    MENU_ITEM_HITBOX_HEIGHT,
    MENU_ITEM_HITBOX_CHAR_WIDTH,
    MENU_ITEM_HITBOX_MIN_WIDTH,
    MENU_INDICATOR_COLOR_IDLE,
    MENU_INDICATOR_COLOR_HOVER,
    HOVER_SCALE,
    PRESS_SCALE,
    HOVER_ANIM_DURATION,
    PRESS_ANIM_DURATION,
    RELEASE_ANIM_DURATION,
)
from ui.ui_sound import play_click, play_hover

"""
==========================================================
MENU TEXT BUTTON

Nút menu dạng chữ có glow (dùng cho Main Menu, Level Select,
Algorithm Panel...). Không có nền hình khối - giống danh sách
"PLAY / SOLVE / ..." trong ảnh mẫu, nhưng chữ TO và có mũi tên
chỉ hướng khi hover để rõ ràng, dễ bấm.

KIẾN TRÚC (quan trọng, đọc trước khi sửa):

    MenuTextButton (Entity, scale luôn = 1, KHÔNG bao giờ đổi)
        ├── self.label    -> GlowText, tự set scale riêng
        └── self._hitbox  -> Button vô hình, tự set scale riêng

    self.label và self._hitbox là 2 ANH EM (cùng cha là
    MenuTextButton), KHÔNG phải cha-con của nhau. Nhờ vậy scale
    của đứa này không nhân dồn vào đứa kia.

    Bản trước đây từng để self.label làm CON của self._hitbox (một
    Button có scale=(0.5, 0.09) rất dẹt để làm vùng bắt click) - Ursina
    nhân scale cha vào con, nên chữ bị bóp gần như biến mất, hiện ra
    như 1 gạch ngang nhỏ xíu. Đây chính là lỗi trong ảnh bạn gửi.
    KHÔNG được lặp lại kiểu lồng này ở bất kỳ nút mới nào.
==========================================================
"""


class _MenuHitbox(Button):
    """
    Vùng bắt hover/click, trong suốt (không có hình). Chỉ chịu
    trách nhiệm phát hiện input, không tự vẽ gì cả - việc hiển thị
    hoàn toàn do MenuTextButton.label (GlowText) đảm nhiệm.
    """

    def __init__(self, owner, **kwargs):
        super().__init__(
            text="",
            model="quad",
            color=color.clear,
            highlight_color=color.clear,
            pressed_color=color.clear,
            **kwargs,
        )
        self.owner = owner

    def on_mouse_enter(self):
        self.owner._on_hover_enter()

    def on_mouse_exit(self):
        self.owner._on_hover_exit()

    def input(self, key):
        if self.hovered and key == "left mouse down":
            self.owner._on_press_down()

        if self.hovered and key == "left mouse up":
            self.owner._on_press_up()


class MenuTextButton(Entity):
    def __init__(
        self,
        text,
        position=(0, 0),
        font=None,
        on_click=None,
        text_scale=1.8,
        main_color=None,
        glow_rgb=None,
        glow_rings=None,
        parent=None,
    ):
        # Entity cha này luôn giữ scale mặc định (1, 1, 1) - KHÔNG
        # setattr scale ở đây, để label/hitbox bên dưới không bị ảnh
        # hưởng. Chỉ vị trí (position) mới được đặt ở cấp này.
        super().__init__(parent=parent, position=position)

        self.callback = on_click
        self.text_scale = text_scale
        self._is_pressed = False

        # Mũi tên chỉ hướng, ẩn (alpha 0) lúc bình thường, sáng lên
        # khi hover - dấu hiệu "đang chọn" rõ ràng, không phụ thuộc
        # vào việc glow có hiển thị đẹp hay không.
        self.indicator = Text(
            text=">",
            parent=self,
            font=font or FONT_REGULAR,
            origin=(-0.5, 0),
            position=(-0.09, 0, -0.02),
            scale=text_scale,
            color=MENU_INDICATOR_COLOR_IDLE,
        )

        self.label = GlowText(
            text=text,
            font=font or FONT_REGULAR,
            parent=self,
            origin=(-0.5, 0),
            main_color=main_color or GLOW_TEXT_COLOR,
            glow_rgb=glow_rgb or GLOW_HALO_RGB,
            rings=glow_rings or MENU_ITEM_GLOW_RINGS,
            scale=text_scale,
            position=(0, 0, -0.01),
        )

        # Bề rộng hitbox ước lượng theo số ký tự - đủ rộng để dễ bấm,
        # không phụ thuộc vào scale thật sự của label (tránh đúng cái
        # bug đã nói ở trên).
        hitbox_width = max(
            MENU_ITEM_HITBOX_MIN_WIDTH,
            len(text) * MENU_ITEM_HITBOX_CHAR_WIDTH * text_scale,
        )

        self._hitbox = _MenuHitbox(
            owner=self,
            parent=self,
            origin=(-0.5, 0),
            scale=(hitbox_width, MENU_ITEM_HITBOX_HEIGHT * text_scale),
            position=(-0.02, 0, 0.01),
        )

    # ==================================================
    # Hover / click - gọi từ _MenuHitbox, tác động lên self.label
    # ==================================================

    def _on_hover_enter(self):
        self.label.animate_scale(
            self.text_scale * HOVER_SCALE,
            duration=HOVER_ANIM_DURATION,
            curve=curve.out_quad,
        )
        self.label.set_glow_alpha_scale(1.6)
        self.indicator.animate_color(
            MENU_INDICATOR_COLOR_HOVER,
            duration=HOVER_ANIM_DURATION,
        )
        play_hover()

    def _on_hover_exit(self):
        if self._is_pressed:
            return

        self.label.animate_scale(
            self.text_scale,
            duration=HOVER_ANIM_DURATION,
            curve=curve.out_quad,
        )
        self.label.set_glow_alpha_scale(1.0)
        self.indicator.animate_color(
            MENU_INDICATOR_COLOR_IDLE,
            duration=HOVER_ANIM_DURATION,
        )

    def _on_press_down(self):
        self._is_pressed = True

        self.label.animate_scale(
            self.text_scale * PRESS_SCALE,
            duration=PRESS_ANIM_DURATION,
        )

    def _on_press_up(self):
        self._is_pressed = False

        self.label.animate_scale(
            self.text_scale * HOVER_SCALE,
            duration=RELEASE_ANIM_DURATION,
            curve=curve.out_back,
        )

        play_click()

        if self.callback:
            invoke(self.callback, delay=RELEASE_ANIM_DURATION)
