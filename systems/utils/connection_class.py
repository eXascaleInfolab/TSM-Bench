class Connection:
    # class to wrap connection to database for the different systems
    def __init__(self, close_f, execute_f, write_f=None):
        self.close_f = close_f
        self.execute_f = execute_f
        self.write_f = write_f if write_f is not None else execute_f #used in online setting

    def close(self):
        self.close_f()

    def execute(self, query):
        return self.execute_f(query)

    def write(self, query , **kwargs):
        #query to insert or points to insert eg with influx write_points
        return self.write_f(query, **kwargs)
