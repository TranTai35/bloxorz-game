from ursina import color, Text

"""
==========================================================
THEME

File này là nguồn màu / font / kích thước DUY NHẤT cho toàn
bộ UI của game. Không hard-code màu hay số trực tiếp trong
các file scenes/*.py hay ui/*.py khác - luôn import từ đây.

Muốn đổi "vibe" của cả game (ví dụ đổi từ cam sang xanh) thì
chỉ cần sửa ở file này.
==========================================================
"""

# ==========================================================
# FONT
# ==========================================================

# Font pixel/retro dùng cho tiêu đề lớn (giống ảnh mẫu BLOXORZ)
FONT_TITLE = "assets/fonts/PressStart2P-Regular.ttf"

# Font dùng cho danh sách menu, HUD, các đoạn text còn lại
FONT_REGULAR = "assets/fonts/Orbitron-Regular.ttf"
FONT_BOLD = "assets/fonts/Orbitron-Bold.ttf"

# Font mặc định cho toàn bộ project (Text() không truyền font riêng
# sẽ tự dùng font này)
Text.default_font = FONT_REGULAR

# ==========================================================
# COLORS
# ==========================================================

BACKGROUND = color.rgb(13, 17, 23)

PRIMARY = color.rgb(255, 159, 28)

PRIMARY_HOVER = color.rgb(255, 185, 70)

WHITE = color.rgb(245, 245, 245)

GRAY = color.rgb(170, 170, 170)

DARK_PANEL = color.rgba(10, 10, 10, 185)

TRANSPARENT = color.rgba(0, 0, 0, 0)

# ---- Glow / neon (dùng cho GlowText - xem ui/glow_text.py) ----

# Màu chữ chính (phần sắc nét ở giữa), gần trắng ngà ấm
GLOW_TEXT_COLOR = color.rgb(255, 250, 235)

# Màu quầng sáng (halo) lan toả quanh chữ - cam lửa giống ảnh mẫu
GLOW_HALO_RGB = (255, 110, 20)

# QUAN TRỌNG: rings ở đây cố tình để RẤT NHẸ (ít vòng, alpha thấp).
# GlowText vẽ (số vòng x 4 hướng) lớp chồng lên nhau - nếu để nhiều
# vòng/alpha cao, glow sẽ "đặc" lại thành 1 khối trắng và nuốt mất
# chữ (lỗi đã gặp ở bản trước). Muốn glow rực hơn, tăng dần TỪNG
# CHÚT MỘT (vd 60 -> 75) và kiểm tra lại bằng cách chạy game, đừng
# tăng nhảy vọt hay thêm nhiều vòng cùng lúc.
TITLE_GLOW_RINGS = ((0.0035, 65), (0.009, 25))

MENU_ITEM_GLOW_RINGS = ((0.003, 55),)

# ==========================================================
# TITLE
# ==========================================================

TITLE_SCALE = 2.6

SUBTITLE_SCALE = 1

# Kích thước chữ của từng dòng menu - để TO, RÕ, dễ đọc/dễ bấm
# (yêu cầu chính của bản thiết kế lại này).
MENU_ITEM_SCALE = 1.8

FOOTER_SCALE = 0.8

# ==========================================================
# BUTTON / MENU ITEM
# ==========================================================

BUTTON_WIDTH = 0.34

BUTTON_HEIGHT = 0.08

# Khoảng cách theo trục Y giữa các dòng menu, để text luôn thẳng hàng
# và không bị chồng lên nhau dù chữ đã to hơn nhiều.
MENU_ITEM_SPACING = 0.16

# Vùng bắt click (hitbox) của mỗi dòng menu - CỐ Ý to hơn chữ hiển
# thị 1 chút để dễ bấm (Fitts's law), và ĐỘC LẬP hoàn toàn với scale
# của chữ (xem ui/menu_button.py) để tránh lỗi chữ bị bóp nhỏ do
# nằm trong 1 Entity cha có scale không đều.
MENU_ITEM_HITBOX_HEIGHT = 0.13
# Bề rộng hitbox tính gần đúng theo số ký tự, xem MenuTextButton
MENU_ITEM_HITBOX_CHAR_WIDTH = 0.052
MENU_ITEM_HITBOX_MIN_WIDTH = 0.32

# Màu mũi tên chỉ hướng (▸) hiện bên trái dòng menu đang hover -
# giúp nút "nổi bật" rõ ràng thay vì chỉ đổi màu chữ.
MENU_INDICATOR_COLOR_IDLE = color.rgba(255, 110, 20, 0)
MENU_INDICATOR_COLOR_HOVER = color.rgb(255, 159, 28)

# ==========================================================
# ANIMATION
# ==========================================================

FADE_TIME = 0.35

HOVER_SCALE = 1.08

PRESS_SCALE = 0.92

HOVER_ANIM_DURATION = 0.1

PRESS_ANIM_DURATION = 0.05

RELEASE_ANIM_DURATION = 0.09

# ==========================================================
# SOUND
# ==========================================================

UI_CLICK_SOUND = "assets/sounds/ui_click.wav"
UI_HOVER_SOUND = "assets/sounds/ui_hover.wav"

UI_CLICK_VOLUME = 0.6
UI_HOVER_VOLUME = 0.35