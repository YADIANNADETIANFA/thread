from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import time


def worker(td_name):
    # 随机阻塞1s~5s
    time.sleep(random.randint(1, 5))
    return f"{td_name} done"


num_threads = 5

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(worker, f"td_{i}") for i in range(num_threads)]

    # 直接遍历`futures`列表本身，而不是`as_completed`，即可实现"按照提交顺序返回线程结果"
    """
    输出结果始终都是：
        td_0 done
        td_1 done
        td_2 done
        td_3 done
        td_4 done
    """
    for future in futures:
        print(future.result())

    # 输出结果随机乱序
    # for future in as_completed(futures):
    #     print(future.result())