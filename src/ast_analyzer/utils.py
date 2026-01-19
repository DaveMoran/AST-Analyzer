"""
ast_analyzer.utils

A list of helper functions that can be reused throughout the application
"""

import fnmatch
import functools
import logging
import os
import time

from pathlib import Path
from typing import Callable, Any, Optional, Generator, Collection

DEFAULT_FMT = "[{curr_time} | {time_taken:0.2f}s] {fn_name}({args}) -> {result}"


class ast_timing:
    """
    Custom decorator that allows for functions to have timing metrics display per run
    """

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


class ast_log:
    """Decorator for logging function calls during AST analysis.

    Logs function calls at a specified level with configurable logger
    name and message. Useful for debugging and monitoring analyzer behavior.

    Args:
        level: Logging level (e.g., logging.DEBUG, logging.INFO)
        name: Optional logger name (defaults to function's module)
        message: Optional log message (defaults to function's name)

    Example:
        >>> @ast_log(logging.INFO)
        ... def analyze_file(filepath):
        ...     pass

        >>> @ast_log(logging.DEBUG, name="analyzer", message="Processing")
        ... def process():
        ...     pass
    """

    def __init__(
        self, level: int, name: Optional[str] = None, message: Optional[str] = None
    ):
        self.level = level
        self.logname = name
        self.logmsg = message

    def __call__(self, fn: Callable[..., Any]):
        self.fn = fn
        self.logname = self.logname if self.logname else fn.__module__
        self.log = logging.getLogger(self.logname)
        self.logmsg = self.logmsg if self.logmsg else fn.__name__

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            self.log.log(self.level, f"Begin Function {self.logmsg} | Args: {args}")
            try:
                result = fn(*args, **kwargs)
            except:
                self.log.exception(
                    f"Error during execution of {self.logmsg}. See traceback below",
                )
            else:
                self.log.log(
                    self.level, f"Function {self.logname} Complete. Result: {result}"
                )
                return result

        return wrapper


def read_from_directory(directory: str) -> Generator[Path, None, None]:
    filenames = (
        file_path
        for file_path in Path(directory).rglob("*")
        if os.access(str(file_path), os.R_OK) and file_path.is_file()
    )
    return filenames


def read_lines(filepath: Path):
    with open(filepath) as f:
        for line in f:
            yield line


def filter_python_files(files: Generator[Path, None, None]):
    for file in files:
        yield file


def filter_by_gitignore(files: Generator[Path, None, None], ignore_file: str):
    for file in files:
        is_match = False
        gen_gitignore = read_lines(ignore_file)
        for ignore_case in gen_gitignore:
            ignore_case = ignore_case.strip()
            if fnmatch.fnmatch(file.name, ignore_case):
                is_match = True

        if not is_match:
            yield file


def filter_by_custom_matches(files: Generator[Path, None, None], matches: Collection):
    for file in files:
        full_path = str(file)
        if not any(match in full_path for match in matches):
            yield file


def skip_virtual_envs(files: Generator[Path, None, None]):
    virtual_envs = ["venv/", ".venv/", "env/"]
    for file in files:
        full_path = str(file)
        if not any(env in full_path for env in virtual_envs):
            yield file


def skip_cache(files: Generator[Path, None, None]):
    caches = ["__pycache__/", ".mypy_cache/", ".pytest_cache/", ".ruff_cache/"]
    for file in files:
        full_path = str(file)
        if not any(cache in full_path for cache in caches):
            yield file


def skip_git(files: Generator[Path, None, None]):
    for file in files:
        full_path = str(file)
        if ".git" not in full_path:
            yield file


def get_working_files(
    directory: str, custom_matches: Collection
) -> Generator[Path, None, None]:
    files = read_from_directory(directory)

    filtered_files = skip_git(
        skip_cache(
            skip_virtual_envs(
                filter_by_custom_matches(
                    filter_python_files(filter_by_gitignore(files, ".gitignore")),
                    custom_matches,
                )
            )
        )
    )

    return filtered_files


if __name__ == "__main__":
    files = get_working_files("./", ["tests"])

    for file in files:
        print(file)
