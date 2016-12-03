# rendezvous

# desired: (a1 and b1) < (a2 and b2)

from sync import Thread, Semaphore, watcher

sem1 = Semaphore(0)
sem2 = Semaphore(0)

def child1():
  print("a1")
  sem1.signal()
  sem2.wait()
  print("a2")

def child2():
  print("b1")
  sem2.signal()
  sem1.wait()
  print("b2")

watcher()

threada = Thread(child1)
threadb = Thread(child2)

