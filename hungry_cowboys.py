# cowboys

# desired: group of cowboys eat dinner from a large pot with M servings of chili
# cowboy wants to eat, he helps himself from pot
# if pot empty, cowboy wakes up the cook then waits until cook refills the pot

from sync import Thread, Semaphore, watcher
import time, random

N_COWBOYS = 10
M = 15

servings = 0
mutex = Semaphore(1)
emptyPot = Semaphore(0)
fullPot = Semaphore(0)

def cowboy(i):
  global servings
  while True:
    mutex.wait()
    if servings == 0:
      emptyPot.signal()
      fullPot.wait()
      servings = M
    servings -= 1
    print("Cowboy %d took a serving with %d servings left" % (i, servings))
    mutex.signal()
    time.sleep(random.random() * 5)
    # print("Cowboy %d finished eating" % i)

def cook():
  while True:
    emptyPot.wait()
    print("Filling pot")
    time.sleep(random.random() * 5)
    print("Filled pot!")
    fullPot.signal()

watcher()

[Thread(cowboy, i) for i in range(N_COWBOYS)]
Thread(cook)
