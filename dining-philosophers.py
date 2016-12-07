# dining philosophers

# desired: n philosophers, each of whom require left and right chopsticks, must eat
# this induces deadlock

from __future__ import print_function
from sync import Thread, Semaphore, watcher
import time, random

N_PHILOSOPHERS = 5

chopsticks = [Semaphore(1) for i in range(N_PHILOSOPHERS)]

# chopsticks_used is just for illustration purposes and isn't part of the solution
chopsticks_used = [False for i in range(N_PHILOSOPHERS)]
mutex_chopsticks_used = Semaphore(1)

def print_chopstick(chopstick):
  if chopstick: return "X"
  else: return "O"

def left(i):
  return i

def right(i):
  return (i + 1) % N_PHILOSOPHERS

def get_chopsticks(i):
  chopsticks[left(i)].wait()
  mutex_chopsticks_used.wait()
  chopsticks_used[left(i)] = True
  mutex_chopsticks_used.signal()

  time.sleep(1)
  chopsticks[right(i)].wait()
  mutex_chopsticks_used.wait()
  chopsticks_used[right(i)] = True
  mutex_chopsticks_used.signal()

def put_chopsticks(i):
  chopsticks[left(i)].signal()
  chopsticks[right(i)].signal()

  mutex_chopsticks_used.wait()
  chopsticks_used[left(i)] = False
  chopsticks_used[right(i)] = False
  mutex_chopsticks_used.signal()

def print_chopsticks_used():
  mutex_chopsticks_used.wait()
  print("[", end = "")
  for i in range(N_PHILOSOPHERS):
    print(print_chopstick(chopsticks_used[i]), end="")
    print(",", end = "")

  print("]")
  mutex_chopsticks_used.signal()

def philosopher(i):
  while True:
    print("%i is thinking..." % i)
    # time.sleep(i + 1)
    print("%i is done thinking and ready to eat" % i)
    print_chopsticks_used()
    get_chopsticks(i)
    print("%i is starting to eat" % i)
    print_chopsticks_used()
    # time.sleep(i + 1)
    print("%i is done eating" % i)
    put_chopsticks(i)
    print_chopsticks_used()


watcher()

[Thread(philosopher, i) for i in range(N_PHILOSOPHERS)]
