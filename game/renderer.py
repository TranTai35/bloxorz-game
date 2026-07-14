from ursina import Entity, color, load_texture


class Renderer:
    TILE_COLORS = {
        "floor": color.white,
        "goal": color.white,
        "fragile": color.rgb(235, 145, 45),
        "soft": color.rgb(55, 180, 235),
        "heavy": color.rgb(210, 65, 70),
        "split": color.rgb(175, 85, 220),
        "bridge": color.rgb(95, 190, 115),
    }

    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.tiles = []
        self.bridge_tiles = {}
        self.floor_texture = load_texture("assets/texture/floor.jpg")
        self.goal_texture = load_texture("assets/texture/goal.jpg")

    def grid_to_world(self, row, col):
        return col, -row

    def _create_switch_marker(self, row, col, switch_type):
        x, z = self.grid_to_world(row, col)
        if switch_type == "soft":
            marker = Entity(
                parent=self.parent,
                model="cube",
                color=color.rgb(20, 105, 175),
                position=(x, 0.16, z),
                rotation_y=45,
                scale=(0.55, 0.04, 0.55),
            )
            self.tiles.append(marker)
        elif switch_type == "heavy":
            for rotation in (45, -45):
                marker = Entity(
                    parent=self.parent,
                    model="cube",
                    color=color.rgb(125, 20, 25),
                    position=(x, 0.16, z),
                    rotation_y=rotation,
                    scale=(0.75, 0.04, 0.12),
                )
                self.tiles.append(marker)
        elif switch_type == "split":
            for offset in (-0.22, 0.22):
                marker = Entity(
                    parent=self.parent,
                    model="cube",
                    color=color.rgb(90, 30, 135),
                    position=(x + offset, 0.16, z),
                    scale=(0.12, 0.04, 0.65),
                )
                self.tiles.append(marker)

    def create_map(self):
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                tile_type = self.board.tile_type(row, col)
                if tile_type == "void" and not self.board.is_bridge(row, col):
                    continue

                x, z = self.grid_to_world(row, col)
                selected_texture = (
                    self.goal_texture if tile_type == "goal" else self.floor_texture
                )
                tile = Entity(
                    parent=self.parent,
                    model="cube",
                    texture=selected_texture,
                    color=self.TILE_COLORS.get(tile_type, color.white),
                    position=(x, 0, z),
                    scale=(1, 0.2, 1),
                )
                self.tiles.append(tile)

                if tile_type == "bridge":
                    bridge_id = self.board.bridge_at[(row, col)]
                    self.bridge_tiles.setdefault(bridge_id, []).append(tile)
                elif tile_type in {"soft", "heavy", "split"}:
                    self._create_switch_marker(row, col, tile_type)

        self.refresh_bridge_states(self.board.initial_bridge_states)

    def refresh_bridge_states(self, bridge_states):
        states = self.board.bridge_state_dict(bridge_states)
        for bridge_id, tiles in self.bridge_tiles.items():
            for tile in tiles:
                tile.enabled = states.get(bridge_id, False)
