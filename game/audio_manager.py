from ursina import Audio


class AudioManager:
    def __init__(self, parent=None):
        self.move_sound = Audio(
            "assets/sounds/block_land.wav",
            parent=parent,
            autoplay=False,
            volume=0.7
        )

        self.background_music = Audio(
            "assets/sounds/background_music.wav",
            parent=parent,
            autoplay=True,
            loop=True,
            volume=0.3
        )

    def play_move_sound(self):
        self.move_sound.stop()
        self.move_sound.play()

    def set_music_volume(self, volume):
        self.background_music.volume = max(0, min(volume, 1))

    def set_sfx_volume(self, volume):
        self.move_sound.volume = max(0, min(volume, 1))

    def toggle_music(self):
        if self.background_music.playing:
            self.background_music.pause()
        else:
            self.background_music.resume()
