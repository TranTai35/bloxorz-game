from ursina import Entity, Text, Button, camera, color


class MenuScene(Entity):
    def __init__(self, on_play, on_solve):
        super().__init__()

        self.on_play = on_play
        self.on_solve = on_solve

        self.background = Entity(
            parent=self,
            model="quad",
            texture="assets/sprites/background.png",
            scale=50,
            double_sided=True
        )

        self.ui_root = Entity(parent=camera.ui)

        self.panel = Entity(
            parent=self.ui_root,
            model="quad",
            color=color.rgba(0, 0, 0, 180),
            scale=(0.65, 0.75)
        )

        self.title = Text(
            parent=self.panel,
            text="BLOXORZ",
            origin=(0, 0),
            position=(0, 0.27, -0.01),
            scale=3
        )

        self.subtitle = Text(
            parent=self.panel,
            text="Puzzle Solver",
            origin=(0, 0),
            position=(0, 0.17, -0.01),
            scale=1.2,
            color=color.light_gray
        )

        self.play_button = Button(
            parent=self.panel,
            text="PLAY",
            position=(0, 0.02, -0.01),
            scale=(0.4, 0.12),
            on_click=self.on_play
        )

        self.solve_button = Button(
            parent=self.panel,
            text="SOLVE",
            position=(0, -0.14, -0.01),
            scale=(0.4, 0.12),
            on_click=self.on_solve
        )

    def on_destroy(self):
        from ursina import destroy
        destroy(self.ui_root)