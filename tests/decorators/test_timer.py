import time

from ast_analyzer.decorators import timer


@timer.timer
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


@timer.timer
def timed_sleep(duration):
    time.sleep(duration)
    return "Done"


def test_repr():
    """Decorator __repr__ shows call count and total time."""

    @timer.timer
    def quick_fn():
        return 1

    quick_fn()
    quick_fn()

    repr_str = repr(quick_fn)
    assert "quick_fn" in repr_str
    assert "2 times" in repr_str


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

    @timer.timer
    def local_timed_sleep(duration):
        time.sleep(duration)
        return "Done"

    local_timed_sleep(0.3)
    local_timed_sleep(0.2)
    local_timed_sleep(0.1)

    assert local_timed_sleep.times_called == 3
    assert 0.58 < local_timed_sleep.accumulated_time < 0.62  # Allow 0.02s tolerance


def test_return():
    """Decorator does not affect the original function return"""
    result = factorial(4)

    assert result == 24
