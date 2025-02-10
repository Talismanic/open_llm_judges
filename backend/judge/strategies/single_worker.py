class SingleWorkerStrategy:
    def execute(self, workers, task_info):
        """
        Executes the task using a single worker.
        """
        worker = workers[0]

        # Create an event loop if not already running
        result = worker.run_sync(task_info).data
        

        return result
