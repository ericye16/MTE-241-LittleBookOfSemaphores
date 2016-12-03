# multiplex

# desired: up to NUM_SIMULTANEOUS "critical point" at once

from sync import Thread, Semaphore, watcher

NUM_SIMULTANEOUS = 3
multiplex = Semaphore(NUM_SIMULTANEOUS)

def child(i):
  print(str(i) + "a")
  multiplex.wait()
  print(str(i) + "critical point")
  multiplex.signal()
  print(str(i) + "c")

watcher()

[Thread(child, i) for i in range(10)]
