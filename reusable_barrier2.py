# reusable barrier2 using two-phase turnstile with pre-loading (less context switching)

# desired: (all rendezvous 0) < (all critical point 0) < (all rendezvous 1) < (all critical point 1) 
# < ... (all rendezvous N_LOOPS - 1) < (all critical point N_LOOPS - 1)

from sync import Thread, Semaphore, watcher
import time, random

N_THREADS = 10
count = 0
mutex = Semaphore(1)
turnstile = Semaphore(0)
turnstile2 = Semaphore(0)

N_LOOPS = 3

def child(i):
  global count
  for l in range(N_LOOPS):
    # phase 1
    time.sleep(random.random() * 5)
    print(str(i) + "rendezvous " + str(l))
    mutex.wait()
    count += 1
    if count == N_THREADS:
      for j in range(N_THREADS):
        turnstile.signal()
    mutex.signal()
    turnstile.wait()
    print(str(i) + "critical point " + str(l))

    # phase 2
    mutex.wait()
    count -= 1
    if count == 0:
      for j in range(N_THREADS):
        turnstile2.signal()
    mutex.signal()
    turnstile2.wait()

watcher()

[Thread(child, i) for i in range(N_THREADS)]
