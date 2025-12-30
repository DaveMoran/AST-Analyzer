"""
tests.test_reporter
"""

from ast_analyzer.reporter import reporter


def test_reporter():
    assert reporter() == "reporter"
