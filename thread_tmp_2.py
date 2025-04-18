import threading
import time
import queue


# 待处理任务列表
data_ls = ["task_1", "task_2", "task_3", "task_4", "task_5", "task_6", "task_7", "task_8", "task_9", "task_10"]

# 全局索引
index = 0

# 同步锁
lock = threading.Lock()


def worker(td_name):
    # 在当前函数中，使用并修改"全局索引index"，而不是创建一个新的局部变量
    global index

    while True:
        # 在上下文中获取同步锁，并在上下文结束后，自动释放。避免遗忘而产生死锁
        # 保证线程安全
        with lock:
            if index >= len(data_ls):
                break   # 所有任务已分配完成
            item = data_ls[index]
            index += 1

        print(f"[{td_name}] 正在处理：{item}]")
        time.sleep(3)
        print(f"[{td_name}] 处理完成：{item}]")


def main():
    # 手动创建3个线程
    threads = []
    for i in range(3):
        td = threading.Thread(target=worker, args=(f"td_{i+1}",))
        threads.append(td)
        td.start()

    # 等待所有线程结束
    for t in threads:
        t.join()

    print("所有任务处理完成")


if __name__ == '__main__':
    main()
