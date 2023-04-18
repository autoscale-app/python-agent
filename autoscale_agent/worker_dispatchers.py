import threading
import traceback
import time


class WorkerDispatchers:
    DISPATCH_INTERVAL = 15

    def __init__(self):
        self._dispatchers = []
        self._running = False
        self._running_lock = threading.Lock()

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
        with self._running_lock:
            if not self._dispatchers:
                return

            if not self._running:
                self._running = True
                threading.Thread(target=self._run_loop, daemon=True).start()

    def _run_loop(self):
        while True:
            self.dispatch()
            time.sleep(self.DISPATCH_INTERVAL)
