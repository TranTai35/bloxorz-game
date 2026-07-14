from ursina import camera, Vec3


def setup_camera(board):
    floor_positions = []

    for row in range(board.rows):
        for col in range(board.cols):
            if not board.is_void(row, col):
                x = col
                z = -row
                floor_positions.append((x, z))

    if not floor_positions:
        camera.position = Vec3(0, 10, -10)
        camera.look_at(Vec3(0, 0, 0))
        return

    min_x = min(x for x, z in floor_positions)
    max_x = max(x for x, z in floor_positions)

    min_z = min(z for x, z in floor_positions)
    max_z = max(z for x, z in floor_positions)

    center_x = (min_x + max_x) / 2
    center_z = (min_z + max_z) / 2

    width = max_x - min_x + 1
    depth = max_z - min_z + 1
    board_size = max(width, depth)

    board_center = Vec3(center_x, 0, center_z)

    camera.position = Vec3(center_x - board_size * 2,board_size * 3,center_z - board_size * 3)

    camera.look_at(board_center)