from hw2.board import Board
ILLEGAL_MOVE = 100
NO_WINNER = 101
WINNER = 102

if __name__ == '__main__':
    board = Board(6, 7)
    markers = [1, 2]
    active = 0
    last_move = NO_WINNER
    while last_move != WINNER:
        board.show()
        col = int(input(f"PLAYER {markers[active]}: "))
        last_move = board.play(col, markers[active])
        while last_move == ILLEGAL_MOVE:
            print(f"COLUMN FULL\nPICK AGAIN: ")
            col = int(input(f"PLAYER {markers[active]}: "))
            last_move = board.play(col, markers[active])
        active += 1
        active = active % 2
    board.show()
    print(f"WINNER: PLAYER {markers[active - 1]}")