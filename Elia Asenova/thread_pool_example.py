from multiprocessing.pool import ThreadPool
import threading
import time

def test_work(str1, str2):
    print(threading.currentThread().getName() + str(str1) + " => " + str(str2))
    time.sleep(5)
    return "new string " + str(str1)  

pool = ThreadPool(processes=5)
tasks = []

for i in range(0,100):
    tasks.append(pool.apply_async(test_work, ("work", "test")))

for task in tasks:
    while not task.ready(): pass
    if not task.successful():
        print("ERROR while execution")
        continue

    print(str(task.get(6)))