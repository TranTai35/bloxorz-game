from ursina import Button, color
from ursina.models.procedural.quad import Quad

from ui.theme import (
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    PRIMARY,
    WHITE,
)
from ui.ui_sound import get_click_audio, get_hover_audio

"""
==========================================================
MENU BUTTON (dạng nút có nền - khối bo góc)

Dùng cho các nút "nặng" hơn MenuTextButton: Back, Restart,
Level Select grid, Algorithm panel,... nơi cần 1 khối nền rõ
ràng thay vì chỉ chữ trần.

VIẾT LẠI HOÀN TOÀN sau khi đọc trực tiếp source code Button
trong thư viện ursina (đã cài vào máy để đối chiếu). Bug thật
đã tìm thấy ở bản trước:

    self.text_entity.scale = 1.2

Button tự tính "self.text_entity.world_scale = 20 * text_size"
để chữ luôn hiện đúng cỡ bất kể nút to/nhỏ ra sao (world_scale
tự bù trừ theo scale của cha). Dòng trên GHI ĐÈ trực tiếp lên
local scale đã được tính sẵn đó bằng 1 con số không liên quan,
khiến chữ bị co lại nhỏ tới mức gần như bằng 0 - biến mất hoàn
toàn vào nền, dù nền vẫn hiện (chỉ là không thấy chữ).

CÁCH SỬA ĐÚNG: không tự ý set thuộc tính con (text_entity) sau
khi Button đã dựng xong. Toàn bộ thông số (màu, bo góc, cỡ chữ,
hiệu ứng hover/press) được truyền THẲNG vào constructor gốc của
Button - để chính Button tự xử lý đúng thứ tự nội bộ của nó,
thay vì mình đoán mò rồi set lại từng thuộc tính sau đó.

Hiệu ứng hover (đổi màu + phóng to nhẹ) và tiếng click/hover đều
dùng thẳng cơ chế có sẵn của Button (highlight_scale, pressed_scale,
highlight_sound, pressed_sound) - đã được ursina test kỹ, không cần
tự viết lại on_mouse_enter/on_mouse_exit/input như bản trước.
==========================================================
"""


class MenuButton(Button):

    def __init__(self, text="", **kwargs):

        options = dict(
            text=text,
            model=Quad,
            radius=.08,
            scale=(BUTTON_WIDTH, BUTTON_HEIGHT),
            color=color.rgba(25, 25, 25, 180),
            highlight_color=PRIMARY,
            pressed_color=color.rgb(35, 35, 35),
            text_color=WHITE,
            text_size=1.2,
            # Phóng to nhẹ khi hover/nhấn - Button tự áp dụng lên
            # model (khối nền), KHÔNG đụng vào text_entity nên chữ
            # luôn giữ đúng cỡ, không bị lỗi như bản trước.
            highlight_scale=1.06,
            pressed_scale=0.94,
            # Audio object dùng chung (singleton) từ ui/ui_sound.py -
            # Button tự gọi .play() khi hover/nhấn, đúng volume đã
            # định nghĩa ở ui/theme.py.
            highlight_sound=get_hover_audio(),
            pressed_sound=get_click_audio(),
        )

        # Cho phép nơi gọi override bất kỳ option nào ở trên (vd tự
        # đặt scale/position/parent riêng cho từng nút).
        options.update(kwargs)

        super().__init__(**options)