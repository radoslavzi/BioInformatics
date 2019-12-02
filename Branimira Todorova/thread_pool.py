from multiprocessing.pool import ThreadPool
import threading
import time

def test_work(str1, str2):
    print(threading.currentThread().getName())
    print(str1 + " => " + str2)
    time.sleep(5)
    return " test str" + str(str1)

pool = ThreadPool(processes=5)
#res = pool.apply_async(test_work, ("work", "test"))
#res.get(5)

tasks = []
for i in range(0, 100):
    tasks.append(pool.apply_async(test_work, ("work", "test")))

for task in tasks:
    while not  task.ready():
        task.wait()
    if not task.successful():
        continue
    

    print(str(task.get(6)))    