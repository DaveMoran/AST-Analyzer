import functools
import logging

from typing import Callable, Any, Optional


class logger:
    """Decorator for logging function calls during AST analysis.

    Logs function calls at a specified level with configurable logger
    name and message. Useful for debugging and monitoring analyzer behavior.

    Args:
        level: Logging level (e.g., logging.DEBUG, logging.INFO)
        name: Optional logger name (defaults to function's module)
        message: Optional log message (defaults to function's name)

    Example:
        >>> @logger(logging.INFO)
        ... def analyze_file(filepath):
        ...     pass

        >>> @logger(logging.DEBUG, name="analyzer", message="Processing")
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
                raise
            else:
                self.log.log(
                    self.level, f"Function {self.logname} Complete. Result: {result}"
                )
                return result

        return wrapper
