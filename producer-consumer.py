# producer-consumer

# desired: producer sends an event every so often
# if nothing is in the queue consumer should wait

from sync import Thread, Semaphore, watcher
import time, random
from collections import deque

mutex = Semaphore(1)
items = Semaphore(0)
buffer = deque()

class Event:
  def __init__(self, x):
    self.x = x

def producer():
  global buffer
  i = 0
  while True:
    time.sleep(random.random() * 5)
    event = Event(i)
    print("Producing event %d!" % event.x)
    mutex.wait()
    buffer.append(event)
    mutex.signal()
    items.signal()
    i += 1

def consumer():
  global buffer
  while True:
    items.wait()
    mutex.wait()
    event = buffer.popleft()
    mutex.signal()
    print("Consuming event %d!" % event.x)
    time.sleep(random.random() * 3)
    print("Finished consuming event %d!" % event.x)


watcher()

Thread(producer)
Thread(consumer)
