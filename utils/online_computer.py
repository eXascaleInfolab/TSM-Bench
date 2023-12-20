import time
from threading import Thread
from threading import Event
from systems import timescaledb  # for type hints

from systems.utils.online_library import generate_continuing_data


class DataIngestor:
    def __init__(self, system_module, dataset, *, batch_size, host, n_threads):
        self.n_threads = n_threads
        self.batch_size = batch_size
        self.host = host
        self.threads = None
        self.insertion_stats = None
        self.event = None
        self.system_module = system_module
        self.dataset = dataset

    def __enter__(self):
        print("starting insertion")
        self.event = Event()
        self.insertion_stats = [{"status": "ok", "insertions": []} for _ in range(self.n_threads)]
        self.threads = []

        data = generate_continuing_data(self.batch_size * 1000, self.dataset)
        self.start_date = data["start_date"]

        input_data_f: timescaledb.input_data = self.system_module.input_data
        for t_n in range(self.n_threads):
            thread = Thread(target=self.system_module.input_data, args=(
                t_n, self.event, data, self.insertion_stats[t_n], self.batch_size, self.host, self.dataset))
            thread.start()
            self.threads.append(thread)

        time.sleep(10)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.event.set()
        time.sleep(10)
        for thread in self.threads:
            print("joining threads")
            thread.join()

        print("cleaning database")
        self.system_module.delete_data(date=self.start_date, host=self.host, dataset=self.dataset)
        if exc_type is not None:
            print(f"Exception caught: {exc_value}, {exc_type} , {exc_value} continuing...")
            print(traceback)
            # Handle or log the exception here if needed
            return True  # Suppresses the exception
