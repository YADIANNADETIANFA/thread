from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import time


# 线程安全的任务队列
task_queue = Queue()


def worker(td_name):
    # 循环执行
    while True:
        # 这里是重点！(如果队列为空，会阻塞等待，直到新任务到来)
        task = task_queue.get()

        print(f"td-{td_name} 开始处理任务: {task}")
        time.sleep(5)
        print(f"td-{td_name} 完成任务处理: {task}")


def main():
    num_thread = 5

    with ThreadPoolExecutor(max_workers=num_thread) as executor:
        for i in range(num_thread):
            executor.submit(worker, f"td-{i}")


if __name__ == '__main__':
    # 模拟任务添加 (可随时追加任务)
    for i in range(20):
        task_queue.put(f"task_{i}")

    main()