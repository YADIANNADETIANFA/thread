import threading
import time
import queue


def blocking_task(td_name, delay, result_queue):
    try:
        print(f"[{td_name}] 开始执行，预期耗时 {delay}s")

        # 同步阻塞任务
        time.sleep(delay)

        if td_name == "td_3":
            raise Exception("让td_3执行出现异常")

        # 将结果放入线程安全队列
        result_queue.put((td_name, "success", f"{td_name} 执行完毕"))

        print(f"[{td_name}] 任务结束")
    except Exception as e:
        # 在线程安全队列，手动添加子线程异常
        result_queue.put((td_name, "error", e))


def main():
    # 用于存储线程结果的线程安全队列
    result_queue = queue.Queue()

    # 创建子线程
    td_1 = threading.Thread(target=blocking_task, args=("td_1", 1, result_queue))
    td_2 = threading.Thread(target=blocking_task, args=("td_2", 2, result_queue))
    td_3 = threading.Thread(target=blocking_task, args=("td_3", 3, result_queue))

    # 启动线程
    td_1.start()
    td_2.start()
    td_3.start()

    # 等待线程结束
    td_1.join()
    td_2.join()
    td_3.join()

    # 获取线程返回结果
    while not result_queue.empty():
        td_name, status, result = result_queue.get()
        if status == "success":
            print(f"[主线程] {td_name} 返回结果：{result}")
        else:
            print(f"[主线程] {td_name} 抛出异常：{result}")


if __name__ == "__main__":
    main()