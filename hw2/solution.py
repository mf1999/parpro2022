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
    tree = []
    root = Node(None)
    root.init_own_children(depth, 1)
    return root


def play_move(comm, combos, board, root):
    start = time.time()
    while len(combos) > 0:

        received_data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        if isinstance(received_data, int):
            worker_id = received_data

            board_copy = Board(6, 7)
            board_copy.set_board(board.get_board_deepcopy())
            board_copy.set_col_full(board.get_col_full_deepcopy())
            # board_copy.show()
            task_package = [board_copy, 1, combos.pop()]
            comm.send(task_package, dest=worker_id, tag=RECEIVE_TASK)
        else:
            final_results, UID = received_data
            # if final_result != 0:
            #     print(UID, flush=True)
            root.write_results(final_results, UID)

    end = time.time()
    print(f"All tasks done: {end - start}s", flush=True)
    # root.render(0)

    start = time.time()
    print(f"Starting heuristics...", flush=True)
    root.run_heuristic(0)
    end = time.time()
    print(f"Heuristics done: {end - start}s", flush=True)

    best = -1
    idx = 0
    for i, child in enumerate(root.get_children()):
        print(f'{i}: {child.get_value()}', flush=True)
    for i, child in enumerate(root.get_children()):
        if child.get_value() > best and child.get_value() != ILLEGAL_MOVE:
            best = child.get_value()
            idx = i
    print(f"PLAYER 1 PLAYS {idx}")
    return board.play(idx, 1)


def master(comm, rank):
    print("Hello from master node!", flush=True)
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
            last_move = play_move(comm, combos, board, root)
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

    # root.render(0)
    # for c in combos:
    #     print(c)

    # root.render(0)


def worker(comm, rank):
    def switch_marker(marker_inner):
        if marker_inner == 1:
            return 2
        return 1

    print(f"Hello from worker # {rank}", flush=True)

    while True:
        comm.send(rank, dest=0, tag=REQUEST_TASK)

        # while not comm.Iprobe(source=0, tag=RECEIVE_TASK):
        #    pass

        task_package = comm.recv(source=0, tag=RECEIVE_TASK)
        board = task_package[0]
        marker = task_package[1]
        UID = task_package[2]

        final_results = []
        for i in range(len(UID)):
            result = board.play(UID[i], marker)
            # played_moves.append(UID[i])
            if result == ILLEGAL_MOVE:
                while len(final_results) != len(UID):
                    final_results.append(ILLEGAL_MOVE)
                break
            elif result == NO_WINNER:
                final_results.append(0)
                marker = switch_marker(marker)
                # kad nema pobjednika
            else: # result == WINNER
                if marker == 1:
                    while len(final_results) != len(UID):
                        final_results.append(+1)
                else:
                    while len(final_results) != len(UID):
                        final_results.append(-1)
                break

        result_package = [final_results, UID]
        comm.send(result_package, dest=0, tag=RESULT_PACKAGE)


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        master(comm, rank)
    else:
        worker(comm, rank)


if __name__ == '__main__':
    main()
