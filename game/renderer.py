from ursina import Entity, color, load_texture


class Renderer:
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent

        # Lưu toàn bộ tile để sau này có thể hủy cùng scene
        self.tiles = []

        # Lưu riêng bridge theo bridge_id
        # Ví dụ:
        # {
        #     "bridge_1": [tile1, tile2],
        #     "bridge_2": [tile3]
        # }
        self.bridge_tiles = {}

        # Load texture một lần
        self.tile_textures = {
            "floor": load_texture(
                "assets/texture/floor.jpg"
            ),

            "goal": load_texture(
                "assets/texture/goal.jpg"
            ),

            "bridge": load_texture(
                "assets/texture/bridge.jpg"
            ),

            "fragile": load_texture(
                "assets/texture/fragile_tile.jpg"
            ),

            "soft": load_texture(
                "assets/texture/soft_switch.jpg"
            ),

            "heavy": load_texture(
                "assets/texture/heavy_switch.jpg"
            ),

            "split": load_texture(
                "assets/texture/split_switch.jpg"
            ),
        }

        self.check_textures()

    def check_textures(self):
        """
        Kiểm tra texture nào không load được.
        """
        for tile_type, texture in self.tile_textures.items():
            if texture is None:
                print(
                    f"Không load được texture của tile: "
                    f"{tile_type}"
                )

    def grid_to_world(self, row, col):
        """
        Chuyển tọa độ ma trận thành tọa độ Ursina.

        row tăng xuống dưới trong ma trận,
        nhưng z của Ursina được đặt ngược lại.
        """
        x = col
        z = -row

        return x, z

    def get_tile_texture(self, tile_type):
        """
        Lấy texture dựa trên loại tile.

        Nếu tile_type không tồn tại trong dictionary,
        dùng floor texture làm mặc định.
        """
        return self.tile_textures.get(
            tile_type,
            self.tile_textures["floor"]
        )

    def create_map(self):
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                tile_type = self.board.tile_type(
                    row,
                    col
                )

                # Không tạo Entity cho ô void bình thường.
                # Bridge có thể nằm trên ô void nên vẫn phải tạo.
                if (
                    tile_type == "void"
                    and not self.board.is_bridge(row, col)
                ):
                    continue

                x, z = self.grid_to_world(row, col)

                selected_texture = self.get_tile_texture(
                    tile_type
                )

                tile = Entity(
                    parent=self.parent,
                    model="cube",
                    texture=selected_texture,

                    # Dùng màu trắng để texture không bị đổi màu
                    color=color.white,

                    position=(x, 0, z),
                    scale=(1, 0.2, 1)
                )

                self.tiles.append(tile)

                # Lưu bridge để có thể bật/tắt sau này
                if tile_type == "bridge":
                    bridge_id = self.board.bridge_at[
                        (row, col)
                    ]

                    self.bridge_tiles.setdefault(
                        bridge_id,
                        []
                    ).append(tile)

        # Áp dụng trạng thái bridge ban đầu
        self.refresh_bridge_states(
            self.board.initial_bridge_states
        )

    def refresh_bridge_states(self, bridge_states):
        """
        Bật hoặc tắt Entity của bridge theo trạng thái hiện tại.
        """
        states = self.board.bridge_state_dict(
            bridge_states
        )

        for bridge_id, tiles in self.bridge_tiles.items():
            is_open = states.get(
                bridge_id,
                False
            )

            for tile in tiles:
                tile.enabled = is_open