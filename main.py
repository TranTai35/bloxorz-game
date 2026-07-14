# from board import Board
# from block import Block
# from algorithms.bfs import bfs

# import pygame

# print(pygame.version.ver)

# board = Board("maps/level1.json")


# start_block = Block(board.start[0], board.start[1])

# result = bfs(board, start_block)

# board.print_board()

# if result is None:
#     print("Không tìm thấy lời giải")
# else:
#     print("Đã tìm thấy lời giải!")

#     path = result.get_path()

#     print("Đường đi:", path)
#     print("Số bước:", len(path))
#     print("Chi phí:", result.cost)

from board import Board
from block import Block

board = Board("maps/level1.json")
block = Block(board.start[0], board.start[1])

board.print_board()

while not board.is_win(block):

    print("\n----------------")
    print(block)

    move = input("Move (W/A/S/D): ").upper()

    if move == "W":
        direction = "UP"
    elif move == "S":
        direction = "DOWN"
    elif move == "A":
        direction = "LEFT"
    elif move == "D":
        direction = "RIGHT"
    else:
        print("Phím không hợp lệ!")
        continue

    new_block = block.copy()
    new_block.move(direction)

    if board.is_valid_block(new_block):
        block = new_block
    else:
        print("Không thể đi hướng đó!")

print("\nChúc mừng, bạn đã thắng!")