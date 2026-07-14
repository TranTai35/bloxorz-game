from ursina import Entity, Vec3, color, curve, destroy, invoke, load_texture

from block import Orientation


class BlockRenderer:
    def __init__(self, block_logic, parent):
        self.block_logic = block_logic
        self.parent = parent
        self.block_texture = load_texture("assets/texture/block.jpg")

        self.entity = Entity(
            parent=self.parent,
            model="cube",
            texture=self.block_texture,
        )
        self.split_entities = [
            Entity(
                parent=self.parent,
                model="cube",
                texture=self.block_texture,
                enabled=False,
            )
            for _ in range(2)
        ]
        self.update_transform()

    def grid_to_world(self, row, col):
        return col, -row

    def get_transform(self, block):
        if block.orientation == Orientation.STANDING:
            row, col = block.pos1
            x, z = self.grid_to_world(row, col)
            return Vec3(x, 1.1, z), Vec3(1, 2, 1)
        if block.orientation == Orientation.HORIZONTAL:
            row1, col1 = block.pos1
            _, col2 = block.pos2
            x, z = self.grid_to_world(row1, (col1 + col2) / 2)
            return Vec3(x, 0.6, z), Vec3(2, 1, 1)
        if block.orientation == Orientation.VERTICAL:
            row1, col1 = block.pos1
            row2, _ = block.pos2
            x, z = self.grid_to_world((row1 + row2) / 2, col1)
            return Vec3(x, 0.6, z), Vec3(1, 1, 2)
        raise ValueError("SPLIT sử dụng hai entity riêng")

    def update_transform(self):
        if self.block_logic.orientation == Orientation.SPLIT:
            self.entity.enabled = False
            for index, (row, col) in enumerate(self.block_logic.get_cells()):
                x, z = self.grid_to_world(row, col)
                cube = self.split_entities[index]
                cube.enabled = True
                cube.position = Vec3(x, 0.6, z)
                cube.scale = Vec3(1, 1, 1)
                cube.rotation = (0, 0, 0)
                cube.color = color.azure if index == self.block_logic.active_index else color.white
            return

        self.entity.enabled = True
        for cube in self.split_entities:
            cube.enabled = False
        position, scale = self.get_transform(self.block_logic)
        self.entity.position = position
        self.entity.scale = scale
        self.entity.rotation = (0, 0, 0)
        self.entity.color = color.white

    def get_pivot_data(self, block, direction):
        position, scale = self.get_transform(block)
        half_x = scale.x / 2
        half_y = scale.y / 2
        half_z = scale.z / 2

        if direction == "UP":
            return Vec3(position.x, position.y - half_y, position.z + half_z), "x", 90
        if direction == "DOWN":
            return Vec3(position.x, position.y - half_y, position.z - half_z), "x", -90
        if direction == "LEFT":
            return Vec3(position.x - half_x, position.y - half_y, position.z), "z", -90
        if direction == "RIGHT":
            return Vec3(position.x + half_x, position.y - half_y, position.z), "z", 90
        raise ValueError(f"Hướng không hợp lệ: {direction}")

    def animate_move(self, old_block, new_block, direction, on_complete):
        if old_block.orientation == Orientation.SPLIT:
            self._animate_split_move(old_block, new_block, direction, on_complete)
            return

        duration = 0.25
        pivot_position, axis, angle = self.get_pivot_data(old_block, direction)
        pivot = Entity(parent=self.parent, position=pivot_position)
        self.entity.world_parent = pivot

        if axis == "x":
            pivot.animate_rotation_x(angle, duration=duration, curve=curve.linear)
        else:
            pivot.animate_rotation_z(angle, duration=duration, curve=curve.linear)

        invoke(
            self._finish_roll_animation,
            pivot,
            new_block,
            on_complete,
            delay=duration,
        )

    def _finish_roll_animation(self, pivot, new_block, on_complete):
        self.entity.world_parent = self.parent
        destroy(pivot)
        self.block_logic = new_block
        self.update_transform()
        on_complete()

    def _animate_split_move(self, old_block, new_block, direction, on_complete):
        duration = 0.12 if direction == "SWITCH" else 0.2
        if direction != "SWITCH":
            row, col = old_block.get_active_cell()
            deltas = {
                "UP": (-1, 0),
                "DOWN": (1, 0),
                "LEFT": (0, -1),
                "RIGHT": (0, 1),
            }
            row_delta, col_delta = deltas[direction]
            x, z = self.grid_to_world(row + row_delta, col + col_delta)
            moving_cube = self.split_entities[old_block.active_index]
            moving_cube.animate_position(
                Vec3(x, 0.6, z),
                duration=duration,
                curve=curve.linear,
            )
        invoke(self._finish_split_animation, new_block, on_complete, delay=duration)

    def _finish_split_animation(self, new_block, on_complete):
        self.block_logic = new_block
        self.update_transform()
        on_complete()

    def animate_fall(self, on_complete):
        duration = 0.7
        targets = (
            self.split_entities
            if self.block_logic.orientation == Orientation.SPLIT
            else [self.entity]
        )
        for target in targets:
            if not target.enabled:
                continue
            target.animate_y(target.y - 8, duration=duration, curve=curve.linear)
            target.animate_rotation_x(target.rotation_x + 45, duration=duration, curve=curve.linear)
            target.animate_rotation_z(target.rotation_z + 25, duration=duration, curve=curve.linear)
        invoke(on_complete, delay=duration)

    def animate_split_fall(self, supported_cells, on_complete):
        duration = 0.7
        supported = set(supported_cells)
        falling_indexes = [
            index
            for index, cell in enumerate(self.block_logic.get_cells())
            if cell not in supported
        ]
        if not falling_indexes:
            falling_indexes = [0, 1]
        for index in falling_indexes:
            cube = self.split_entities[index]
            cube.animate_y(cube.y - 8, duration=duration, curve=curve.in_quad)
            cube.animate_rotation_x(cube.rotation_x + 45, duration=duration, curve=curve.linear)
        invoke(on_complete, delay=duration)

    def animate_tip_and_fall(self, invalid_block, direction, on_complete):
        position = self.entity.position
        scale = self.entity.scale
        half_x, half_y, half_z = scale.x / 2, scale.y / 2, scale.z / 2
        if direction == "UP":
            pivot_position, axis, angle = Vec3(position.x, position.y - half_y, position.z - half_z), "x", 90
        elif direction == "DOWN":
            pivot_position, axis, angle = Vec3(position.x, position.y - half_y, position.z + half_z), "x", -90
        elif direction == "LEFT":
            pivot_position, axis, angle = Vec3(position.x + half_x, position.y - half_y, position.z), "z", -90
        elif direction == "RIGHT":
            pivot_position, axis, angle = Vec3(position.x - half_x, position.y - half_y, position.z), "z", 90
        else:
            raise ValueError(f"Hướng không hợp lệ: {direction}")
        self._tip_from_pivot(pivot_position, axis, angle, on_complete)

    def animate_edge_tip_and_fall(self, supported_cell, direction, on_complete):
        row, col = supported_cell
        tile_x, tile_z = self.grid_to_world(row, col)
        floor_top_y = 0.1
        if direction == "UP":
            pivot_position, axis, angle = Vec3(tile_x, floor_top_y, tile_z + 0.5), "x", 90
        elif direction == "DOWN":
            pivot_position, axis, angle = Vec3(tile_x, floor_top_y, tile_z - 0.5), "x", -90
        elif direction == "LEFT":
            pivot_position, axis, angle = Vec3(tile_x - 0.5, floor_top_y, tile_z), "z", -90
        elif direction == "RIGHT":
            pivot_position, axis, angle = Vec3(tile_x + 0.5, floor_top_y, tile_z), "z", 90
        else:
            raise ValueError(f"Hướng không hợp lệ: {direction}")
        self._tip_from_pivot(pivot_position, axis, angle, on_complete)

    def _tip_from_pivot(self, pivot_position, axis, angle, on_complete):
        tip_duration = 0.3
        fall_duration = 0.7
        # The pivot belongs to the level root and the block must actually be its child.
        # This fixes the half-on/half-off-board crash and makes the edge rotation visible.
        pivot = Entity(parent=self.parent, position=pivot_position)
        self.entity.world_parent = pivot
        if axis == "x":
            pivot.animate_rotation_x(angle, duration=tip_duration, curve=curve.in_quad)
        else:
            pivot.animate_rotation_z(angle, duration=tip_duration, curve=curve.in_quad)
        invoke(
            self._finish_tip,
            pivot,
            fall_duration,
            on_complete,
            delay=tip_duration,
        )

    def _finish_tip(self, pivot, fall_duration, on_complete):
        self.entity.world_parent = self.parent
        destroy(pivot)
        self.entity.animate_y(
            self.entity.y - 8,
            duration=fall_duration,
            curve=curve.in_quad,
        )
        invoke(on_complete, delay=fall_duration)
