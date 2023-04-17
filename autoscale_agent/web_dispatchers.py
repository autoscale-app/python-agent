import threading
import traceback
import time
import sys


class AlreadySetError(Exception):
    pass


class WebDispatchers:
    DISPATCH_INTERVAL = 15

    def __init__(self):
        self.queue_time = None

    def set_queue_time(self, dispatcher):
        if self.queue_time is not None:
            raise AlreadySetError

        self.queue_time = dispatcher

    def dispatch(self):
        try:
            if self.queue_time:
                self.queue_time.dispatch()
        except Exception as e:
            print(
                f"Autoscale: {type(e).__name__}\n{traceback.print_tb(e.__traceback__)}"
            )

    def run(self):
        threading.Thread(target=self.run_loop, daemon=True).start()

    def run_loop(self):
        while True:
            self.dispatch()
            sys.stdout.flush()
            time.sleep(self.DISPATCH_INTERVAL)
