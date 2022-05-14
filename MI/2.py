import mpi4py

mpi4py.rc.recv_mprobe = False
mpi4py.rc.threads = False

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
r = comm.Get_rank()
n = comm.Get_size()

x = np.random.randint(low=1, high=20)
x_max = None
print(f"{r} original x: {x}")

if r == 0:
    comm.send(x, dest=r+1)
    x_max = comm.recv(source=r+1)

elif r == n-1:
    x_max = max(x, comm.recv(source=r-1))
    comm.send(x_max, dest=r-1)

else:
    x_max = max(x, comm.recv(source=r-1))
    comm.send(x_max, dest=r+1)
    x_max = comm.recv(source=r+1)
    comm.send(x_max, dest=r-1)


print(f"{r} MAX x: {x_max}")
