import mpi4py

mpi4py.rc.recv_mprobe = False
mpi4py.rc.threads = False

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
r = comm.Get_rank()
n = comm.Get_size()

if r == 0:
    print(f"{r} waiting.", flush=True)
    for i in range(n-1):
        comm.recv(source=MPI.ANY_SOURCE)
    for i in range(1, n):
        comm.send(None, dest=i)

else:
    print(f"{r} waiting.", flush=True)
    comm.send(None, dest=0)
    comm.recv(source=0)

print(f"{r} continuing", flush=True)