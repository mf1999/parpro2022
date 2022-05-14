import mpi4py

mpi4py.rc.recv_mprobe = False
mpi4py.rc.threads = False

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
r = comm.Get_rank()
n = comm.Get_size()

x = np.random.randint(low=1, high=20)
print(f"{r} starting x: {x}", flush=True)

x_min = None

i = 0
comm.barrier()
while i < np.log2(n):
    dest_id = r ^ (2**i)
    if dest_id < n:
        print(f"{r} sending to {dest_id}", flush=True)

        comm.send(x, dest=dest_id) #r XOR 2^i
        x_min = min(x, comm.recv(source=dest_id))

    i += 1
comm.barrier()
print(f"{r} MIN x: {x_min}", flush=True)

