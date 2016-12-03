# reusable barrier2 using two-phase turnstile with pre-loading (less context switching)

# desired: (all rendezvous 0) < (all critical point 0) < (all rendezvous 1) < (all critical point 1) 
# < ... (all rendezvous N_LOOPS - 1) < (all critical point N_LOOPS - 1)

from sync import Thread, Semaphore, watcher
from BarrierObj import Barrier

N_THREADS = 10
barrier = Barrier(N_THREADS)

N_LOOPS = 3

def child(i):
  for l in range(N_LOOPS):
    # phase 1
    print(str(i) + "rendezvous " + str(l))
    barrier.phase1()
    print(str(i) + "critical point " + str(l))
    barrier.phase2()

watcher()

[Thread(child, i) for i in range(N_THREADS)]
