from ursina import Entity, Text, Button, color


class AlgorithmSelectPanel(Entity):
    def __init__(
        self,
        parent,
        on_algorithm_selected,
        on_close
    ):
        super().__init__(parent=parent)

        self.on_algorithm_selected = on_algorithm_selected
        self.on_close = on_close

        self.background = Entity(
            parent=self,
            model="quad",
            color=color.rgba(0, 0, 0, 220),
            scale=(0.65, 0.7),
            z=-0.05
        )

        self.title = Text(
            parent=self,
            text="SELECT ALGORITHM",
            origin=(0, 0),
            position=(0, 0.25, -0.06),
            scale=1.7
        )

        algorithms = [
            ("BFS", "BFS"),
            ("IDS", "IDS"),
            ("UCS", "UCS"),
            ("A*", "ASTAR")
        ]

        for index, (display_name, algorithm_name) in enumerate(algorithms):
            button = Button(
                parent=self,
                text=display_name,
                position=(0, 0.12 - index * 0.12, -0.06),
                scale=(0.35, 0.085)
            )

            button.on_click = (
                lambda name=algorithm_name:
                self.select_algorithm(name)
            )

        self.close_button = Button(
            parent=self,
            text="Cancel",
            position=(0, -0.37, -0.06),
            scale=(0.25, 0.07),
            on_click=self.on_close
        )

    def select_algorithm(self, algorithm_name):
        self.on_algorithm_selected(algorithm_name)
