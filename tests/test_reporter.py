"""
tests.test_reporter
"""

import pytest


# =============================================================================
# MetricsCollector Tests
# =============================================================================
@pytest.mark.metrics
class TestMetricsCollectorInit:
    """Tests for MetricsCollector.__init__"""

    def test_init_total_fns_zero(self, metrics_collector):
        """total_fns starts at 0."""
        assert metrics_collector.total_fns == 0

    def test_init_total_lines_zero(self, metrics_collector):
        """total_lines starts at 0."""
        assert metrics_collector.total_lines == 0

    def test_init_files_analyzed_zero(self, metrics_collector):
        """files_analyzed starts at 0."""
        assert metrics_collector.files_analyzed == 0


@pytest.mark.metrics
class TestMetricsCollectorAddFileMetrics:
    """Tests for MetricsCollector.add_file_metrics"""

    def test_add_single_file(self, metrics_collector):
        """Adding metrics for one file updates counters."""
        metrics_collector.add_file_metrics(5, 100)
        assert metrics_collector.total_fns == 5
        assert metrics_collector.total_lines == 100
        assert metrics_collector.files_analyzed == 1

    def test_add_multiple_files(self, metrics_collector):
        """Adding metrics for multiple files accumulates."""
        metrics_collector.add_file_metrics(5, 100)
        metrics_collector.add_file_metrics(3, 50)
        metrics_collector.add_file_metrics(2, 25)
        assert metrics_collector.total_fns == 10
        assert metrics_collector.total_lines == 175
        assert metrics_collector.files_analyzed == 3

    @pytest.mark.parametrize(
        "fn_count,ln_count",
        [
            (0, 0),
            (0, 100),
            (10, 0),
        ],
    )
    def test_add_zero_values(self, metrics_collector, fn_count, ln_count):
        """Adding zero values is valid."""
        metrics_collector.add_file_metrics(fn_count, ln_count)
        assert metrics_collector.total_fns == fn_count
        assert metrics_collector.total_lines == ln_count
        assert metrics_collector.files_analyzed == 1


@pytest.mark.metrics
class TestMetricsCollectorGetSummary:
    """Tests for MetricsCollector.get_summary"""

    def test_get_summary_empty_raises_division_error(self, metrics_collector):
        """Summary for empty collector raises ZeroDivisionError.

        Note: Current implementation divides by files_analyzed without checking
        for zero, causing ZeroDivisionError when no files have been analyzed.
        """
        with pytest.raises(ZeroDivisionError):
            metrics_collector.get_summary()

    def test_get_summary_populated(self, populated_metrics_collector):
        """Summary for populated collector."""
        summary = populated_metrics_collector.get_summary()
        assert summary["files"] == 3
        assert summary["functions"] == 16  # 5 + 3 + 8
        # avg = 16 / 3 ≈ 5.33
        assert summary["avg_fns_per_file"] == pytest.approx(16 / 3)

    def test_get_summary_returns_dict(self, populated_metrics_collector):
        """get_summary returns a dictionary."""
        summary = populated_metrics_collector.get_summary()
        assert isinstance(summary, dict)
