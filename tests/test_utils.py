import time

from ast_analyzer.utils import ast_timing


@ast_timing
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


@ast_timing
def expensive_function(duration):
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

    expensive_function(0.5)
    captured = capsys.readouterr()
    assert "WARNING" in captured.out
