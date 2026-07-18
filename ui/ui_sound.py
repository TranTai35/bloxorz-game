from ursina import Audio

from ui.theme import (
    UI_CLICK_SOUND,
    UI_HOVER_SOUND,
    UI_CLICK_VOLUME,
    UI_HOVER_VOLUME,
)

"""
==========================================================
UI SOUND

Quản lý tập trung âm thanh click/hover cho toàn bộ menu, panel,
HUD,... Dùng singleton (biến module-level) để không tạo lại
Audio() mỗi lần người dùng hover qua 1 nút - vừa tốn bộ nhớ vừa
có thể gây lag nếu list dài (level select có nhiều nút).

Cách dùng trong bất kỳ file nào cần âm thanh UI:

    from ui.ui_sound import play_click, play_hover

    play_click()
    play_hover()

Lưu ý: ui_click.wav / ui_hover.wav hiện là âm thanh placeholder
được tạo tạm bằng code (sine tổng hợp). Khi có SFX click "xịn"
hơn (Freesound, tự thu, v.v.), chỉ cần thay 2 file .wav trong
assets/sounds/ cùng tên - không cần sửa code.
==========================================================
"""

_click_audio = None
_hover_audio = None


def get_click_audio():
    global _click_audio
    if _click_audio is None:
        _click_audio = Audio(
            UI_CLICK_SOUND,
            autoplay=False,
            loop=False,
            volume=UI_CLICK_VOLUME,
        )
    return _click_audio


def get_hover_audio():
    global _hover_audio
    if _hover_audio is None:
        _hover_audio = Audio(
            UI_HOVER_SOUND,
            autoplay=False,
            loop=False,
            volume=UI_HOVER_VOLUME,
        )
    return _hover_audio


def play_click():
    audio = get_click_audio()
    audio.stop()
    audio.play()


def play_hover():
    audio = get_hover_audio()
    audio.stop()
    audio.play()