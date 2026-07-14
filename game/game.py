from ursina import Entity, Text, Button, camera, color

from board import Board
from block import Block
from game.renderer import Renderer
from game.block_renderer import BlockRenderer
from game.audio_manager import AudioManager
from game.camera_controller import setup_camera


class Game(Entity):
    def __init__(self, level_path):
        super().__init__()

        #lấy ma trận từ board
        self.board = Board(level_path)

        #xây ui map
        self.renderer = Renderer(self.board)
        self.renderer.create_map()

        #nhận vị trí bắt đầu
        self.block_logic = Block(
            self.board.start[0],
            self.board.start[1]
        )
        
        #hiện block cho giao diện game
        self.block_renderer = BlockRenderer(self.block_logic)
           
        #set up góc nhìn
        setup_camera(self.board)

        #quản lí âm thanh
        self.audio_manager = AudioManager()

        #bộ đếm bước di chuyển
        self.move_count = 0
        
        #tạo ui 
        self.create_ui()

        self.is_moving = False
        self.has_won = False




    def input(self, key):
        if key == "m":
            self.audio_manager.toggle_music()
            return

        if key == "r":
            self.restart()
            return

        if self.is_moving or self.has_won:
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
        if self.is_moving:
            return

        old_block = self.block_logic

        new_block = self.block_logic.copy()
        new_block.move(direction)

        if not self.board.is_valid_block(new_block):
            print("Nước đi không hợp lệ")
            return

        self.is_moving = True

        self.block_renderer.animate_move(
            old_block=old_block,
            new_block=new_block,
            direction=direction,
            on_complete=lambda: self.finish_move(new_block)
        )


    def finish_move(self, new_block):
        self.block_logic = new_block

        self.block_renderer.block_logic = new_block
        self.block_renderer.update_transform()

        self.is_moving = False

        print(self.block_logic)

        self.audio_manager.play_move_sound()

        self.move_count += 1
        self.move_text.text = f"Moves: {self.move_count}"

        if self.board.is_win(self.block_logic):
            self.show_win()

    def create_ui(self):
        self.move_text = Text(
            text="Moves: 0",
            parent=camera.ui,
            position=(-0.85, 0.45),
            scale=1.2
        )

        self.win_panel = Entity(
            parent=camera.ui,
            model="quad",
            color=color.rgba(0, 0, 0, 180),
            scale=(0.65, 0.35),
            enabled=False
        )

        self.win_text = Text(
            text="YOU WIN!",
            parent=self.win_panel,
            origin=(0, 0),
            position=(0, 0.12, -0.01),
            scale=2,
            color=color.white
        )

        self.restart_button = Button(
            text="Restart",
            parent=self.win_panel,
            scale=(0.3, 0.18),
            y=-0.12,
            on_click=self.restart
        )

    def show_win(self):
        self.has_won = True
        self.win_panel.enabled = True

        self.win_text.text = (
            "YOU WIN!\n"
            f"Moves: {self.move_count}"
        )
    
    def restart(self):
        self.block_logic = Block(
            self.board.start[0],
            self.board.start[1]
        )

        self.block_renderer.block_logic = self.block_logic
        self.block_renderer.update_transform()

        self.move_count = 0
        self.has_won = False
        self.is_moving = False

        self.move_text.text = "Moves: 0"
        self.win_panel.enabled = False

        print("Game restarted")