# deadlock

from sync import Thread, Semaphore, watcher

sem1 = Semaphore(0)
sem2 = Semaphore(0)

def child1():
  print("a1")
  sem2.wait()
  sem1.signal()
  print("a2")

def child2():
  print("b1")
  sem1.wait()
  sem2.signal()
  print("b2")

watcher()

threada = Thread(child1)
threadb = Thread(child2)

