"""
ast_analyzer.utils

A list of helper functions that can be reused throughout the application
"""

import time
import functools

from typing import Callable, Any

DEFAULT_FMT = "[{curr_time} | {time_taken:0.2f}s] {fn_name}({args}) -> {result}"


class ast_timing:
    def __init__(self, fn: Callable, fmt: str = DEFAULT_FMT):
        functools.wraps(fn)(self)
        self.fn = fn
        self.fmt = fmt
        self.accumulated_time = 0
        self.times_called = 0

    def __call__(self, *args: Any, **kwargs: Any):
        # Start timer
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        start_time = time.perf_counter()

        # Run function
        _result = self.fn(*args, **kwargs)

        # Get time taken, add to free variables
        time_taken = time.perf_counter() - start_time
        self.accumulated_time += time_taken
        self.times_called += 1

        # Populate logger variables
        fn_name = self.fn.__name__
        args = ", ".join(repr(arg) for arg in args)
        result = repr(_result)

        # Print timing
        print(self.fmt.format(**locals()))
        if time_taken > 0.5:
            print(f"{'-' * 20} WARNING: Function took longer than 0.5s {'-' * 20}")
        return _result

    def __repr__(self):
        return f"Function '{self.fn.__name__}' called {self.times_called} times. Total time: {self.accumulated_time:.2f}s."
