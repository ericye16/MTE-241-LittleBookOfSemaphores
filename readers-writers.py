# readers writers

# desired: n readers can all simultaneously read a value but only 1 writer can write
# no readers can be reading while writing is happening

from sync import Thread, Semaphore, watcher
import time, random

N_READERS = 5
N_WRITERS = 5

value = 0
readers = 0
mutex = Semaphore(1)
roomEmpty = Semaphore(1)

def writer(i):
  global value
  while True:
    time.sleep(random.random())
    roomEmpty.wait()
    value = random.randint(0,5)
    print("Writer %d is writing %d" % (i, value))
    time.sleep(random.random() * 3)
    roomEmpty.signal()

def reader(i):
  global value
  global readers
  while True:
    mutex.wait()
    readers += 1
    if readers == 1:
      roomEmpty.wait()
    mutex.signal()
    print("Reader %d with %d readers is reading %d" % (i, readers, value))
    time.sleep(random.random() * 5)
    mutex.wait()
    readers -= 1
    if readers == 0:
      roomEmpty.signal()
    mutex.signal()
    time.sleep(random.random() * 10)


watcher()

[Thread(writer, i) for i in range(N_WRITERS)]
[Thread(reader, i) for i in range(N_READERS)]
