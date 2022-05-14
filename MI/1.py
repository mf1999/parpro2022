import mpi4py

mpi4py.rc.recv_mprobe = False
mpi4py.rc.threads = False

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
r = comm.Get_rank()
n = comm.Get_size()

lx = None
rx = None
x = r

if r == 0:
    rx = comm.recv(source=r+1)
    lx = comm.recv(source=n-1)
    comm.send(x, dest=r+1)
    comm.send(x, dest=n-1)

elif r == n - 1:
    if n % 2 == 0:
        comm.send(x, dest=r-1)
        lx = comm.recv(source=r-1)
        comm.send(x, dest=0)
        rx = comm.recv(source=0)
    else:
        lx = comm.recv(source=r-1)
        comm.send(x, dest=0)
        comm.send(x, dest=r-1)
        rx = comm.recv(source=0)

elif r % 2 == 1:
    comm.send(x, dest=r+1)
    comm.send(x, dest=r-1)
    lx = comm.recv(source=r-1)
    rx = comm.recv(source=r+1)

elif r % 2 == 0:
    lx = comm.recv(source=r-1)
    rx = comm.recv(source=r+1)
    comm.send(x, dest=r+1)
    comm.send(x, dest=r-1)

print(f"{r}: {lx} {x} {rx}", flush=True)


