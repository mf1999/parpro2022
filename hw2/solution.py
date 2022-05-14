import mpi4py

from node import Node

mpi4py.rc.recv_mprobe = False
mpi4py.rc.threads = False
from mpi4py import MPI

import sys
import time
from board import Board
from itertools import product

ILLEGAL_MOVE = 100
NO_WINNER = 101
WINNER = 102

REQUEST_TASK = 201
RECEIVE_TASK = 202


def init_empty_tree(depth):
    tree = []
    root = Node(None)
    root.init_own_children(depth, 1)
    return root


def master(comm, rank):
    print("Hello from master node!", flush=True)
    if len(sys.argv) != 2:
        print("Please provide depth next time! Assumed = 4", flush=True)
        depth = 4
    else:
        depth = int(sys.argv[1])

    board = Board(6, 7)
    root = init_empty_tree(depth)
    root.set_board(board)
    combinations = product(range(7), repeat=depth)
    for UID in combinations:
        task_package = [board.get_deepcopy(), ]


def worker(comm, rank):
    rank = comm.Get_rank()
    print(f"Hello from worker # {rank}", flush=True)

    while True:
        comm.isend(None, dest=0, tag=REQUEST_TASK)

        while not comm.Iprobe(source=0, tag=RECEIVE_TASK):
            pass

        task_package = comm.recv(source=0, tag=RECEIVE_TASK)
        board = Board(task_package[0])
        col = task_package[1]
        marker = task_package[2]
        UID = task_package[3]

        result = board.play(col, marker)

        result_package = [board, result, UID]
        comm.isend(result_package, dest=0)


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        master(comm, rank)
    else:
        worker(comm, rank)


if __name__ == '__main__':
    main()
