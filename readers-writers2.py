# readers writers using lightswitches

# desired: n readers can all simultaneously read a value but only 1 writer can write
# no readers can be reading while writing is happening

# note that there's a tendency for starvation to occur unless you tune the sleeps properly
from sync import Thread, Semaphore, watcher
from LightswitchObj import LightswitchObj
import time, random

N_READERS = 5
N_WRITERS = 5

value = 0
lightswitch = LightswitchObj()
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
  global LightswitchObj
  while True:
    lightswitch.lock(roomEmpty)
    print("Reader %d is reading %d" % (i, value))
    time.sleep(random.random() * 5)
    lightswitch.unlock(roomEmpty)
    time.sleep(random.random() * 10)


watcher()

[Thread(writer, i) for i in range(N_WRITERS)]
[Thread(reader, i) for i in range(N_READERS)]
