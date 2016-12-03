# reusable barrier2 using two-phase turnstile with pre-loading (less context switching)

from sync import Thread, Semaphore, watcher

N_THREADS = 10
count = 0
mutex = Semaphore(1)
turnstile = Semaphore(0)
turnstile2 = Semaphore(1)

N_LOOPS = 3

def child(i):
  global count
  for l in range(N_LOOPS):
    # phase 1
    print(str(i) + "rendezvous " + str(l))
    mutex.wait()
    count += 1
    if count == N_THREADS:
      turnstile2.wait()
      for j in range(N_THREADS):
        turnstile.signal()
    mutex.signal()
    turnstile.wait()
    print(str(i) + "critical point " + str(l))

    # phase 2
    mutex.wait()
    count -= 1
    if count == 0:
      turnstile.wait()
      for j in range(N_THREADS):
        turnstile2.signal()
    mutex.signal()
    turnstile2.wait()

watcher()

[Thread(child, i) for i in range(N_THREADS)]
