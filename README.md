# Bloxorz Solver

Dự án mô phỏng trò chơi **Bloxorz** bằng Python và Ursina. Người chơi điều khiển một khối hộp lăn trên bản đồ để đưa khối đứng thẳng tại ô đích. Dự án hỗ trợ hai chế độ chính:

- **Play**: người chơi tự điều khiển khối bằng bàn phím.
- **Solve**: người dùng chọn thuật toán, sau đó chương trình tự tìm đường và phát lại lời giải bằng animation.

README này mô tả cấu trúc dự án, vai trò của từng file, luồng hoạt động và cách tiếp tục phát triển.

---

## 1. Công nghệ sử dụng

- Python 3
- Ursina Engine
- JSON để lưu bản đồ
- Các thuật toán tìm kiếm trạng thái như BFS, DFS, UCS và A*

Cài Ursina:

```bash
pip install ursina
```

Chạy chương trình:

```bash
python main.py
```

Nên chạy lệnh từ thư mục gốc của dự án để Ursina tìm đúng thư mục `assets`, `maps` và các module Python.

---

## 2. Cấu trúc thư mục đề xuất

```text
Bloxorz Solver/
├── main.py
├── app_controller.py
├── board.py
├── block.py
├── state.py
│
├── maps/
│   ├── level1.json
│   ├── level2.json
│   └── ...
│
├── algorithms/
│   ├── __init__.py
│   ├── successor.py
│   ├── search_result.py
│   ├── solver.py
│   ├── bfs.py
│   ├── dfs.py
│   ├── ucs.py
│   └── astar.py
│
├── game/
│   ├── __init__.py
│   ├── game.py
│   ├── renderer.py
│   ├── block_renderer.py
│   ├── camera_controller.py
│   └── audio_manager.py
│
├── scenes/
│   ├── __init__.py
│   ├── menu_scene.py
│   ├── level_select_scene.py
│   └── algorithm_select_panel.py
│
└── assets/
    ├── texture/
    │   ├── floor.jpg
    │   ├── goal.jpg
    │   └── block.jpg
    ├── sprites/
    │   └── background.jpg
    └── sounds/
        ├── background_music.*
        └── move_sound.*
```

Tên file trong `assets` có thể khác tùy phiên bản dự án. Khi đổi tên file, cần sửa lại đường dẫn trong code.

---

# 3. Luồng hoạt động tổng quát

```text
main.py
   ↓
AppController
   ↓
Main Menu
   ├── Play
   │     ↓
   │  Level Select
   │     ↓
   │  Game ở chế độ người chơi
   │
   └── Solve
         ↓
      Level Select
         ↓
      Chọn thuật toán
         ↓
      Game ở chế độ tự giải
```

`AppController` chịu trách nhiệm chuyển đổi giữa các màn hình. Mỗi màn hình được tạo thành một `Entity`, khi chuyển màn hình thì màn hình cũ phải được hủy để tránh UI, board hoặc block còn sót lại.

---

# 4. Mô tả từng file

## `main.py`

Đây là điểm bắt đầu của chương trình.

Nhiệm vụ chính:

- Khởi tạo Ursina.
- Thiết lập cửa sổ.
- Tạo `AppController`.
- Gọi `app.run()`.

Ví dụ:

```python
from ursina import Ursina, window
from app_controller import AppController

app = Ursina()

window.title = "Bloxorz Solver"
window.borderless = False
window.fullscreen = False

controller = AppController()

app.run()
```

Không nên tạo trực tiếp `Game(...)` trong `main.py` nữa, vì việc chuyển màn hình được quản lý bởi `AppController`.

---

## `app_controller.py`

Đây là bộ điều khiển các màn hình của ứng dụng.

### Thuộc tính quan trọng

```python
self.current_screen
```

Lưu màn hình hiện tại, có thể là:

- `MenuScene`
- `LevelSelectScene`
- `Game`

### Các hàm chính

#### `clear_screen()`

Hủy màn hình hiện tại trước khi mở màn hình mới.

```python
def clear_screen(self):
    if self.current_screen is not None:
        destroy(self.current_screen)
        self.current_screen = None
```

#### `show_main_menu()`

Hiện menu chính có hai nút `Play` và `Solve`.

#### `show_level_select(mode)`

Hiện màn hình chọn level.

`mode` có thể là:

```text
play
solve
```

#### `handle_level_selected(level_path, mode, algorithm=None)`

Nhận level được chọn từ `LevelSelectScene`.

- Nếu là `play`, mở game ngay.
- Nếu là `solve`, chỉ mở game sau khi đã chọn thuật toán.

#### `start_game(level_path, mode, algorithm)`

Tạo `Game` với đúng level, chế độ và thuật toán.

---

## `board.py`

Quản lý dữ liệu bản đồ.

### Nhiệm vụ

- Đọc file JSON.
- Lưu ma trận bản đồ.
- Lưu vị trí bắt đầu và vị trí đích.
- Kiểm tra ô hợp lệ.
- Kiểm tra block có rơi khỏi bản đồ hay không.
- Kiểm tra điều kiện thắng.

### Các thuộc tính thường dùng

```python
self.grid
self.rows
self.cols
self.start
self.goal
```

### Các hàm chính

#### `is_inside(row, col)`

Kiểm tra tọa độ có nằm trong ma trận hay không.

#### `is_void(row, col)`

Kiểm tra ô có phải khoảng trống hay không.

Trong bản đồ hiện tại, ký hiệu `#` thường được dùng cho khoảng trống.

#### `is_floor(row, col)`

Kiểm tra ô có phải sàn hợp lệ hay không.

#### `is_goal(row, col)`

Kiểm tra tọa độ có phải ô đích hay không.

#### `is_valid_block(block)`

Kiểm tra tất cả ô mà block đang chiếm có nằm trên sàn hay không.

#### `is_win(block)`

Trả về `True` khi block:

- đang ở trạng thái đứng thẳng;
- đứng đúng tại ô goal.

---

## `block.py`

Quản lý logic và trạng thái của khối hộp.

### `Orientation`

Các hướng/trạng thái của block:

```python
STANDING
HORIZONTAL
VERTICAL
```

Ý nghĩa:

- `STANDING`: block đứng thẳng trên một ô.
- `HORIZONTAL`: block nằm ngang trên hai cột.
- `VERTICAL`: block nằm dọc trên hai hàng.

### Thuộc tính chính

```python
self.pos1
self.pos2
self.orientation
```

`pos1` và `pos2` lưu các ô mà block đang chiếm.

### Các hàm chính

#### `copy()`

Tạo bản sao của block để thử một nước đi mà không làm thay đổi trạng thái hiện tại.

#### `get_cells()`

Trả về danh sách các ô mà block đang chiếm.

#### `move_up()`
#### `move_down()`
#### `move_left()`
#### `move_right()`

Cập nhật tọa độ và orientation theo từng hướng.

#### `move(direction)`

Hàm tổng quát nhận chuỗi:

```text
UP
DOWN
LEFT
RIGHT
```

rồi gọi hàm di chuyển tương ứng.

---

## `state.py`

Biểu diễn một trạng thái trong thuật toán tìm kiếm.

### Thuộc tính

```python
self.block
self.parent
self.action
self.cost
```

Ý nghĩa:

- `block`: trạng thái khối tại node hiện tại.
- `parent`: node cha.
- `action`: hành động từ node cha đến node này.
- `cost`: tổng chi phí từ trạng thái bắt đầu.

### Hàm chính

#### `get_path()`

Đi ngược từ node goal về node bắt đầu thông qua `parent`, sau đó đảo danh sách để thu được đường đi đúng.

Ví dụ kết quả:

```python
["RIGHT", "DOWN", "LEFT"]
```

#### `__eq__()` và `__hash__()`

Cho phép dùng `State` trong `set` hoặc dictionary. Hai trạng thái được xem là giống nhau khi block có cùng vị trí và cùng orientation.

---

# 5. Thư mục `algorithms`

## `algorithms/successor.py`

Sinh các trạng thái kế tiếp từ một trạng thái hiện tại.

### `get_successors(current_state, board)`

Thử lần lượt bốn hướng:

```python
["UP", "DOWN", "LEFT", "RIGHT"]
```

Với mỗi hướng:

1. Copy block hiện tại.
2. Thực hiện nước đi.
3. Kiểm tra block có còn hợp lệ trên board hay không.
4. Nếu hợp lệ, tạo `State` mới.

Trạng thái làm block rơi khỏi map không được đưa vào danh sách successor.

---

## `algorithms/search_result.py`

Chuẩn hóa kết quả trả về của tất cả thuật toán.

Các thuật toán nên trả về cùng một kiểu dữ liệu để `Game` không cần biết chi tiết triển khai bên trong.

### Thuộc tính đề xuất

```python
path
steps
expanded_nodes
search_time
found
```

Ví dụ:

```python
class SearchResult:
    def __init__(
        self,
        path=None,
        expanded_nodes=0,
        search_time=0.0,
        found=False
    ):
        self.path = path if path is not None else []
        self.steps = len(self.path)
        self.expanded_nodes = expanded_nodes
        self.search_time = search_time
        self.found = found
```

---

## `algorithms/bfs.py`

Tìm đường bằng Breadth-First Search.

Đặc điểm:

- Dùng queue.
- Mở rộng trạng thái theo từng lớp.
- Nếu mỗi nước đi có cùng chi phí, BFS tìm được lời giải ít bước nhất.

Các thông số cần ghi nhận:

```python
expanded_nodes
search_time
path
```

---

## `algorithms/ids.py`

Dùng Iterative Deepening Search.

Cách hoạt động:

- Chạy Depth-Limited Search với giới hạn độ sâu tăng dần.
- Bắt đầu từ giới hạn 0, sau đó 1, 2, 3...
- Dừng khi tìm thấy goal.

Cần tránh lặp trạng thái vô hạn trong cùng một nhánh.

---

## `algorithms/ucs.py`

Dùng Uniform Cost Search.

Đặc điểm:

- Dùng priority queue.
- Mở rộng node có tổng chi phí nhỏ nhất trước.
- Một lần roll có cost 1; đi qua fragile tile cộng 1; kích hoạt switch cộng
  0.25; đổi cube đang điều khiển bằng Space có cost 0.5.
- Cost không đồng đều giúp UCS có thể chọn đường an toàn hơn BFS dù số bước
  bằng nhau.

---

## `algorithms/astar.py`

Dùng A* Search.

Công thức:

```text
f(n) = g(n) + h(n)
```

Trong đó:

- `g(n)`: chi phí từ start đến node hiện tại.
- `h(n)`: heuristic ước lượng khoảng cách đến goal.

Heuristic hiện tại lấy khoảng cách Manhattan nhỏ nhất từ các ô block đang chiếm
đến goal, chia 2 và làm tròn lên. Nếu block chưa đứng thì lower bound ít nhất là
1. Đây là heuristic admissible vì một lần roll chỉ có thể rút ngắn khoảng cách
tọa độ tối đa hai ô, còn các penalty của UCS đều không âm.

---

## `algorithms/solver.py`

Đóng vai trò bộ chọn thuật toán.

Ví dụ:

```python
def solve(board, start_block, algorithm_name):
    algorithm_name = algorithm_name.upper()

    if algorithm_name == "BFS":
        return bfs(board, start_block)

    if algorithm_name == "IDS":
        return ids(board, start_block)

    if algorithm_name == "UCS":
        return ucs(board, start_block)

    if algorithm_name == "ASTAR":
        return astar(board, start_block)

    raise ValueError(
        f"Thuật toán không hợp lệ: {algorithm_name}"
    )
```

`Game` chỉ gọi hàm `solve()` thay vì gọi trực tiếp từng thuật toán.

---

# 6. Thư mục `game`

## `game/game.py`

Đây là class chính điều khiển một level.

### Constructor

```python
def __init__(
    self,
    level_path,
    mode="play",
    algorithm=None,
    on_back=None
):
```

Ý nghĩa tham số:

- `level_path`: đường dẫn file JSON.
- `mode`: `play` hoặc `solve`.
- `algorithm`: tên thuật toán khi mode là `solve`.
- `on_back`: callback để quay lại màn hình chọn level.

### Các nhóm thuộc tính quan trọng

#### Trạng thái game

```python
self.move_count
self.is_moving
self.has_won
self.has_lost
```

#### Trạng thái solver

```python
self.search_result
self.solution_moves
self.solution_index
self.is_solving
```

#### Thời gian

```python
self.scene_start_time
self.total_time
```

#### Root của scene

```python
self.world_root
self.ui_root
```

- `world_root`: chứa board, block, sky và các object 3D.
- `ui_root`: chứa text, button và panel UI.

Việc dùng root giúp hủy toàn bộ level sạch sẽ khi chuyển scene.

### Các hàm quan trọng

#### `input(key)`

Xử lý bàn phím.

Trong mode `play`:

```text
W = UP
S = DOWN
A = LEFT
D = RIGHT
R = Restart
M = bật/tắt nhạc
Escape = quay lại Level Select
```

Trong mode `solve`, người dùng không được dùng WASD để điều khiển block.

#### `try_move(direction)`

Thử di chuyển block.

- Copy trạng thái hiện tại.
- Di chuyển block copy.
- Nếu hợp lệ, phát animation rồi gọi `finish_move()`.
- Nếu không hợp lệ, phát animation rơi rồi gọi `show_lose()`.

#### `finish_move(new_block)`

Được gọi sau khi animation lật kết thúc.

Nhiệm vụ:

- Cập nhật block logic.
- Đồng bộ renderer.
- Tăng số bước.
- Phát âm thanh.
- Kiểm tra thắng.
- Nếu solver đang chạy, gọi bước tiếp theo.

#### `start_fall(invalid_block, direction)`

Xử lý trường hợp block rơi khỏi map.

Phân biệt:

- Một phần block còn được sàn đỡ: xoay quanh mép rồi rơi.
- Không còn phần nào được đỡ: rơi thẳng.

#### `start_solver()`

Gọi thuật toán đã chọn và nhận `SearchResult`.

Nếu tìm thấy lời giải:

```python
self.solution_moves = self.search_result.path
```

sau đó gọi `play_next_solution_move()`.

#### `play_next_solution_move()`

Lấy từng hướng trong lời giải và gọi `try_move()`.

Không dùng vòng lặp để chạy toàn bộ path cùng lúc vì animation cần hoàn tất từng bước.

#### `create_ui()`

Tạo giao diện trong level:

- số bước;
- thời gian;
- tên thuật toán;
- nút Back;
- panel thắng/thua;
- nút Restart;
- nút quay về Level Select.

#### `show_win()`

Hiện kết quả khi thắng.

Trong mode `play`:

```text
YOU WIN
Moves
Time
```

Trong mode `solve`:

```text
SOLVED
Algorithm
Moves
Expanded nodes
Search time
Total time
```

#### `show_lose()`

Hiện kết quả khi người chơi làm block rơi.

#### `show_no_solution()`

Hiện thông báo khi thuật toán không tìm thấy lời giải.

#### `show_solver_error(message)`

Hiện lỗi khi thuật toán chưa được hỗ trợ hoặc có lỗi khi chạy.

#### `restart()`

Đưa block về vị trí ban đầu, reset số bước, thời gian và trạng thái.

Trong mode `solve`, sau khi reset thì solver được chạy lại.

#### `back_to_level_select()`

Gọi callback `on_back` để quay lại màn hình chọn level.

#### `on_destroy()`

Dọn dẹp UI và các object khi rời level.

Nếu mọi object 3D đều là con của `world_root`, việc hủy `Game` sẽ tự hủy chúng theo.

---

## `game/renderer.py`

Hiển thị bản đồ 3D.

### Thuộc tính

```python
self.board
self.parent
self.tiles
self.floor_texture
self.goal_texture
```

### `grid_to_world(row, col)`

Chuyển tọa độ ma trận sang tọa độ Ursina:

```python
x = col
z = -row
```

### `create_map()`

Duyệt toàn bộ ma trận:

- Bỏ qua ô void.
- Tạo `Entity` cho ô sàn.
- Nếu là goal, dùng texture goal.
- Nếu là ô thường, dùng texture floor.
- Mọi tile phải có `parent=self.parent`.

Ví dụ:

```python
if self.board.is_goal(row, col):
    selected_texture = self.goal_texture
else:
    selected_texture = self.floor_texture
```

Không nên load texture lại trong mỗi vòng lặp. Hãy load một lần trong `__init__()`.

---

## `game/block_renderer.py`

Hiển thị block và quản lý animation.

### Thuộc tính

```python
self.block_logic
self.parent
self.entity
```

### `grid_to_world(row, col)`

Chuyển tọa độ grid sang Ursina.

### `get_transform(block)`

Tính `position` và `scale` theo orientation.

Ví dụ:

```text
STANDING   -> scale (1, 2, 1)
HORIZONTAL -> scale (2, 1, 1)
VERTICAL   -> scale (1, 1, 2)
```

### `update_transform()`

Ép entity về đúng vị trí, scale và rotation dựa trên logic hiện tại.

Hàm này giúp loại bỏ sai số sau animation.

### `get_pivot_data(block, direction)`

Tính:

- vị trí pivot;
- trục xoay;
- góc xoay.

### `animate_move(...)`

Tạo pivot tại cạnh tiếp xúc với sàn rồi xoay block 90 độ.

Block được tạm thời đặt làm con của pivot:

```python
self.entity.world_parent = pivot
```

### `finish_animation(...)`

- Đưa block trở lại `self.parent`.
- Hủy pivot.
- Cập nhật logic.
- Ép transform chính xác.
- Gọi callback.

### `animate_fall(on_complete)`

Cho block rơi xuống khi không còn ô sàn đỡ.

### `animate_edge_tip_and_fall(...)`

Xử lý trường hợp một phần block còn tựa trên ô ở rìa. Block xoay thêm quanh mép ngoài của ô sàn rồi mới rơi.

### Lưu ý về parent

Mọi pivot nên có:

```python
parent=self.parent
```

Khi xoay, block phải có:

```python
self.entity.world_parent = pivot
```

Khi animation kết thúc:

```python
self.entity.world_parent = self.parent
```

Không nên đưa block trở lại `scene`, vì như vậy block có thể bị tách khỏi `world_root` và không bị hủy khi đổi màn hình.

---

## `game/camera_controller.py`

Thiết lập góc nhìn isometric cho từng board.

### `setup_camera(board)`

Nhiệm vụ:

- Tìm giới hạn của các ô sàn.
- Tính tâm board.
- Tính kích thước board.
- Đặt camera xa hoặc gần tùy kích thước level.
- Cho camera nhìn vào tâm board.

Nhờ vậy level lớn và level nhỏ đều hiển thị tương đối phù hợp.

---

## `game/audio_manager.py`

Quản lý âm thanh.

Nhiệm vụ:

- Phát nhạc nền.
- Phát âm thanh khi block hoàn thành một nước đi.
- Bật hoặc tắt nhạc bằng phím `M`.

Các hàm thường có:

```python
play_move_sound()
toggle_music()
```

---

# 7. Thư mục `scenes`

## `scenes/menu_scene.py`

Màn hình menu chính.

Có hai nút:

```text
PLAY
SOLVE
```

Các callback `on_play` và `on_solve` được truyền từ `AppController`.

UI nên được đặt trong một `ui_root` để hủy sạch khi rời menu.

---

## `scenes/level_select_scene.py`

Màn hình chọn level.

### Nhiệm vụ

- Đọc tự động tất cả file `.json` trong thư mục `maps`.
- Sắp xếp level theo số.
- Tạo số nút tương ứng số level hiện có.
- Xử lý khác nhau giữa mode `play` và `solve`.

### `get_level_files()`

Dùng `Path("maps").glob("*.json")` để lấy danh sách level.

### `create_level_buttons()`

Tạo button theo dạng lưới.

Trong lambda của vòng lặp cần lưu giá trị hiện tại:

```python
button.on_click = (
    lambda path=str(level_path):
    self.select_level(path)
)
```

Không nên viết trực tiếp `lambda: self.select_level(level_path)` vì tất cả nút có thể trỏ tới level cuối cùng.

### `select_level(level_path)`

- Mode `play`: mở game ngay.
- Mode `solve`: lưu level được chọn và mở panel chọn thuật toán.

### `open_algorithm_panel(level_path)`

Tạo `AlgorithmSelectPanel` làm con của `self.ui_root`.

### `select_algorithm(algorithm)`

Ghép level đã chọn với thuật toán, sau đó gọi callback để mở Game.

### `close_algorithm_panel()`

Hủy panel thuật toán và đặt biến về `None`.

---

## `scenes/algorithm_select_panel.py`

Panel chọn thuật toán.

Có bốn lựa chọn:

```text
BFS
IDS
UCS
A*
```

Panel chỉ chịu trách nhiệm trả tên thuật toán về `LevelSelectScene`.

Không lưu `selected_level_path` trong panel. Biến đó thuộc về `LevelSelectScene`.

### `select_algorithm(algorithm_name)`

Chỉ gọi:

```python
self.on_algorithm_selected(algorithm_name)
```

Panel nên nhận `parent` từ `LevelSelectScene`, không nên tự làm con trực tiếp của `camera.ui`, vì nếu không nó có thể còn tồn tại sau khi chuyển sang Game.

---

# 8. Định dạng file level JSON

Ví dụ:

```json
{
  "grid": [
    "#######",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#######"
  ],
  "start": [2, 2],
  "goal": [4, 4]
}
```

Ý nghĩa:

- `grid`: ma trận bản đồ.
- `start`: vị trí block bắt đầu ở trạng thái đứng.
- `goal`: vị trí đích.

Ký hiệu hiện tại:

```text
# = khoảng trống
. = ô sàn
F = ô dễ vỡ
S = soft switch
H = heavy switch
X = split switch
```

Bridge và liên kết switch được khai báo tường minh để trạng thái đóng/mở có thể
được lưu trong state của solver. Ví dụ:

```json
{
  "grid": ["#########", "#..S#...#", "#########"],
  "start": [1, 1],
  "goal": [1, 7],
  "bridges": {
    "bridge_1": {
      "cells": [[1, 4]],
      "initial_open": false
    }
  },
  "switches": [
    {
      "id": "switch_1",
      "position": [1, 3],
      "type": "soft",
      "bridges": ["bridge_1"],
      "action": "toggle"
    }
  ]
}
```

`type` nhận `soft`, `heavy` hoặc `split`. `action` nhận `toggle`, `open`
hoặc `close`. Với permanent switch có thể dùng `"behavior": "permanent"`
và `"state": "open"`. Split switch khai báo thêm hai tọa độ
`"targets": [[r1, c1], [r2, c2]]`.

---

# 9. Cách thêm level mới

1. Tạo file JSON mới trong thư mục `maps`.
2. Đặt tên theo dạng:

```text
level4.json
level5.json
```

3. Khởi động lại game.
4. Màn hình Level Select sẽ tự tạo thêm nút tương ứng.

Không cần sửa code tạo button.

---

# 10. Cách thêm thuật toán mới

Ví dụ thêm Greedy Best-First Search:

1. Tạo file:

```text
algorithms/gbfs.py
```

2. Cho hàm trả về `SearchResult`.
3. Import và thêm nhánh trong `algorithms/solver.py`.
4. Thêm button trong `algorithm_select_panel.py`.

Ví dụ:

```python
if algorithm_name == "GBFS":
    return gbfs(board, start_block)
```

---

# 11. Hai loại thời gian trong chế độ Solve

## `search_time`

Chỉ đo thời gian thuật toán tìm lời giải.

Dùng để so sánh hiệu suất BFS, IDS, UCS và A*.

```python
search_start = time.perf_counter()

# chạy thuật toán

search_time = time.perf_counter() - search_start
```

## `total_time`

Đo từ lúc vào scene Game đến khi animation đi hết đường và block tới goal.

Bao gồm:

- thời gian thuật toán;
- thời gian animation;
- khoảng nghỉ giữa các bước.

Không dùng `total_time` để kết luận thuật toán nào nhanh hơn, vì phần lớn thời gian có thể đến từ animation.

---

# 12. Những lỗi thường gặp

## Texture chỉ hiện màu trắng

Kiểm tra:

- đường dẫn file có đúng không;
- `texture` hay `textures` có đúng tên thư mục không;
- file có thật sự là JPG hoặc PNG không;
- không được chỉ đổi tên WebP thành JPG;
- nên dùng `load_texture()` để kiểm tra.

## Board còn tồn tại khi quay lại menu

Nguyên nhân thường là tile được tạo trực tiếp dưới `scene`.

Cách sửa:

- tạo `world_root` trong `Game`;
- cho Renderer, BlockRenderer, Sky và pivot làm con của `world_root`;
- không đưa block trở lại `scene` sau animation.

## Panel chọn thuật toán còn hiện sau khi vào Game

Nguyên nhân: panel là con trực tiếp của `camera.ui`.

Cách sửa: truyền `parent=self.ui_root` từ `LevelSelectScene`.

## `Game` không có `ui_root`

Phải tạo:

```python
self.ui_root = Entity(parent=camera.ui)
```

trước khi gọi:

```python
self.create_ui()
```

## Tất cả nút level mở cùng một level

Trong lambda vòng lặp, phải lưu giá trị hiện tại:

```python
lambda path=str(level_path): self.select_level(path)
```

## WebP không đọc được

Phiên bản Panda3D/Ursina hiện tại có thể không hỗ trợ `.webp` làm texture. Hãy chuyển thật sự sang PNG hoặc JPG bằng Paint hoặc phần mềm chỉnh ảnh.

---

# 13. Quy tắc khi phát triển tiếp

- Không đặt toàn bộ code vào một file.
- Logic của block không được phụ thuộc vào Ursina.
- Board chỉ quản lý dữ liệu map, không tạo Entity.
- Renderer chỉ hiển thị, không tự thay đổi logic game.
- Các thuật toán không được thao tác trực tiếp với Entity hoặc animation.
- Mỗi thuật toán phải trả về `SearchResult`.
- Mọi object của một level nên nằm dưới `world_root` hoặc `ui_root`.
- Khi thêm tính năng mới, kiểm tra cả mode `play` và `solve`.

---

# 14. Công việc còn có thể phát triển

- Thêm màn hình hướng dẫn.
- Thêm chọn tốc độ animation trong mode Solve.
- Thêm khóa level hoặc lưu tiến trình.
- Thêm ảnh preview cho từng level.
- Thêm nút pause khi solver đang chạy.
- Thêm bảng so sánh kết quả nhiều thuật toán trên cùng level.
- Hoàn thiện báo cáo PDF, biểu đồ thí nghiệm và video demo của nhóm.

---

# 15. Quy trình làm việc nhóm đề xuất

Mỗi thành viên nên tạo branch riêng:

```bash
git checkout -b feature/ten-tinh-nang
```

Ví dụ:

```bash
git checkout -b feature/astar
git checkout -b feature/advanced-tiles
git checkout -b feature/ui-improvement
```

Trước khi code:

```bash
git pull origin main
```

Sau khi hoàn thành:

```bash
git add .
git commit -m "Add A* solver"
git push origin feature/astar
```

Sau đó tạo Pull Request để người khác review trước khi merge vào `main`.

Không nên để nhiều người sửa cùng một file lớn trong cùng thời điểm nếu có thể tránh được.

---

# 16. Gợi ý phân chia công việc

| Thành viên | Phần phụ trách |
|---|---|
| Người 1 | GUI, menu, level select, Game flow |
| Người 2 | BFS và IDS |
| Người 3 | UCS và A* |
| Người 4 | Tile đặc biệt, switch, bridge |
| Người 5 | Test level, báo cáo, thống kê và video |

Có thể thay đổi tùy số thành viên trong nhóm.

---

# 17. Trạng thái hiện tại của dự án

Các phần đã có hoặc đang hoạt động:

- Đọc map JSON.
- Hiển thị board 3D.
- Hiển thị goal bằng texture riêng.
- Di chuyển block theo đúng orientation.
- Animation lật block.
- Animation rơi khỏi map.
- Kiểm tra thắng/thua.
- Restart level.
- Âm thanh cơ bản.
- Menu chính.
- Chọn level tự động từ thư mục `maps`.
- Chế độ Play và Solve.
- Panel chọn thuật toán.
- Khóa điều khiển tay trong mode Solve.
- Bộ đếm bước và thời gian.
- Cấu trúc để phát lại đường đi của solver.
- BFS, IDS, UCS với cost không đồng đều và A* với heuristic admissible.
- Thống kê search time, peak memory, expanded/generated nodes, peak frontier,
  solution length và solution cost.
- Fragile tile, bridge, soft switch, heavy switch và permanent/toggle behavior.
- Split switch, điều khiển hai cube bằng Space và tự ghép lại khi kề nhau.
- State của solver bao gồm cả cấu hình bridge và cube đang được điều khiển.
- Bảy level mẫu, gồm level cơ bản, từng cơ chế nâng cao và một level kết hợp.
- Bộ kiểm thử logic cho chuyển hướng, biên bản đồ, tile nâng cao và bốn solver.

Chạy kiểm thử:

```bash
python -m unittest discover -s tests -v
```

Xuất dữ liệu thí nghiệm (mặc định đo mỗi cấu hình 5 lần):

```bash
python run_experiments.py
```

Kết quả được ghi vào `output/experiments.csv` để tạo bảng và biểu đồ cho báo cáo.

---

# 18. Ghi chú cuối

README này mô tả kiến trúc và luồng của phiên bản hiện tại. Khi thay đổi tên file, tên class, ký hiệu map hoặc cấu trúc dữ liệu, cần cập nhật README để các thành viên khác không làm việc dựa trên thông tin cũ.

Nên bổ sung thêm ảnh chụp các màn hình sau khi giao diện ổn định:

- Main Menu
- Level Select
- Algorithm Select
- Play Mode
- Solve Mode
- Result Panel
