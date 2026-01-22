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

    def test_str_empty(self, empty_analysis_result):
        """__str__ shows 0 changes for empty results."""
        assert str(empty_analysis_result) == "Analysis Complete! There are 0 changes to implement"

    def test_str_populated(self, populated_analysis_result):
        """__str__ shows count of changes for populated results."""
        assert str(populated_analysis_result) == "Analysis Complete! There are 3 changes to implement"


@pytest.mark.analysis_result
class TestAnalysisResultLen:
    """Tests for AnalysisResult.__len__"""

    def test_len_empty(self, empty_analysis_result):
        """__len__ returns 0 for empty results."""
        assert len(empty_analysis_result) == 0

    def test_len_populated(self, populated_analysis_result):
        """__len__ returns count of findings."""
        assert len(populated_analysis_result) == 3


@pytest.mark.analysis_result
class TestAnalysisResultBool:
    """Tests for AnalysisResult.__bool__"""

    def test_bool_empty_is_false(self, empty_analysis_result):
        """__bool__ returns False for empty results."""
        assert bool(empty_analysis_result) is False

    def test_bool_populated_is_true(self, populated_analysis_result):
        """__bool__ returns True when findings exist."""
        assert bool(populated_analysis_result) is True


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

    def test_getitem_by_type_string(self, populated_analysis_result):
        """String key returns all findings of that type."""
        warnings = populated_analysis_result["warning"]
        assert len(warnings) == 1
        assert warnings[0]["message"] == "Too many functions"

    def test_getitem_by_type_returns_list(self, populated_analysis_result):
        """String key returns a list even for single match."""
        errors = populated_analysis_result["error"]
        assert isinstance(errors, list)
        assert len(errors) == 1

    def test_getitem_by_type_key_error(self, populated_analysis_result):
        """String key with no matches raises KeyError."""
        with pytest.raises(KeyError):
            _ = populated_analysis_result["nonexistent"]

    def test_getitem_invalid_type_raises(self, populated_analysis_result):
        """Non-int, non-str key raises TypeError."""
        with pytest.raises(TypeError):
            _ = populated_analysis_result[3.14]


@pytest.mark.analysis_result
class TestAnalysisResultIter:
    """Tests for AnalysisResult.__iter__"""

    def test_iter_empty(self, empty_analysis_result):
        """Iterating over empty results yields nothing."""
        items = list(empty_analysis_result)
        assert items == []

    def test_iter_populated(self, populated_analysis_result):
        """Iterating yields each finding in order."""
        items = list(populated_analysis_result)
        assert len(items) == 3
        assert items[0]["type"] == "warning"
        assert items[1]["type"] == "error"
        assert items[2]["type"] == "info"

    def test_iter_in_for_loop(self, populated_analysis_result):
        """Can use in for loop."""
        types = [item["type"] for item in populated_analysis_result]
        assert types == ["warning", "error", "info"]


@pytest.mark.analysis_result
class TestAnalysisResultAdd:
    """Tests for AnalysisResult.__add__"""

    def test_add_combines_results(self, empty_analysis_result, populated_analysis_result):
        """__add__ combines findings from both results."""
        combined = empty_analysis_result + populated_analysis_result
        assert len(combined) == 3

    def test_add_creates_new_instance(self, populated_analysis_result):
        """__add__ returns a new AnalysisResult, not modifying originals."""
        from ast_analyzer.classes.AnalysisResult import AnalysisResult
        other = AnalysisResult()
        other.results.append({"type": "warning", "message": "new warning"})
        combined = populated_analysis_result + other
        assert len(combined) == 4
        assert len(populated_analysis_result) == 3  # original unchanged
        assert len(other) == 1  # original unchanged

    def test_add_invalid_type_returns_not_implemented(self, empty_analysis_result):
        """__add__ returns NotImplemented for non-AnalysisResult types."""
        result = empty_analysis_result.__add__("not an AnalysisResult")
        assert result is NotImplemented
