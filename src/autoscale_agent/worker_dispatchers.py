import threading
import traceback
import time

class WorkerDispatchers:
    DISPATCH_INTERVAL = 15

    def __init__(self):
        self._dispatchers = []

    def __iter__(self):
        return iter(self._dispatchers)

    def __len__(self):
        return len(self._dispatchers)

    def __getitem__(self, index):
        return self._dispatchers[index]

    def append(self, dispatcher):
        self._dispatchers.append(dispatcher)

    def dispatch(self):
        for dispatcher in self:
            try:
                dispatcher.dispatch()
            except Exception as e:
                print(f"Autoscale::Agent/WorkerDispatcher: {type(e).__name__}\n{traceback.print_tb(e.__traceback__)}")

    def run(self):
        def _run():
            while True:
                self.dispatch()
                time.sleep(self.DISPATCH_INTERVAL)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
