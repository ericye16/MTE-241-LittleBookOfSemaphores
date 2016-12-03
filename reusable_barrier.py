# reusable barrier using two-phase turnstile

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
    mutex.signal()
    if count == N_THREADS:
      turnstile.signal()
      turnstile2.wait()
    turnstile.wait()
    turnstile.signal()
    print(str(i) + "critical point " + str(l))

    # phase 2
    mutex.wait()
    count -= 1
    mutex.signal()
    if count == 0:
      turnstile2.signal()
      turnstile.wait()
    turnstile2.wait()
    turnstile2.signal()

watcher()

[Thread(child, i) for i in range(N_THREADS)]
