import time

from ast_analyzer.utils import ast_timing


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
