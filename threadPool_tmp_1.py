import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 模拟任务列表
task_ls = [f"task_{i}" for i in range(10)]

# 全局索引
task_index = 0

# 同步锁
index_lock = threading.Lock()

# 线程安全的结果队列
result_queue = Queue()


def get_task():
    # 在当前函数中，使用并修改"全局索引task_index"，而不是创建一个新的局部变量
    global task_index

    with index_lock:
        if task_index >= len(task_ls):
            return None
        task = task_ls[task_index]
        task_index += 1
        return task


def worker(td_name):
    while True:
        # 每个子线程一经创建，就会循环不断地处理任务
        task = get_task()
        if task is None:
            break
        try:
            # 模拟任务处理
            print(f"td-{td_name} start process task: {task}")
            time.sleep(5)
            print(f"td-{td_name} end process task: {task}")

            result = f"{td_name} processed {task} done."
            result_queue.put({"task": task, "result": result, "error": None})
        except Exception as e:
            # 在线程安全队列，手动添加子线程的任务处理异常
            result_queue.put({"task": task, "result": None, "error": e})


def main():
    num_threads = 3

    # 启动线程池
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 启动多个子线程，提交任务
        # 每个子线程都会立即返回一个future对象
        futures = [executor.submit(worker, f"td_{i}") for i in range(num_threads)]

        # `as_completed(futures)`是一个生成器，每当任意一个线程结束，就会yield一个future对象
        #  (注意，这里debug时，似乎是所有子线程全部结束，才返回。那是因为每一个子线程始终都在内部循环，直至所有任务都结束。所以才看起来像是所有子线程都结束了才返回。)
        for future in as_completed(futures):
            try:
                # 阻塞当前主线程，等待该future对应的子线程执行结束
                # 返回子线程return的结果，由于没有return，所以是None
                # 可用于子线程的异常捕获 (如果该future对应的子线程，执行中抛出异常，`result`会重新抛出)
                future.result()
            except Exception as e:
                # 捕获线程级异常 (worker内没有捕获到的异常，导致子线程执行失败)
                result_queue.put({"task": "thread-level-error", "result": None, "error": e})

    # 汇总结果
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    # 打印所有结果
    for item in results:
        if item["error"]:
            print(f"Task: {item['task']} failed with error: {item['error']}")
        else:
            print(f"Task: {item['task']} succeeded with result: {item['result']}")


if __name__ == '__main__':
    main()


"""
# with ThreadPoolExecutor(max_workers=num_threads) as executor:
线程池上下文管理器，它的作用：
+ 创建线程池`executor`
+ 在`with`上下文块结束时，自动调用`executor.shutdown(wait=True)`
    + `shutdown(wait=True)`的作用：等待线程池中所有线程任务执行完成后，才继续执行之后的代码


"""