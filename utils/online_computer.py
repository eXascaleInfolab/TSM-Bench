import time
from threading import Thread
from threading import Event

from systems.utils.online_library import generate_continuing_data


class IngestionResult:
    def __init__(self, tn):
        self.status = "ok"
        self.tn = tn
        self.insertions = []
        self.evaluated = False
        self.error_message = None

    def add(self, n_rows_inserted, start_time, end_time):
        self.insertions.append((n_rows_inserted, start_time, end_time))

    def set_fail(self, e: Exception):
        print(f"thread {self.tn} failed with {e}")
        self.status = "failed"
        self.error_message = str(e)

    def set_evaluated(self):
        self.evaluated = True


class DataIngestor:
    def __init__(self, system_module, dataset, *, n_rows_s, max_runtime, host, n_threads, ):
        self.n_threads = n_threads
        self.n_rows_s = n_rows_s
        self.host = host
        self.threads = None
        self.event = None
        self.system_module = system_module
        self.dataset = dataset
        self.max_runtime = max_runtime  # seconds

    def __enter__(self):
        self.event = Event()
        self.threads = []
        self.ingestion_results = [IngestionResult(tn) for tn in range(self.n_threads)]

        print("generating data")



        insertion_queries = [-1] * self.n_threads

        for t_n in range(self.n_threads):
            data = generate_continuing_data(self.n_rows_s * self.max_runtime, self.dataset)
            ingestion = [self.system_module.generate_insertion_query(
                time_stamps=data["time_stamps"][i:i + self.n_rows_s],
                station_ids=data["stations"][i:i + self.n_rows_s],
                sensors_values=data["sensors"][i:i + self.n_rows_s],
                dataset=self.dataset)
                for i in range(0, self.n_rows_s * self.max_runtime, self.n_rows_s)]
            self.start_date = data["start_date"]
            insertion_queries[t_n] = ingestion

        assert len(insertion_queries) == self.n_threads
        assert len(insertion_queries[0]) == self.max_runtime

        input_data_f  = self.system_module.input_data

        print("starting insertion")
        for t_n in range(self.n_threads):
            thread = Thread(target=input_data_f, args=(insertion_queries[t_n], self.event, self.ingestion_results[t_n], self.host , self.dataset))
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
        print("AAAAAAAAAAAAA")
        print(*[ingestion_result.insertions for ingestion_result in self.ingestion_results], sep="\n")







