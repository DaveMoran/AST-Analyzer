"""
ast_analyzer.utils

A list of helper functions that can be reused throughout the application
"""

import time

DEFAULT_FMT = "[{curr_time} | {time_taken:0.2f}s] {fn_name}({args}) -> {result}"


class ast_timing:
    def __init__(self, fmt=DEFAULT_FMT):
        self.fmt = fmt

    def __call__(self, fn):

        def timestamp(*_args):
            curr_time = time.strftime("%H:%M:%S", time.localtime())
            start_time = time.perf_counter()
            _result = fn(*_args)
            time_taken = time.perf_counter() - start_time
            fn_name = fn.__name__
            args = ", ".join(repr(arg) for arg in _args)
            result = repr(_result)
            print(self.fmt.format(**locals()))
            return _result

        return timestamp
