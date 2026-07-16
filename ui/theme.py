from ursina import color, Text

# ==========================================================
# FONT
# ==========================================================

FONT_REGULAR = "assets/fonts/Orbitron-Regular.ttf"
FONT_BOLD = "assets/fonts/Orbitron-Bold.ttf"

# Font mặc định cho toàn bộ project
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

# ==========================================================
# TITLE
# ==========================================================

TITLE_SCALE = 3.8

SUBTITLE_SCALE = 1

BUTTON_TEXT_SCALE = 1.2

FOOTER_SCALE = 0.8

# ==========================================================
# BUTTON
# ==========================================================

BUTTON_WIDTH = 0.34

BUTTON_HEIGHT = 0.08

BUTTON_SPACING = 0.12

# ==========================================================
# ANIMATION
# ==========================================================

FADE_TIME = 0.35

BUTTON_HOVER_SCALE = 1.05

BUTTON_PRESS_SCALE = 0.95