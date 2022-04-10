import threading
import time

class Worker(threading.Thread):
    
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("sub thread start ", threading.currentThread().getName())
        time.sleep(5)
        print("sub thread end ", threading.currentThread().getName())


print("main thread start")

threads = []
for i in range(3):
    thread = Worker(i)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("main thread post job")
print("main thread end")
