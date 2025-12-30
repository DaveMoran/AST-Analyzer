"""
tests.test_analyzer
"""

from ast_analyzer.analyzer import analyzer


def test_analyzer():
    assert analyzer() == "analyzer"
