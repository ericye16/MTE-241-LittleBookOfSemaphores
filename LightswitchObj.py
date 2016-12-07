# LightSwitch obj

from sync import Thread, Semaphore, watcher

class LightswitchObj:
  def __init__(self):
    self.count = 0
    self.mutex = Semaphore(1)

  def lock(self, semaphore):
    self.mutex.wait()
    self.count += 1
    if self.count == 1:
      semaphore.wait()
    self.mutex.signal()

  def unlock(self, semaphore):
    self.mutex.wait()
    self.count -= 1
    if self.count == 0:
      semaphore.signal()
    self.mutex.signal()