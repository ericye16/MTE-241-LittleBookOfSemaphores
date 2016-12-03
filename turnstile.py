# turnstile

# desired: (all rendezvous) < (all critical points)

from sync import Thread, Semaphore, watcher

N_THREADS = 10
count = 0
mutex = Semaphore(1)
turnstile = Semaphore(0)

def child(i):
  global count
  print(str(i) + "rendezvous")
  mutex.wait()
  count += 1
  mutex.signal()
  if count == N_THREADS:
    turnstile.signal()
  turnstile.wait()
  turnstile.signal()
  print(str(i) + "critical point")

  # note that the turnstile is _not_ ready to go again: it has a value of 1

watcher()

[Thread(child, i) for i in range(N_THREADS)]
