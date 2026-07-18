from ursina import Entity, Text, color

"""
==========================================================
GLOW TEXT (đã đơn giản hóa)

Bản trước vẽ nhiều bản sao chữ lệch nhau quanh chữ chính để giả
lập glow ("poor man's bloom"). Cách này liên tục bị lỗi chữ bị
chồng/nhân đôi vì rất khó canh đúng khoảng lệch khi không có màn
hình để chạy thử trực tiếp - dù đã sửa 2 lần vẫn còn dấu vết.

=> Theo yêu cầu, giờ GlowText chỉ vẽ ĐÚNG 1 LỚP CHỮ DUY NHẤT.
Không còn rủi ro chồng chữ nữa, vì chỉ có 1 Text() được tạo.

"Cảm giác glow" giờ đến từ việc chọn màu sáng/ấm (main_color) cho
chữ - không phải quầng sáng thật, nhưng an toàn 100% và vẫn nổi
bật trên nền tối. Nếu sau này muốn có quầng sáng thật, cách đúng
là dùng shader/bloom post-processing của Ursina thay vì xếp chồng
Text - nhưng việc đó nằm ngoài phạm vi UI này.

API được giữ nguyên hệt như bản cũ (text, main_label, set_main_color,
set_glow_alpha_scale...) để menu_button.py và menu_scene.py KHÔNG
cần sửa gì thêm - các tham số glow_rgb/rings/directions vẫn được
nhận vào cho khỏi lỗi ở nơi gọi, nhưng không còn được dùng nữa.
==========================================================
"""


class GlowText(Entity):
    def __init__(
        self,
        text,
        font=None,
        origin=(-0.5, 0),
        main_color=color.white,
        glow_rgb=None,      # không còn dùng - giữ lại cho tương thích
        rings=None,          # không còn dùng - giữ lại cho tương thích
        directions=None,     # không còn dùng - giữ lại cho tương thích
        **kwargs
    ):
        super().__init__(**kwargs)

        self._label = text
        self._font = font
        self._origin = origin

        # Chữ duy nhất, sắc nét, không có bản sao nào khác.
        self.main_label = Text(
            parent=self,
            text=text,
            font=font,
            origin=origin,
            color=main_color,
        )

        # Giữ lại 2 danh sách rỗng này để các hàm gọi từ nơi khác
        # (vd MenuTextButton.set_glow_alpha_scale) không bị lỗi vì
        # thiếu thuộc tính - chúng chỉ đơn giản không làm gì cả.
        self._glow_labels = []
        self._glow_base_alphas = []
        self._glow_rgb = glow_rgb

    @property
    def text(self):
        return self.main_label.text

    @text.setter
    def text(self, value):
        self.main_label.text = value

    def set_main_color(self, new_color):
        self.main_label.color = new_color

    def set_glow_alpha_scale(self, factor):
        """
        Không còn lớp glow nào để chỉnh alpha (xem docstring ở đầu
        file). Hàm này được giữ lại rỗng để menu_button.py gọi vào
        lúc hover/click mà không bị lỗi thiếu hàm.
        """
        pass