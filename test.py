import threading
import time

def worker(num):
    """thread worker function"""
    print ('Worker start: %s' % num)
    time.sleep(2)
    print('Worker end: %s' % num)
    return

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()