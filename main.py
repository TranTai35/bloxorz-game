from board import Board
from block import Block
from algorithms.bfs import bfs

import pygame

print(pygame.version.ver)

board = Board("maps/level1.json")


start_block = Block(board.start[0], board.start[1])

result = bfs(board, start_block)

board.print_board()

if result is None:
    print("Không tìm thấy lời giải")
else:
    print("Đã tìm thấy lời giải!")

    path = result.get_path()

    print("Đường đi:", path)
    print("Số bước:", len(path))
    print("Chi phí:", result.cost)