# mutex

from sync import Thread, Semaphore, watcher

mutex = Semaphore(1)
count = 0

def child1():
  global count
  mutex.wait()
  print("a1")
  count += 1
  mutex.signal()

def child2():
  global count
  mutex.wait()
  print("b1")
  count += 1
  mutex.signal()

watcher()

threada = Thread(child1)
threadb = Thread(child2)

threada.join()
threadb.join()
print(count)