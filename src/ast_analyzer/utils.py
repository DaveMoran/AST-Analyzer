"""
ast_analyzer.utils

A list of helper functions that can be reused throughout the application
"""

import time

DEFAULT_FMT = "[{curr_time} | {time_taken:0.2f}s] {fn_name}({args}) -> {result}"


class ast_timing:
    def __init__(self, fmt=DEFAULT_FMT):
        self.fmt = fmt
        self.accumulated_time = 0
        self.times_called = 0

    def __call__(self, fn):

        def timestamp(*_args):
            # Start timer
            curr_time = time.strftime("%H:%M:%S", time.localtime())
            start_time = time.perf_counter()

            # Run function
            _result = fn(*_args)

            # Get time taken, add to free variables
            time_taken = time.perf_counter() - start_time
            self.accumulated_time += time_taken
            self.times_called += 1

            # Populate logger variables
            fn_name = fn.__name__
            args = ", ".join(repr(arg) for arg in _args)
            result = repr(_result)

            # Print timing
            print(self.fmt.format(**locals()))
            if time_taken > 0.5:
                print(f"{'-' * 20} WARNING: Function took longer than 0.5s {'-' * 20}")
            return _result

        return timestamp

    def __repr__(self):
        return f"Function '{self.func.__name__}' called {self.times_called} times. Total time: {self.accumulated_time:.2}s."
