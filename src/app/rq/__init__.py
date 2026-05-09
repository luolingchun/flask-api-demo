from app.config import REDIS_CONNECT

default_queue = None


def init_queue():
    from rq import Queue

    global default_queue
    default_queue = Queue(name="default", connection=REDIS_CONNECT)
