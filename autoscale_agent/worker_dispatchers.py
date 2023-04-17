import threading
import traceback
import time


class WorkerDispatchers:
    DISPATCH_INTERVAL = 15

    def __init__(self):
        self._dispatchers = []

    def append(self, dispatcher):
        self._dispatchers.append(dispatcher)

    def dispatch(self):
        for dispatcher in self._dispatchers:
            try:
                dispatcher.dispatch()
            except Exception as e:
                print(
                    f"Autoscale: {type(e).__name__}\n{traceback.print_tb(e.__traceback__)}"
                )

    def run(self):
        threading.Thread(target=self.run_loop, daemon=True).start()

    def run_loop(self):
        while True:
            self.dispatch()
            time.sleep(self.DISPATCH_INTERVAL)
