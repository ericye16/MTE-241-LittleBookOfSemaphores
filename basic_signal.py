from sync import Thread, Semaphore, watcher

sem = Semaphore(0)

def child1():
  sem.wait()
  print("child a")

def child2():
  print("child b")
  sem.signal()

watcher()

threada = Thread(child1)
threadb = Thread(child2)

