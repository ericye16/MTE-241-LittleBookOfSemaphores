# cowboys

# desired: group of cowboys eat dinner from a large pot with M servings of chili
# cowboy wants to eat, he helps himself from pot
# if pot empty, cowboy wakes up the cook then waits until cook refills the pot

from sync import Thread, Semaphore, watcher
import time, random

N_COWBOYS = 10
M = 15

t0 = time.time()

servings = 0
mutex = Semaphore(1)
emptyPot = Semaphore(0)
fullPot = Semaphore(0)

def cowboy(i):
  global servings
  while True:
    mutex.wait()
    if servings == 0:
      print("[%f] Cowboy %d is asking cook to refill pot" % (time.time() - t0, i))
      emptyPot.signal()
      fullPot.wait()
      servings = M
    servings -= 1
    time.sleep(random.random()) # it takes up to 1s to take a serving
    print("[%f] Cowboy %d took a serving with %d servings left" % (time.time() - t0, i, servings))
    mutex.signal()
    time.sleep(random.random() * 5) # it takes up to 5s to eat a serving
    # print("Cowboy %d finished eating" % i)

def cook():
  while True:
    emptyPot.wait()
    print("[%f] Filling pot" % (time.time() - t0))
    time.sleep(random.random() * 5)
    print("[%f] Filled pot!" % (time.time() - t0))
    fullPot.signal()

watcher()

[Thread(cowboy, i) for i in range(N_COWBOYS)]
Thread(cook)
