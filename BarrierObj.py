# reusable barrier2 using two-phase turnstile with pre-loading (less context switching)

from sync import Thread, Semaphore, watcher

class Barrier:
  def __init__(self, n):
    self.N_THREADS = n
    self.count = 0
    self.mutex = Semaphore(1)
    self.turnstile = Semaphore(0)
    self.turnstile2 = Semaphore(1)

  def phase1(self):
    self.mutex.wait()
    self.count += 1
    if count == N_THREADS:
      self.turnstile2.wait()
      for j in range(N_THREADS):
        self.turnstile.signal()
    self.mutex.signal()
    self.turnstile.wait()

  def phase1(self):
    self.mutex.wait()
    self.count -= 1
    if count == 0:
      self.turnstile.wait()
      for j in range(N_THREADS):
        self.turnstile2.signal()
    self.mutex.signal()
    self.turnstile2.wait()

  def wait(self):
    self.phase1()
    self.phase2()