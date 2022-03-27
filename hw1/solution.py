import mpi4py

mpi4py.rc.recv_mprobe = False
mpi4py.rc.threads = False

from mpi4py import MPI
import time
import numpy as np


# Proces(i)
# {	misli (slucajan broj sekundi);					// ispis: mislim
# 		i 'istovremeno' odgovaraj na zahtjeve!			// asinkrono, s povremenom provjerom (vidi nastavak)
# 	dok (nemam obje vilice) {
# 		posalji zahtjev za vilicom;				// ispis: trazim vilicu (i)
# 		ponavljaj {
# 			cekaj poruku (bilo koju!);
# 			ako je poruka odgovor na zahtjev		// dobio vilicu
# 				azuriraj vilice;
# 			inace ako je poruka zahtjev			// drugi traze moju vilicu
# 				obradi zahtjev (odobri ili zabiljezi);
# 		} dok ne dobijes trazenu vilicu;
# 	}
# 	jedi;								// ispis: jedem
# 	odgovori na postojeće zahtjeve;					// ako ih je bilo
# }

class Fork:

    def __init__(self):
        self.state = False
        # True = Clean
        # False = Dirty
        # None = Empty

    def clean(self):
        self.state = True

    def eat(self):
        self.state = False

    def get_state(self):
        return self.state

    def is_dirty(self):
        return self.state == 0

    def is_clean(self):
        return self.state == 1


def init_forks(rank: int, size: int):
    if rank == 0:
        return Fork(), Fork()
    elif rank == size - 1:
        return None, None
    else:
        return None, Fork()


def init_neighbors(rank: int, size: int):
    if rank == 0:
        return size - 1, rank + 1

    elif rank == size - 1:
        return rank - 1, 0

    else:
        return rank - 1, rank + 1


def think():
    global comm
    global rank

    sleep_duration = np.random.randint(1, 6)
    print(f'{" " * rank}Process {rank}: Thinking for {sleep_duration}s!', flush=True)
    for i in range(sleep_duration):
        time.sleep(1.0)
        check_for_requests()


def eat():
    global rank
    global left_fork, right_fork
    print(f'{" " * rank}Process {rank}: eating!', flush=True)
    left_fork.eat()
    right_fork.eat()


def send_requests():
    global comm, rank
    global REQUEST
    global left_fork, right_fork
    global left_neighbor, right_neighbor
    global my_requests

    if left_fork is None and not my_requests[0]:
        comm.send(rank, dest=left_neighbor, tag=REQUEST)
        my_requests[0] = True
        print(f'{" " * rank}Process {rank}: Requesting left fork!', flush=True)
    if right_fork is None and not my_requests[1]:
        comm.send(rank, dest=right_neighbor, tag=REQUEST)
        my_requests[1] = True
        print(f'{" " * rank}Process {rank}: Requesting right fork!', flush=True)


def send_left_fork():
    global left_fork, left_neighbor, RECEIVE

    left_fork.clean()
    print(f'{" " * rank}Process {rank}: SENDING my LEFT FORK!', flush=True)
    comm.send(left_fork, dest=left_neighbor, tag=RECEIVE)
    left_fork = None


def send_right_fork():
    global right_fork, right_neighbor, RECEIVE

    right_fork.clean()
    print(f'{" " * rank}Process {rank}: SENDING my RIGHT FORK!', flush=True)

    comm.send(right_fork, dest=right_neighbor, tag=RECEIVE)
    right_fork = None


def check_for_requests():
    global comm, rank
    global left_neighbor, right_neighbor
    global left_fork, right_fork
    global REQUEST, RECEIVE
    global outstanding_requests

    if comm.Iprobe(source=left_neighbor, tag=REQUEST):
        # print(f'{" " * rank}Process {rank}: got a REQUEST for my LEFT FORK!', flush=True)
        comm.recv(source=left_neighbor, tag=REQUEST)
        if left_fork is not None:
            if left_fork.is_dirty():
                send_left_fork()
            else:
                outstanding_requests[0] = True
        else:
            outstanding_requests[0] = True

    if comm.Iprobe(source=right_neighbor, tag=REQUEST):
        # print(f'{" " * rank}Process {rank}: got a REQUEST for my RIGHT FORK!', flush=True)
        comm.recv(source=right_neighbor, tag=REQUEST)
        if right_fork is not None:
            if right_fork.is_dirty():
                send_right_fork()
            else:
                outstanding_requests[1] = True
        else:
            outstanding_requests[1] = True


def check_for_receive():
    global comm
    global left_neighbor, right_neighbor
    global left_fork, right_fork
    global REQUEST, RECEIVE
    global my_requests

    # print(f'{" " * rank}Process {rank}: checking for left fork!', flush=True)
    if comm.Iprobe(source=left_neighbor, tag=RECEIVE):
        left_fork = comm.recv(source=left_neighbor, tag=RECEIVE)
        my_requests[0] = False
        print(f'{" " * rank}Process {rank}: got my left fork!', flush=True)

    # print(f'{" " * rank}Process {rank}: checking for right fork!', flush=True)
    if comm.Iprobe(source=right_neighbor, tag=RECEIVE):
        right_fork = comm.recv(source=right_neighbor, tag=RECEIVE)
        my_requests[1] = False
        print(f'{" " * rank}Process {rank}: got my right fork!', flush=True)


def deal_with_backlog():
    global outstanding_requests

    if outstanding_requests[0]:
        send_left_fork()
        outstanding_requests[0] = False
    if outstanding_requests[1]:
        send_right_fork()
        outstanding_requests[0] = False


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

REQUEST = 0
RECEIVE = 1

left_fork, right_fork = init_forks(rank, size)
left_neighbor, right_neighbor = init_neighbors(rank, size)
my_requests = [False, False]
outstanding_requests = [False, False]  # left, right

while True:
    think()
    while left_fork is None or right_fork is None:
        send_requests()
        check_for_receive()
        check_for_requests()

    eat()
    deal_with_backlog()
