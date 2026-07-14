from ursina import (
    Entity,
    Text,
    Button,
    camera,
    window,
    color,
    Sky,
    invoke,
    destroy
)

from board import Board
from block import Block
from game.renderer import Renderer
from game.block_renderer import BlockRenderer
from game.audio_manager import AudioManager
from game.camera_controller import setup_camera
import time
from algorithms.solver import solve


class Game(Entity):
    def __init__(self,level_path,mode="play",algorithm=None,on_back=None):
        super().__init__()

        # Thông tin scene
        self.level_path = level_path
        self.mode = mode
        self.algorithm = algorithm
        self.on_back = on_back

        # Trạng thái game
        self.move_count = 0
        self.is_moving = False
        self.has_won = False
        self.has_lost = False

        # Trạng thái solver
        self.search_result = None
        self.solution_moves = []
        self.solution_index = 0
        self.is_solving = False

        # Đo thời gian từ khi vào scene game
        self.scene_start_time = time.perf_counter()
        self.total_time = 0.0

        self.world_root = Entity(parent=self)

        # Root chứa toàn bộ UI của Game
        # Bắt buộc phải tạo trước create_ui()
        self.ui_root = Entity(parent=camera.ui)

        window.color = color.rgb(35, 45, 60)

        # Đọc level
        self.board = Board(level_path)

        # Nền
        self.background = Sky(
            parent=self.world_root,
            texture="assets/sprites/background.jpg"
        )
            
        
        # Tạo map
        self.renderer = Renderer(
            self.board,
            parent=self.world_root
        )
        self.renderer.create_map()

        # Tạo block logic
        self.block_logic = Block(
            self.board.start[0],
            self.board.start[1]
        )

        # Tạo block hiển thị
        self.block_renderer = BlockRenderer(
            self.block_logic,
            parent=self.world_root
        )

        # Camera
        setup_camera(self.board)

        # Âm thanh
        self.audio_manager = AudioManager()

        # UI
        self.create_ui()

        # Chế độ solver tự chạy sau khi scene tạo xong
        if self.mode == "solve":
            invoke(self.start_solver, delay=0.3)

    def start_solver(self):
        if self.mode != "solve":
            return

        if self.algorithm is None:
            self.show_solver_error(
                "Chưa chọn thuật toán"
            )
            return

        if self.is_moving or self.has_won or self.has_lost:
            return

        try:
            self.search_result = solve(
                board=self.board,
                start_block=self.block_logic.copy(),
                algorithm_name=self.algorithm
            )

        except ValueError as error:
            print(error)
            self.show_solver_error(str(error))
            return

        except Exception as error:
            print("Solver error:", error)
            self.show_solver_error(str(error))
            return

        print(self.search_result)

        if not self.search_result.found:
            self.show_no_solution()
            return

        self.solution_moves = list(
            self.search_result.path
        )
        self.solution_index = 0
        self.is_solving = True

        if len(self.solution_moves) == 0:
            if self.board.is_win(self.block_logic):
                self.show_win()
            else:
                self.show_no_solution()

            return

        self.play_next_solution_move()

    def play_next_solution_move(self):
        if not self.is_solving:
            return

        if self.is_moving:
            return

        if self.solution_index >= len(self.solution_moves):
            self.is_solving = False

            if self.board.is_win(self.block_logic):
                self.show_win()
            else:
                self.show_no_solution()

            return

        direction = self.solution_moves[self.solution_index]

        self.solution_index += 1

        self.try_move(direction)


    def update(self):
        if self.has_won or self.has_lost:
            return

        self.total_time = (
            time.perf_counter() - self.scene_start_time
        )

        self.timer_text.text = (
            f"Time: {self.total_time:.2f}s"
        )

    def input(self, key):
        if key == "m":
            self.audio_manager.toggle_music()
            return

        if key == "escape":
            self.back_to_level_select()
            return

        if key == "r":
            self.restart()
            return

        # Người chơi không được dùng WASD trong chế độ Solve
        if self.mode == "solve":
            return

        if self.is_moving or self.has_won or self.has_lost:
            return

        key_to_direction = {
            "w": "UP",
            "s": "DOWN",
            "a": "LEFT",
            "d": "RIGHT"
        }

        if key in key_to_direction:
            self.try_move(key_to_direction[key])

    def try_move(self, direction):
        if self.is_moving or self.has_won or self.has_lost:
            return

        old_block = self.block_logic

        new_block = self.block_logic.copy()
        new_block.move(direction)

        self.is_moving = True

        if self.board.is_valid_block(new_block):
            # Nước đi hợp lệ
            self.block_renderer.animate_move(
                old_block=old_block,
                new_block=new_block,
                direction=direction,
                on_complete=lambda: self.finish_move(new_block)
            )

        else:
            # Nước đi không hợp lệ:
            # vẫn cho block lật trước, rồi mới rơi
            self.block_renderer.animate_move(
                old_block=old_block,
                new_block=new_block,
                direction=direction,
                on_complete=lambda: self.start_fall( new_block,direction)
            )


    def finish_move(self, new_block):
        self.block_logic = new_block

        self.block_renderer.block_logic = new_block
        self.block_renderer.update_transform()

        self.is_moving = False

        self.audio_manager.play_move_sound()

        self.move_count += 1
        self.move_text.text = (
            f"Moves: {self.move_count}"
        )

        if self.board.is_win(self.block_logic):
            self.is_solving = False
            self.show_win()
            return

        if self.mode == "solve" and self.is_solving:
            invoke(
                self.play_next_solution_move,
                delay=0.15
            )

    

    def start_fall(self, invalid_block, direction):
        self.block_logic = invalid_block
        self.block_renderer.block_logic = invalid_block

        self.move_count += 1
        self.move_text.text = f"Moves: {self.move_count}"

        supported_cells = []

        for row, col in invalid_block.get_cells():
            if self.board.is_floor(row, col):
                supported_cells.append((row, col))

        if len(supported_cells) == 1:
            # Một phần block còn nằm trên ô rìa:
            # chổng đuôi lên rồi mới rơi.
            self.block_renderer.animate_edge_tip_and_fall(
                supported_cell=supported_cells[0],
                direction=direction,
                on_complete=self.show_lose
            )

        else:
            # Không còn ô nào đỡ block thì rơi thẳng.
            self.block_renderer.animate_fall(
                on_complete=self.show_lose
            )
        

    def create_ui(self):
        self.move_text = Text(
            text="Moves: 0",
            parent=self.ui_root,
            position=(-0.85, 0.45),
            scale=1.2
        )

        self.timer_text = Text(
            text="Time: 0.00s",
            parent=self.ui_root,
            position=(-0.85, 0.39),
            scale=1.2
        )

        if self.mode == "solve":
            self.algorithm_text = Text(
                text=f"Algorithm: {self.algorithm}",
                parent=self.ui_root,
                position=(-0.85, 0.33),
                scale=1.2
            )
        else:
            self.algorithm_text = None

        self.back_button = Button(
            text="Back",
            parent=self.ui_root,
            position=(-0.82, -0.43),
            scale=(0.18, 0.07),
            on_click=self.back_to_level_select
        )

        self.win_lose_panel = Entity(
            parent=self.ui_root,
            model="quad",
            color=color.rgba(0, 0, 0, 210),
            scale=(0.78, 0.68),
            enabled=False
        )

        self.win_lose_text = Text(
            text="",
            parent=self.win_lose_panel,
            origin=(0, 0),
            position=(0, 0.23, -0.01),
            scale=1.4,
            color=color.white
        )

        self.restart_button = Button(
            text="Restart",
            parent=self.win_lose_panel,
            position=(-0.18, -0.25, -0.01),
            scale=(0.25, 0.09),
            on_click=self.restart
        )

        self.result_back_button = Button(
            text="Level Select",
            parent=self.win_lose_panel,
            position=(0.18, -0.25, -0.01),
            scale=(0.25, 0.09),
            on_click=self.back_to_level_select
        )

    def show_win(self):
        if self.has_won:
            return

        self.is_moving = False
        self.is_solving = False
        self.has_won = True

        self.total_time = (
            time.perf_counter() - self.scene_start_time
        )

        self.win_lose_panel.enabled = True
        self.win_lose_text.color = color.white

        if self.mode == "solve" and self.search_result is not None:
            self.win_lose_text.text = (
                "SOLVED!\n\n"
                f"Algorithm: {self.algorithm}\n"
                f"Moves: {self.move_count}\n"
                f"Expanded: "
                f"{self.search_result.expanded_nodes}\n"
                f"Search time: "
                f"{self.search_result.search_time:.6f}s\n"
                f"Total time: {self.total_time:.2f}s"
            )

        else:
            self.win_lose_text.text = (
                "YOU WIN!\n\n"
                f"Moves: {self.move_count}\n"
                f"Time: {self.total_time:.2f}s"
            )
    
    def show_lose(self):
        self.is_moving = False
        self.is_solving = False
        self.has_lost = True

        self.total_time = (
            time.perf_counter() - self.scene_start_time
        )

        self.win_lose_panel.enabled = True
        self.win_lose_text.color = color.red

        self.win_lose_text.text = (
            "YOU LOSE!\n\n"
            f"Moves: {self.move_count}\n"
            f"Time: {self.total_time:.2f}s"
        )

    def show_no_solution(self):
        self.is_moving = False
        self.is_solving = False
        self.has_lost = True

        self.total_time = (
            time.perf_counter() - self.scene_start_time
        )

        self.win_lose_panel.enabled = True
        self.win_lose_text.color = color.red

        expanded_nodes = 0
        search_time = 0.0

        if self.search_result is not None:
            expanded_nodes = self.search_result.expanded_nodes
            search_time = self.search_result.search_time

        self.win_lose_text.text = (
            "NO SOLUTION!\n\n"
            f"Algorithm: {self.algorithm}\n"
            f"Expanded: {expanded_nodes}\n"
            f"Search time: {search_time:.6f}s"
        )
    
    def show_solver_error(self, message):
        self.is_moving = False
        self.is_solving = False
        self.has_lost = True

        self.win_lose_panel.enabled = True
        self.win_lose_text.color = color.red

        self.win_lose_text.text = (
            "SOLVER ERROR!\n\n"
            f"{message}"
        )

    def back_to_level_select(self):
        if self.is_moving:
            return

        self.is_solving = False

        if self.on_back is not None:
            self.on_back()


    def restart(self):
        if self.is_moving:
            return

        self.block_logic = Block(
            self.board.start[0],
            self.board.start[1]
        )

        self.block_renderer.block_logic = self.block_logic
        self.block_renderer.update_transform()

        self.move_count = 0

        self.is_moving = False
        self.is_solving = False
        self.has_won = False
        self.has_lost = False

        self.solution_moves = []
        self.solution_index = 0
        self.search_result = None

        self.scene_start_time = time.perf_counter()
        self.total_time = 0.0

        self.move_text.text = "Moves: 0"
        self.timer_text.text = "Time: 0.00s"

        self.win_lose_panel.enabled = False
        self.win_lose_text.text = ""
        self.win_lose_text.color = color.white

        if self.mode == "solve":
            invoke(self.start_solver, delay=0.3)

        print("Game restarted")
    
    def on_destroy(self):
        self.is_solving = False

        if hasattr(self, "ui_root"):
            destroy(self.ui_root)