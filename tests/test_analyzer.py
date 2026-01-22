"""
tests.test_analyzer
"""

import pytest


# =============================================================================
# AnalysisResult Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultInit:
    """Tests for AnalysisResult.__init__"""

    def test_init_creates_empty_results(self, empty_analysis_result):
        """Results list initializes empty."""
        assert empty_analysis_result.results == []

    def test_init_results_is_list(self, empty_analysis_result):
        """Results attribute is a list."""
        assert isinstance(empty_analysis_result.results, list)


@pytest.mark.analysis_result
class TestAnalysisResultRepr:
    """Tests for AnalysisResult.__repr__"""

    def test_repr_empty(self, empty_analysis_result):
        """__repr__ shows empty results list."""
        assert repr(empty_analysis_result) == "AnalysisResult(results=[])"

    def test_repr_populated(self, populated_analysis_result):
        """__repr__ shows populated results list."""
        r = repr(populated_analysis_result)
        assert r.startswith("AnalysisResult(results=[")
        assert "warning" in r
        assert "error" in r


@pytest.mark.analysis_result
class TestAnalysisResultStr:
    """Tests for AnalysisResult.__str__"""

    def test_str_raises_not_implemented(self, empty_analysis_result):
        """__str__ raises NotImplementedError because it calls __len__.

        Note: __str__ uses len(self) internally, which raises NotImplementedError.
        This is expected behavior until ASTANA-6 implements __len__.
        """
        with pytest.raises(NotImplementedError):
            str(empty_analysis_result)

    def test_str_raises_with_populated_results(self, populated_analysis_result):
        """__str__ raises NotImplementedError even with results."""
        with pytest.raises(NotImplementedError):
            str(populated_analysis_result)


@pytest.mark.analysis_result
class TestAnalysisResultLen:
    """Tests for AnalysisResult.__len__"""

    def test_len_raises_not_implemented(self, empty_analysis_result):
        """__len__ raises NotImplementedError (ASTANA-6 work)."""
        with pytest.raises(NotImplementedError):
            len(empty_analysis_result)


@pytest.mark.analysis_result
class TestAnalysisResultBool:
    """Tests for AnalysisResult.__bool__"""

    def test_bool_raises_not_implemented(self, empty_analysis_result):
        """__bool__ raises NotImplementedError (ASTANA-6 work)."""
        with pytest.raises(NotImplementedError):
            bool(empty_analysis_result)


@pytest.mark.analysis_result
class TestAnalysisResultGetitem:
    """Tests for AnalysisResult.__getitem__"""

    def test_getitem_valid_index(self, populated_analysis_result):
        """Valid index returns the result item."""
        item = populated_analysis_result[0]
        assert item["type"] == "warning"

    def test_getitem_negative_index(self, populated_analysis_result):
        """Negative index returns from end."""
        item = populated_analysis_result[-1]
        assert item["type"] == "info"

    def test_getitem_index_error(self, populated_analysis_result):
        """Out of range index raises IndexError."""
        with pytest.raises(IndexError):
            _ = populated_analysis_result[100]

    def test_getitem_empty_raises(self, empty_analysis_result):
        """Indexing empty results raises IndexError."""
        with pytest.raises(IndexError):
            _ = empty_analysis_result[0]


@pytest.mark.analysis_result
class TestAnalysisResultAdd:
    """Tests for AnalysisResult.__add__"""

    def test_add_raises_not_implemented(self, empty_analysis_result, populated_analysis_result):
        """__add__ raises NotImplementedError (ASTANA-6 work)."""
        with pytest.raises(NotImplementedError):
            _ = empty_analysis_result + populated_analysis_result
