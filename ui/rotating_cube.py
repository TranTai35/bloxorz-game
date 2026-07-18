from ursina import Entity, time

"""
==========================================================
ROTATING CUBE

Cục cube 3D xoay vòng vòng trang trí cạnh logo ở Main Menu -
dùng ĐÚNG texture khối người chơi trong game (assets/texture/
block.jpg, xem game/block_renderer.py) để đồng bộ hình ảnh
giữa menu và gameplay, thay vì dùng 1 khối trơn không liên quan.

Đặt trong camera.ui (giống toàn bộ UI khác của menu) nên không
cần lo về camera/góc nhìn thế giới 3D - cube tự xoay quanh trục
của chính nó bằng update(), Ursina tự gọi hàm này mỗi frame.
==========================================================
"""

BLOCK_TEXTURE_PATH = "assets/texture/block.jpg"


class RotatingCube(Entity):
    def __init__(
        self,
        spin_speed_y=45,
        spin_speed_x=12,
        **kwargs
    ):
        super().__init__(
            model="cube",
            texture=BLOCK_TEXTURE_PATH,
            # Góc nghiêng ban đầu để thấy được nhiều mặt cube ngay
            # từ đầu (giống góc nhìn isometric trong ảnh mẫu), thay
            # vì nhìn thẳng vào 1 mặt lúc mới xuất hiện.
            rotation=(20, -30, 0),
            **kwargs
        )

        self.spin_speed_y = spin_speed_y
        self.spin_speed_x = spin_speed_x

    def update(self):
        self.rotation_y += self.spin_speed_y * time.dt
        self.rotation_x += self.spin_speed_x * time.dt