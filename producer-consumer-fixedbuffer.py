# producer-consumer with fixed buffer size

# desired: producer sends an event every so often
# if nothing is in the queue consumer should wait
# block on the producer side if we're out of buffer spaces

from sync import Thread, Semaphore, watcher
import time, random
from collections import deque

BUFFER_SIZE = 3

mutex = Semaphore(1)
items = Semaphore(0)
spaces = Semaphore(BUFFER_SIZE)
buffer = deque()

t0 = time.time()

class Event:
  def __init__(self, x):
    self.x = x

def producer():
  global buffer
  i = 0
  while True:
    time.sleep(1)
    event = Event(i)
    print("P: [%f] Producing event %d!" % (time.time() - t0, event.x))
    spaces.wait()
    mutex.wait()
    buffer.append(event)
    mutex.signal()
    items.signal()
    print("P: [%f] Finished putting event %d in buffer" % (time.time() - t0, event.x))
    i += 1

def consumer():
  global buffer
  while True:
    items.wait()
    mutex.wait()
    event = buffer.popleft()
    mutex.signal()
    spaces.signal()
    print("C: [%f] Consuming event %d!" % (time.time() - t0, event.x))
    time.sleep(2)
    print("C: [%f] Finished consuming event %d!" % (time.time() - t0, event.x))


watcher()

Thread(producer)
Thread(consumer)
