from threading import Thread

def thread_function(target, args, start_thread=False):
    thread = Thread(target=target, args=args)

    if (start_thread):
        thread_start(thread=thread)

    return thread

def thread_start(thread):
    thread.start()