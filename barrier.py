# barrier

# suboptimal because the last task probably is the lowest-priority task, so this involves a lot of context switches
from sync import Thread, Semaphore, watcher

N_THREADS = 10
count = 0
mutex = Semaphore(1)
barrier = Semaphore(0)

def child(i):
  global count
  print(str(i) + "rendezvous")
  mutex.wait()
  count += 1
  if count == N_THREADS:
    for j in range(N_THREADS):
      barrier.signal()
  mutex.signal()
  barrier.wait()
  print(str(i) + "critical point")

  # note that the barrier is ready to go again

watcher()

[Thread(child, i) for i in range(N_THREADS)]
