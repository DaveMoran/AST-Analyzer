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
        """Results dict initializes with empty warnings and errors."""
        assert empty_analysis_result.results["warnings"] == []
        assert empty_analysis_result.results["errors"] == []
        assert empty_analysis_result.results["files"] == set()

    def test_init_results_is_dict(self, empty_analysis_result):
        """Results attribute is a dict."""
        assert isinstance(empty_analysis_result.results, dict)


@pytest.mark.analysis_result
class TestAnalysisResultRepr:
    """Tests for AnalysisResult.__repr__"""

    def test_repr_empty(self, empty_analysis_result):
        """__repr__ shows empty results dict."""
        r = repr(empty_analysis_result)
        assert r.startswith("AnalysisResult(results={")
        assert "'warnings': []" in r
        assert "'errors': []" in r

    def test_repr_populated(self, populated_analysis_result):
        """__repr__ shows populated results dict."""
        r = repr(populated_analysis_result)
        assert r.startswith("AnalysisResult(results={")
        assert "warnings" in r
        assert "errors" in r


@pytest.mark.analysis_result
class TestAnalysisResultStr:
    """Tests for AnalysisResult.__str__"""

    def test_str_empty(self, empty_analysis_result):
        """__str__ shows congratulations message for empty results."""
        assert str(empty_analysis_result) == "Congrats! No errors or warnings found in directory"

    def test_str_populated(self, populated_analysis_result):
        """__str__ shows count of changes for populated results."""
        s = str(populated_analysis_result)
        assert "Analysis Complete!" in s
        assert "3 changes to implement" in s


@pytest.mark.analysis_result
class TestAnalysisResultLen:
    """Tests for AnalysisResult.__len__"""

    def test_len_empty(self, empty_analysis_result):
        """__len__ returns 0 for empty results."""
        assert len(empty_analysis_result) == 0

    def test_len_populated(self, populated_analysis_result):
        """__len__ returns count of warnings + errors."""
        assert len(populated_analysis_result) == 3  # 2 warnings + 1 error


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

    def test_getitem_warnings(self, populated_analysis_result):
        """'warnings' key returns warnings list."""
        warnings = populated_analysis_result["warnings"]
        assert isinstance(warnings, list)
        assert len(warnings) == 2

    def test_getitem_errors(self, populated_analysis_result):
        """'errors' key returns errors list."""
        errors = populated_analysis_result["errors"]
        assert isinstance(errors, list)
        assert len(errors) == 1

    def test_getitem_empty_warnings(self, empty_analysis_result):
        """Empty results returns empty warnings list."""
        warnings = empty_analysis_result["warnings"]
        assert warnings == []

    def test_getitem_empty_errors(self, empty_analysis_result):
        """Empty results returns empty errors list."""
        errors = empty_analysis_result["errors"]
        assert errors == []

    def test_getitem_invalid_key_raises(self, populated_analysis_result):
        """Invalid key raises KeyError."""
        with pytest.raises(KeyError):
            _ = populated_analysis_result["nonexistent"]


@pytest.mark.analysis_result
class TestAnalysisResultIter:
    """Tests for AnalysisResult.__iter__"""

    def test_iter_empty(self, empty_analysis_result):
        """Iterating over empty results yields nothing."""
        items = list(empty_analysis_result)
        assert items == []

    def test_iter_populated(self, populated_analysis_result):
        """Iterating yields all findings (warnings then errors)."""
        items = list(populated_analysis_result)
        assert len(items) == 3  # 2 warnings + 1 error

    def test_iter_in_for_loop(self, populated_analysis_result):
        """Can use in for loop."""
        count = 0
        for item in populated_analysis_result:
            assert "file" in item
            count += 1
        assert count == 3


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
        other.append_warning("new warning", "new_file.py")
        combined = populated_analysis_result + other
        assert len(combined) == 4
        assert len(populated_analysis_result) == 3  # original unchanged
        assert len(other) == 1  # original unchanged

    def test_add_invalid_type_returns_not_implemented(self, empty_analysis_result):
        """__add__ returns NotImplemented for non-AnalysisResult types."""
        result = empty_analysis_result.__add__("not an AnalysisResult")
        assert result is NotImplemented
