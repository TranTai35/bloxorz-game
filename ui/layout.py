"""
==========================================================
UI LAYOUT

Toàn bộ vị trí của Menu Scene được quản lý tại đây.

Không hard-code position trong menu_scene.py nữa - mọi toạ độ
X/Y nên lấy từ file này để khi cần chỉnh layout, chỉ sửa 1 chỗ.

Thiết kế theo ảnh mẫu: chữ căn trái, tiêu đề + danh sách menu
thẳng hàng theo trục X, không có khung/panel nền.
==========================================================
"""

# ==========================================================
# TRỤC X CHUNG
# ==========================================================

# Toàn bộ tiêu đề + danh sách menu dùng chung 1 trục X để luôn
# thẳng hàng (origin của text là (-0.5, 0) - tức mép trái của
# chữ nằm đúng tại toạ độ này).
MENU_X = -0.75

# ==========================================================
# LOGO / TIÊU ĐỀ
# ==========================================================

TITLE_Y = 0.32

# Cube xoay đặt cạnh logo (làm sau - xem ui/rotating_cube.py khi có)
CUBE_OFFSET_X = 0.30
CUBE_OFFSET_Y = 0.0

# ==========================================================
# DANH SÁCH MENU
# ==========================================================

# Vị trí Y của dòng menu đầu tiên, các dòng sau tự trừ dần theo
# MENU_ITEM_SPACING (xem ui/theme.py) - không cần khai báo tay
# từng dòng như trước.
MENU_LIST_START_Y = 0.08

# ==========================================================
# FOOTER
# ==========================================================

FOOTER_Y = -0.45

# ==========================================================
# BACKGROUND
# ==========================================================

BACKGROUND_SCALE = 50
