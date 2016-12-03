import threading, os, sys, signal

# some code to simplify python's threading

class Semaphore(threading._Semaphore):
  wait = threading._Semaphore.acquire
  signal = threading._Semaphore.release

class Thread(threading.Thread):
  def __init__(self, t, *args):
    threading.Thread.__init__(self, target=t, args=args)
    self.start()

def watcher():
  child = os.fork()
  if child == 0: return
  try:
    os.wait()
  except KeyboardInterrupt:
    print 'KeyboardInterrupt'
    os.kill(child, signal.SIGKILL)
  sys.exit()