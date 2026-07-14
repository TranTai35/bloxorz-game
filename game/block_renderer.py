from ursina import Entity, color, invoke, destroy, Vec3, scene, curve
from block import Orientation


class BlockRenderer:
    def __init__(self, block_logic):
        self.block_logic = block_logic

        self.entity = Entity(
            model="cube",
            texture="assets/texture/block.jpg",
            color=color.white
        )

        self.update_transform()

    def grid_to_world(self, row, col):
        x = col
        z = -row
        return x, z

    def get_transform(self, block):
        if block.orientation == Orientation.STANDING:
            row, col = block.pos1
            x, z = self.grid_to_world(row, col)

            position = Vec3(x, 1.1, z)
            scale = Vec3(1, 2, 1)

        elif block.orientation == Orientation.HORIZONTAL:
            row1, col1 = block.pos1
            row2, col2 = block.pos2

            center_col = (col1 + col2) / 2
            x, z = self.grid_to_world(row1, center_col)

            position = Vec3(x, 0.6, z)
            scale = Vec3(2, 1, 1)

        elif block.orientation == Orientation.VERTICAL:
            row1, col1 = block.pos1
            row2, col2 = block.pos2

            center_row = (row1 + row2) / 2
            x, z = self.grid_to_world(center_row, col1)

            position = Vec3(x, 0.6, z)
            scale = Vec3(1, 1, 2)

        else:
            raise ValueError("Orientation không hợp lệ")

        return position, scale

    def update_transform(self):
        position, scale = self.get_transform(self.block_logic)

        self.entity.position = position
        self.entity.scale = scale
        self.entity.rotation = (0, 0, 0)

    def get_pivot_data(self, block, direction):
        position, scale = self.get_transform(block)

        half_x = scale.x / 2
        half_y = scale.y / 2
        half_z = scale.z / 2

        if direction == "UP":
            pivot_position = Vec3(
                position.x,
                position.y - half_y,
                position.z + half_z
            )
            axis = "x"
            angle = 90

        elif direction == "DOWN":
            pivot_position = Vec3(
                position.x,
                position.y - half_y,
                position.z - half_z
            )
            axis = "x"
            angle = -90

        elif direction == "LEFT":
            pivot_position = Vec3(
                position.x - half_x,
                position.y - half_y,
                position.z
            )
            axis = "z"
            angle = -90

        elif direction == "RIGHT":
            pivot_position = Vec3(
                position.x + half_x,
                position.y - half_y,
                position.z
            )
            axis = "z"
            angle = 90

        else:
            raise ValueError(f"Hướng không hợp lệ: {direction}")

        return pivot_position, axis, angle

    def animate_move(
        self,
        old_block,
        new_block,
        direction,
        on_complete
    ):
        duration = 0.25

        pivot_position, axis, angle = self.get_pivot_data(
            old_block,
            direction
        )

        pivot = Entity(
            parent=scene,
            position=pivot_position
        )

        # Đổi parent nhưng giữ nguyên vị trí thế giới
        self.entity.world_parent = pivot

        if axis == "x":
            pivot.animate_rotation_x(
                angle,
                duration=duration,
                curve=curve.linear
            )

        elif axis == "z":
            pivot.animate_rotation_z(
                angle,
                duration=duration,
                curve=curve.linear
            )

        invoke(
            self.finish_animation,
            pivot,
            new_block,
            on_complete,
            delay=duration
        )

    def finish_animation(
        self,
        pivot,
        new_block,
        on_complete
    ):
        # Đưa block trở về scene và giữ world transform
        self.entity.world_parent = scene

        destroy(pivot)

        # Gán trạng thái logic mới
        self.block_logic = new_block

        # Ép về transform chính xác để tránh sai số animation
        self.update_transform()

        on_complete()