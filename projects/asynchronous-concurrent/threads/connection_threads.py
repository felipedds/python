import time
from threading import Thread
from queue import Queue

''' 
One thread(data_generator) generates the data and 
the other thread(data_consumer) depends on the data from the other to execute.
'''

def data_generator(queue):
    for i in range(1, 11):
        print(f'Data {i} gerated.', flush=True)
        time.sleep(2)
        queue.put(i)

def data_consumer(queue):
    while queue.qsize() > 0:
        val = queue.get()
        print(f'Data {val * 2} processed.', flush=True)
        time.sleep(1)
        queue.task_done()

if __name__ == '__main__':
    print('System initiated.', flush=True)
    queue = Queue()
    thread1 = Thread(target=data_generator, args=(queue,))
    thread2 = Thread(target=data_consumer, args=(queue,))

    thread1.start()
    thread1.join()
    thread2.start()
    thread2.join()