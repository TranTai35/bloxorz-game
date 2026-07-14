from ursina import Entity, load_texture


class Renderer:
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.tiles = []

        self.floor_texture = load_texture(
            "assets/texture/floor.jpg"
        )

        self.goal_texture = load_texture(
            "assets/texture/goal.jpg"
        )

    def grid_to_world(self, row, col):
        x = col
        z = -row
        return x, z

    def create_map(self):
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                if self.board.is_void(row, col):
                    continue

                x, z = self.grid_to_world(row, col)

                if self.board.is_goal(row, col):
                    selected_texture = self.goal_texture
                else:
                    selected_texture = self.floor_texture

                tile = Entity(
                    parent=self.parent,
                    model="cube",
                    texture=selected_texture,
                    position=(x, 0, z),
                    scale=(1, 0.2, 1)
                )

                self.tiles.append(tile)