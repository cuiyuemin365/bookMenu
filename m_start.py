from config.config import Config
from mythread import TablePageThread, DetailPageThread

if __name__ == '__main__':
    cfg = Config.get_cfg()
    tag_threads = []
    tag_thread_num = int(cfg.get("sys", "tag_thread_num"))
    for i in range(0, tag_thread_num):
        m = TablePageThread("TablePageThread" + str(i))
        tag_threads.append(m)

    for i in range(0, tag_thread_num):
        tag_threads[i].start()

    # id_threads = []
    # id_thread_num = int(cfg.get("sys", "id_thread_num"))
    # for i in range(0, id_thread_num):
    #     m = DetailPageThread("DetailPageThread" + str(i))
    #     id_threads.append(m)
    #
    # for i in range(0, id_thread_num):
    #     id_threads[i].start()

    for i in range(0, tag_thread_num):
        tag_threads[i].join()
    # for i in range(0, id_thread_num):
    #     id_threads[i].join()
