import time

from ursina import Button, Entity, Sky, Text, camera, color, destroy, invoke, window

from algorithms.solver import solve
from block import Block, Orientation
from board import Board
from game.audio_manager import AudioManager
from game.block_renderer import BlockRenderer
from game.camera_controller import setup_camera
from game.renderer import Renderer


class Game(Entity):
    def __init__(self, level_path, mode="play", algorithm=None, on_back=None):
        super().__init__()
        self.level_path = level_path
        self.mode = mode
        self.algorithm = algorithm
        self.on_back = on_back

        self.move_count = 0
        self.is_moving = False
        self.has_won = False
        self.has_lost = False
        self.search_result = None
        self.solution_moves = []
        self.solution_index = 0
        self.is_solving = False
        self.scene_start_time = time.perf_counter()
        self.total_time = 0.0

        self.world_root = Entity(parent=self)
        self.ui_root = Entity(parent=camera.ui)
        window.color = color.rgb(35, 45, 60)

        self.board = Board(level_path)
        self.bridge_states = self.board.initial_bridge_states
        self.background = Sky(
            parent=self.world_root,
            texture="assets/sprites/background.jpg",
        )

        self.renderer = Renderer(self.board, parent=self.world_root)
        self.renderer.create_map()
        self.block_logic = Block(*self.board.start)
        self.block_renderer = BlockRenderer(self.block_logic, parent=self.world_root)
        setup_camera(self.board)
        self.audio_manager = AudioManager(parent=self.world_root)
        self.create_ui()

        if self.mode == "solve":
            invoke(self.start_solver, delay=0.3)

    def start_solver(self):
        if self.mode != "solve":
            return
        if self.algorithm is None:
            self.show_solver_error("Chưa chọn thuật toán")
            return
        if self.is_moving or self.has_won or self.has_lost:
            return

        try:
            self.search_result = solve(
                board=self.board,
                start_block=self.block_logic.copy(),
                algorithm_name=self.algorithm,
                start_bridge_states=self.bridge_states,
            )
        except (ValueError, RuntimeError) as error:
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

        self.solution_moves = list(self.search_result.path)
        self.solution_index = 0
        self.is_solving = True
        if not self.solution_moves:
            if self.board.is_win(self.block_logic):
                self.show_win()
            else:
                self.show_no_solution()
            return
        self.play_next_solution_move()

    def play_next_solution_move(self):
        if not self.is_solving or self.is_moving:
            return
        if self.solution_index >= len(self.solution_moves):
            self.is_solving = False
            if self.board.is_win(self.block_logic):
                self.show_win()
            else:
                self.show_no_solution()
            return

        action = self.solution_moves[self.solution_index]
        self.solution_index += 1
        self.try_move(action)

    def update(self):
        if self.has_won or self.has_lost:
            return
        self.total_time = time.perf_counter() - self.scene_start_time
        self.timer_text.text = f"Time: {self.total_time:.2f}s"

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
        if self.mode == "solve" or self.is_moving or self.has_won or self.has_lost:
            return

        key_to_action = {
            "w": "UP",
            "s": "DOWN",
            "a": "LEFT",
            "d": "RIGHT",
        }
        if key == "space" and self.block_logic.is_split:
            self.try_move("SWITCH")
        elif key in key_to_action:
            self.try_move(key_to_action[key])

    def try_move(self, action):
        if self.is_moving or self.has_won or self.has_lost:
            return

        old_block = self.block_logic
        try:
            transition = self.board.transition(
                old_block,
                self.bridge_states,
                action,
            )
        except ValueError as error:
            self.show_solver_error(str(error))
            return

        self.is_moving = True
        if transition.valid:
            self.block_renderer.animate_move(
                old_block=old_block,
                new_block=transition.block,
                direction=action,
                on_complete=lambda: self.finish_move(transition),
            )
        else:
            self.block_renderer.animate_move(
                old_block=old_block,
                new_block=transition.block,
                direction=action,
                on_complete=lambda: self.start_fall(transition, action),
            )

    def finish_move(self, transition):
        self.block_logic = transition.block
        self.bridge_states = transition.bridge_states
        self.block_renderer.block_logic = self.block_logic
        self.block_renderer.update_transform()
        self.renderer.refresh_bridge_states(self.bridge_states)
        self.is_moving = False
        self.audio_manager.play_move_sound()
        self.move_count += 1
        self.move_text.text = f"Moves: {self.move_count}"

        if self.board.is_win(self.block_logic):
            self.is_solving = False
            self.show_win()
            return
        if self.mode == "solve" and self.is_solving:
            invoke(self.play_next_solution_move, delay=0.15)

    def start_fall(self, transition, direction):
        invalid_block = transition.block
        self.block_logic = invalid_block
        self.bridge_states = transition.bridge_states
        self.block_renderer.block_logic = invalid_block
        self.renderer.refresh_bridge_states(self.bridge_states)
        self.move_count += 1
        self.move_text.text = f"Moves: {self.move_count}"

        supported_cells = [
            cell
            for cell in invalid_block.get_cells()
            if self.board.is_floor(*cell, self.bridge_states)
        ]

        if invalid_block.orientation == Orientation.SPLIT:
            self.block_renderer.animate_split_fall(
                supported_cells=supported_cells,
                on_complete=self.show_lose,
            )
        elif (
            len(supported_cells) == 1
            and not (
                invalid_block.orientation == Orientation.STANDING
                and self.board.is_fragile(*invalid_block.pos1)
            )
        ):
            self.block_renderer.animate_edge_tip_and_fall(
                supported_cell=supported_cells[0],
                direction=direction,
                on_complete=self.show_lose,
            )
        else:
            self.block_renderer.animate_fall(on_complete=self.show_lose)

    def create_ui(self):
        self.move_text = Text(
            text="Moves: 0",
            parent=self.ui_root,
            position=(-0.85, 0.45),
            scale=1.2,
        )
        self.timer_text = Text(
            text="Time: 0.00s",
            parent=self.ui_root,
            position=(-0.85, 0.39),
            scale=1.2,
        )
        self.algorithm_text = None
        if self.mode == "solve":
            self.algorithm_text = Text(
                text=f"Algorithm: {self.algorithm}",
                parent=self.ui_root,
                position=(-0.85, 0.33),
                scale=1.2,
            )

        controls = "WASD: Roll | R: Restart | M: Music | Esc: Back"
        if self.mode == "play":
            controls += " | Space: Switch cube"
        self.controls_text = Text(
            text=controls,
            parent=self.ui_root,
            origin=(0, 0),
            position=(0, -0.47),
            scale=0.8,
        )
        self.back_button = Button(
            text="Back",
            parent=self.ui_root,
            position=(-0.82, -0.40),
            scale=(0.18, 0.07),
            on_click=self.back_to_level_select,
        )

        self.win_lose_panel = Entity(
            parent=self.ui_root,
            model="quad",
            color=color.rgba(0, 0, 0, 220),
            scale=(0.82, 0.78),
            enabled=False,
        )
        self.win_lose_text = Text(
            text="",
            parent=self.win_lose_panel,
            origin=(0, 0),
            position=(0, 0.25, -0.01),
            scale=1.15,
            color=color.white,
        )
        self.restart_button = Button(
            text="Restart",
            parent=self.win_lose_panel,
            position=(-0.18, -0.31, -0.01),
            scale=(0.25, 0.09),
            on_click=self.restart,
        )
        self.result_back_button = Button(
            text="Level Select",
            parent=self.win_lose_panel,
            position=(0.18, -0.31, -0.01),
            scale=(0.25, 0.09),
            on_click=self.back_to_level_select,
        )

    def show_win(self):
        if self.has_won:
            return
        self.is_moving = False
        self.is_solving = False
        self.has_won = True
        self.total_time = time.perf_counter() - self.scene_start_time
        self.win_lose_panel.enabled = True
        self.win_lose_text.color = color.white

        if self.mode == "solve" and self.search_result is not None:
            result = self.search_result
            self.win_lose_text.text = (
                "SOLVED!\n\n"
                f"Algorithm: {self.algorithm}\n"
                f"Solution length: {result.steps}\n"
                f"Solution cost: {result.solution_cost:.2f}\n"
                f"Expanded / Generated: {result.expanded_nodes} / {result.generated_nodes}\n"
                f"Peak frontier: {result.peak_frontier}\n"
                f"Peak memory: {result.memory_usage_mb:.3f} MB\n"
                f"Search time: {result.search_time:.6f}s\n"
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
        self.total_time = time.perf_counter() - self.scene_start_time
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
        self.total_time = time.perf_counter() - self.scene_start_time
        self.win_lose_panel.enabled = True
        self.win_lose_text.color = color.red
        result = self.search_result
        self.win_lose_text.text = (
            "NO SOLUTION!\n\n"
            f"Algorithm: {self.algorithm}\n"
            f"Expanded: {result.expanded_nodes if result else 0}\n"
            f"Peak memory: {result.memory_usage_mb if result else 0.0:.3f} MB\n"
            f"Search time: {result.search_time if result else 0.0:.6f}s"
        )

    def show_solver_error(self, message):
        self.is_moving = False
        self.is_solving = False
        self.has_lost = True
        self.win_lose_panel.enabled = True
        self.win_lose_text.color = color.red
        self.win_lose_text.text = f"SOLVER ERROR!\n\n{message}"

    def back_to_level_select(self):
        if self.is_moving:
            return
        self.is_solving = False
        if self.on_back is not None:
            self.on_back()

    def restart(self):
        if self.is_moving:
            return
        self.block_logic = Block(*self.board.start)
        self.bridge_states = self.board.initial_bridge_states
        self.block_renderer.block_logic = self.block_logic
        self.block_renderer.update_transform()
        self.renderer.refresh_bridge_states(self.bridge_states)

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

    def on_destroy(self):
        self.is_solving = False
        if hasattr(self, "ui_root"):
            destroy(self.ui_root)
