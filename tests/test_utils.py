import logging
import time

from ast_analyzer.utils import ast_timing, ast_log


@ast_timing
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


@ast_timing
def timed_sleep(duration):
    time.sleep(duration)
    return "Done"


def test_prints_timing_output(capsys):
    """Decorator should print timing information to stdout."""

    factorial(3)
    captured = capsys.readouterr()
    assert "factorial" in captured.out
    assert "->" in captured.out


def test_longer_time(capsys):
    """Decorator should print out warning msg"""

    timed_sleep(0.5)
    captured = capsys.readouterr()
    assert "WARNING" in captured.out


def test_accumulated_time():
    """Decorator should print out combined time"""

    @ast_timing
    def local_timed_sleep(duration):
        time.sleep(duration)
        return "Done"

    local_timed_sleep(0.3)
    local_timed_sleep(0.2)
    local_timed_sleep(0.1)

    assert local_timed_sleep.times_called == 3
    assert 0.59 < local_timed_sleep.accumulated_time < 0.61  # Allow 0.01s tolerance


def test_return():
    """Decorator does not affect the original function return"""
    result = factorial(4)

    assert result == 24


"""
TODO: Quick follow PR to split decorator tests and fn into separate files
For now we'll use this as a separator
"""


@ast_log(logging.DEBUG)
def add(a, b):
    return a + b


def test_ast_log_defaults(caplog):

    with caplog.at_level(logging.DEBUG):
        add(3, 5)

    assert "DEBUG" in caplog.text
    assert "add" in caplog.text


@ast_log(logging.DEBUG, name="Subtraction")
def sub(a, b):
    return a - b


def test_with_custom_name(caplog):

    with caplog.at_level(logging.DEBUG):
        sub(3, 5)

    assert "DEBUG" in caplog.text
    assert "Subtraction" in caplog.text


@ast_log(logging.DEBUG, message="Custom Message")
def mult(a, b):
    return a * b


def test_with_custom_msg(caplog):

    with caplog.at_level(logging.DEBUG):
        mult(3, 5)

    assert "DEBUG" in caplog.text
    assert "Custom Message" in caplog.text


@ast_log(logging.INFO, name="Math.Div", message="Division operation")
def div(a, b):
    return a / b


def test_ast_log_full_custom(caplog):
    with caplog.at_level(logging.INFO):
        div(10, 2)

    assert "INFO" in caplog.text
    assert "Math.Div" in caplog.text
    assert "Division operation" in caplog.text
