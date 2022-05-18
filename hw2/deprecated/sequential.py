import mpi4py

from node import Node

mpi4py.rc.recv_mprobe = False
mpi4py.rc.threads = False
from mpi4py import MPI

import sys
import time
from board import Board
import itertools

ILLEGAL_MOVE = 100
NO_WINNER = 101
WINNER = 102

REQUEST_TASK = 201
RECEIVE_TASK = 202
RESULT_PACKAGE = 203


def init_empty_tree(depth):
    root = Node(None)
    root.init_own_children(depth, 1)
    return root


def switch_marker(marker_inner):
    if marker_inner == 1:
        return 2
    return 1


def main():

    if len(sys.argv) != 2:
        print("Please provide depth next time! Assumed = 4", flush=True)
        depth = 4
    else:
        depth = int(sys.argv[1])

    board = Board(6, 7)
    last_move = NO_WINNER
    active = 1
    while last_move != WINNER:
        board.show()
        if active == 1:
            combos = []
            for d in range(1, depth + 1):
                products = list(itertools.product(range(7), repeat=d))
                for p in products:
                    combos.append(list(p))

            root = init_empty_tree(depth)
            root.set_board(board)
            # IZRACUNAT NAJBOLJE POTEZE
            start = time.time()
            while len(combos) > 0:
                board_copy = Board(6, 7)
                board_copy.set_board(board.get_board_deepcopy())
                board_copy.set_col_full(board.get_col_full_deepcopy())

                UID = combos.pop()

                final_results = []
                marker = 1
                for i in range(len(UID)):
                    result = board_copy.play(UID[i], marker)
                    # played_moves.append(UID[i])
                    if result == ILLEGAL_MOVE:
                        while len(final_results) != len(UID):
                            final_results.append(ILLEGAL_MOVE)
                        break
                    elif result == NO_WINNER:
                        final_results.append(0)
                        marker = switch_marker(marker)
                        # kad nema pobjednika
                    else:  # result == WINNER
                        if marker == 1:
                            while len(final_results) != len(UID):
                                final_results.append(+1)
                        else:
                            while len(final_results) != len(UID):
                                final_results.append(-1)
                        break
                root.write_results(final_results, UID)
            end = time.time()
            print(f"All tasks done: {end-start}s")
            root.run_heuristic(0)
            best = -1
            idx = 0
            for i, child in enumerate(root.get_children()):
                print(f'{i}: {child.get_value()}', flush=True)
            for i, child in enumerate(root.get_children()):
                if child.get_value() > best and child.get_value() != ILLEGAL_MOVE:
                    best = child.get_value()
                    idx = i
            print(f"PLAYER 1 PLAYS {idx}")
            last_move = board.play(idx, 1)
            active = 2
        else:
            col = int(input(f"PLAYER 2: "))
            last_move = board.play(col, 2)
            while last_move == ILLEGAL_MOVE:
                print(f"COLUMN FULL\nPICK AGAIN: ")
                col = int(input(f"PLAYER 2: "))
                last_move = board.play(col, 2)
            active = 1
    board.show()
    print(f"WINNER: PLAYER {2 if active == 1 else 1}")


if __name__ == '__main__':
    main()
