from ursina import (
    Entity,
    invoke,
    destroy,
    Vec3,
    curve,
    load_texture
)
from block import Orientation


class BlockRenderer:
    def __init__(self, block_logic, parent):
        self.block_logic = block_logic
        self.parent = parent

        block_texture = load_texture(
            "assets/texture/block.jpg"
        )

        print("Block texture:", block_texture)

        self.entity = Entity(
            parent=self.parent,
            model="cube",
            texture=block_texture
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
        parent=self.parent,
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
        self.entity.world_parent = self.parent

        destroy(pivot)

        # Gán trạng thái logic mới
        self.block_logic = new_block

        # Ép về transform chính xác để tránh sai số animation
        self.update_transform()

        on_complete()

    #animation chơi rơi ở rìa khi nằm
    def animate_fall(self, on_complete):
        duration = 0.7
        fall_distance = 8

        self.entity.animate_y(
            self.entity.y - fall_distance,
            duration=duration,
            curve=curve.linear
        )

        # Xoay nhẹ trong lúc rơi để nhìn tự nhiên hơn
        self.entity.animate_rotation_x(
            self.entity.rotation_x + 45,
            duration=duration,
            curve=curve.linear
        )

        self.entity.animate_rotation_z(
            self.entity.rotation_z + 25,
            duration=duration,
            curve=curve.linear
        )

        invoke(
            on_complete,
            delay=duration
        )

    #animation chơi rơi khi ở rìa khi đứng
    def animate_tip_and_fall(self,invalid_block,direction,on_complete):
        tip_duration = 0.25
        fall_duration = 0.7

        position = self.entity.position
        scale = self.entity.scale

        half_x = scale.x / 2
        half_y = scale.y / 2
        half_z = scale.z / 2

        if direction == "UP":
            pivot_position = Vec3(
                position.x,
                position.y - half_y,
                position.z - half_z
            )
            axis = "x"
            angle = 90

        elif direction == "DOWN":
            pivot_position = Vec3(
                position.x,
                position.y - half_y,
                position.z + half_z
            )
            axis = "x"
            angle = -90

        elif direction == "LEFT":
            pivot_position = Vec3(
                position.x + half_x,
                position.y - half_y,
                position.z
            )
            axis = "z"
            angle = -90

        elif direction == "RIGHT":
            pivot_position = Vec3(
                position.x - half_x,
                position.y - half_y,
                position.z
            )
            axis = "z"
            angle = 90

        else:
            raise ValueError(f"Hướng không hợp lệ: {direction}")

        pivot = Entity(
            parent=scene,
            position=pivot_position
        )

        self.entity.world_parent = self.parent

        if axis == "x":
            pivot.animate_rotation_x(
                angle,
                duration=tip_duration,
                curve=curve.linear
            )
        else:
            pivot.animate_rotation_z(
                angle,
                duration=tip_duration,
                curve=curve.linear
            )

        invoke(
            self.finish_tip,
            pivot,
            fall_duration,
            on_complete,
            delay=tip_duration
        )

    def finish_tip(self, pivot, fall_duration, on_complete):
        self.entity.world_parent = self.parent
        destroy(pivot)

        self.entity.animate_y(
            self.entity.y - 8,
            duration=fall_duration,
            curve=curve.in_quad
        )

        invoke(
            on_complete,
            delay=fall_duration
        )

    #animation cho rơi khi ở cận rìa
    def animate_edge_tip_and_fall(self,supported_cell,direction,on_complete):
        tip_duration = 0.3
        fall_duration = 0.7

        row, col = supported_cell
        tile_x, tile_z = self.grid_to_world(row, col)

        # Mặt trên floor đang ở y = 0.1
        floor_top_y = 0.1

        if direction == "UP":
            # UP: z tăng do grid_to_world dùng z = -row
            pivot_position = Vec3(
                tile_x,
                floor_top_y,
                tile_z + 0.5
            )
            axis = "x"
            angle = 90

        elif direction == "DOWN":
            pivot_position = Vec3(
                tile_x,
                floor_top_y,
                tile_z - 0.5
            )
            axis = "x"
            angle = -90

        elif direction == "LEFT":
            pivot_position = Vec3(
                tile_x - 0.5,
                floor_top_y,
                tile_z
            )
            axis = "z"
            angle = -90

        elif direction == "RIGHT":
            pivot_position = Vec3(
                tile_x + 0.5,
                floor_top_y,
                tile_z
            )
            axis = "z"
            angle = 90

        else:
            raise ValueError(f"Hướng không hợp lệ: {direction}")

        pivot = Entity(
            parent=scene,
            position=pivot_position
        )

        # Đặt block làm con pivot nhưng giữ nguyên world transform
        self.entity.world_parent = self.parent

        if axis == "x":
            pivot.animate_rotation_x(
                angle,
                duration=tip_duration,
                curve=curve.in_quad
            )

        else:
            pivot.animate_rotation_z(
                angle,
                duration=tip_duration,
                curve=curve.in_quad
            )

        invoke(
            self.finish_edge_tip,
            pivot,
            fall_duration,
            on_complete,
            delay=tip_duration
        )

    def finish_edge_tip(self, pivot,fall_duration,on_complete):
        # Giữ transform hiện tại khi rời pivot
        self.entity.world_parent = self.parent

        destroy(pivot)

        self.entity.animate_y(
            self.entity.y - 8,
            duration=fall_duration,
            curve=curve.in_quad
        )

        invoke(
            on_complete,
            delay=fall_duration
        )