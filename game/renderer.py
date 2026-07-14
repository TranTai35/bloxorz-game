from ursina import Entity, color


class Renderer:
    def __init__(self, board):
        self.board = board
        self.tile_entities = []

        self.tile_height = 0.2
        self.floor_y = 0

    def grid_to_world(self, row, col):
        """
        Chuyển tọa độ ma trận (row, col)
        thành tọa độ Ursina (x, y, z).
        """
        x = col
        z = -row

        return x, z

    def create_map(self):
        """
        Tạo các ô sàn dựa trên board.grid.
        """

        for row in range(self.board.rows):
            for col in range(self.board.cols):

                if self.board.is_void(row, col):
                    continue

                x, z = self.grid_to_world(row, col)

                if self.board.is_goal(row, col):
                    tile_texture = "assets/texture/goal.jpg"
                else:
                    tile_texture = "assets/texture/floor.jpg"

                tile = Entity(
                    model="cube",
                    texture=tile_texture,
                    color=color.white,
                    position=(x, self.floor_y, z),
                    scale=(1, self.tile_height, 1)
                )

                self.tile_entities.append(tile)