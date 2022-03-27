import numpy
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

randNum = numpy.zeros(1)

if rank == 1:
    randNum = numpy.random.random_sample(1)
    print("Process", rank, "drew the number", randNum[0])
    comm.isend(randNum, dest=0)

if rank == 0:
    print("Process", rank, "before receiving has the number", randNum[0])
    comm.recv(randNum)
    print("Process", rank, "received the number", randNum[0])
