# from ursina import Ursina, Entity, EditorCamera, color


# # Khởi tạo ứng dụng Ursina
# app = Ursina()


# # Tạo một khối lập phương
# cube = Entity(
#     model="cube",
#     color=color.orange,
#     position=(0, 0, 0),
#     scale=(1, 1, 1)
# )

# quad = Entity(
#     model="quad",
#     color=color.red,
#     position=(0, -, 0),
#     rotation= (90,0,0),
#     scale=(1, 1, 1)
# )

# # Cho phép dùng chuột để xoay và di chuyển camera
# EditorCamera()


# # Chạy ứng dụng
# app.run()

from ursina import Ursina, Entity, EditorCamera, color, camera, Vec3

app = Ursina()

cube = Entity(
    model='cube',
    texture='block.jpg',
    color=color.white,
    position=(0, 0, 0),
    scale=(1, 2, 1)
)

floor = Entity(
    model='cube',
    texture= 'floor.jpg',
    color=color.white,
    position=(0, -1.05, 0),
    rotation=(0, 0, 0),
    scale=(1, 0.1, 1)
)

# Camera kiểu isometric
# camera.position = (-10, 30, -10)
# camera.look_at(Vec3(0, 0, 0))
EditorCamera()

app.run()