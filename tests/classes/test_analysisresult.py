"""
tests.classes.test_analysisresult

Test suite for the AnalysisResult container class.
"""

import pytest
from ast_analyzer.classes.AnalysisResult import AnalysisResult


# =============================================================================
# Initialization Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultInit:
    """Tests for AnalysisResult.__init__"""

    def test_init_creates_empty_warnings(self, empty_analysis_result):
        """Warnings list initializes empty."""
        assert empty_analysis_result.results["warnings"] == []

    def test_init_creates_empty_errors(self, empty_analysis_result):
        """Errors list initializes empty."""
        assert empty_analysis_result.results["errors"] == []

    def test_init_creates_empty_files_set(self, empty_analysis_result):
        """Files set initializes empty."""
        assert empty_analysis_result.results["files"] == set()

    def test_init_results_is_dict(self, empty_analysis_result):
        """Results attribute is a dict."""
        assert isinstance(empty_analysis_result.results, dict)

    def test_init_has_three_keys(self, empty_analysis_result):
        """Results dict has exactly three keys."""
        assert set(empty_analysis_result.results.keys()) == {"warnings", "errors", "files"}


# =============================================================================
# __repr__ Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultRepr:
    """Tests for AnalysisResult.__repr__"""

    def test_repr_starts_with_class_name(self, empty_analysis_result):
        """__repr__ starts with AnalysisResult class name."""
        assert repr(empty_analysis_result).startswith("AnalysisResult(")

    def test_repr_contains_results_key(self, empty_analysis_result):
        """__repr__ contains 'results=' key."""
        assert "results=" in repr(empty_analysis_result)

    def test_repr_shows_empty_warnings(self, empty_analysis_result):
        """__repr__ shows empty warnings list for empty results."""
        assert "'warnings': []" in repr(empty_analysis_result)

    def test_repr_shows_empty_errors(self, empty_analysis_result):
        """__repr__ shows empty errors list for empty results."""
        assert "'errors': []" in repr(empty_analysis_result)

    def test_repr_populated_contains_data(self, populated_analysis_result):
        """__repr__ shows populated data."""
        r = repr(populated_analysis_result)
        assert "warnings" in r
        assert "errors" in r


# =============================================================================
# __str__ Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultStr:
    """Tests for AnalysisResult.__str__"""

    def test_str_empty_shows_congrats(self, empty_analysis_result):
        """__str__ shows congratulations for empty results."""
        assert str(empty_analysis_result) == "Congrats! No errors or warnings found in directory"

    def test_str_populated_shows_analysis_complete(self, populated_analysis_result):
        """__str__ shows 'Analysis Complete!' header for populated results."""
        assert "Analysis Complete!" in str(populated_analysis_result)

    def test_str_populated_shows_change_count(self, populated_analysis_result):
        """__str__ shows total count of changes to implement."""
        assert "3 changes to implement" in str(populated_analysis_result)

    def test_str_populated_shows_warnings_count(self, populated_analysis_result):
        """__str__ shows warnings count."""
        assert "Warnings: 2" in str(populated_analysis_result)

    def test_str_populated_shows_errors_count(self, populated_analysis_result):
        """__str__ shows errors count."""
        assert "Errors: 1" in str(populated_analysis_result)

    def test_str_populated_shows_files_count(self, populated_analysis_result):
        """__str__ shows files to change count."""
        assert "Files to Change: 3" in str(populated_analysis_result)


# =============================================================================
# __len__ Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultLen:
    """Tests for AnalysisResult.__len__"""

    def test_len_empty_is_zero(self, empty_analysis_result):
        """__len__ returns 0 for empty results."""
        assert len(empty_analysis_result) == 0

    def test_len_counts_warnings_and_errors(self, populated_analysis_result):
        """__len__ returns sum of warnings and errors."""
        assert len(populated_analysis_result) == 3  # 2 warnings + 1 error

    def test_len_warnings_only(self):
        """__len__ counts warnings when no errors exist."""
        result = AnalysisResult()
        result.append_warning("warn1", "file1.py")
        result.append_warning("warn2", "file2.py")
        assert len(result) == 2

    def test_len_errors_only(self):
        """__len__ counts errors when no warnings exist."""
        result = AnalysisResult()
        result.append_error("err1", "file1.py")
        assert len(result) == 1


# =============================================================================
# __bool__ Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultBool:
    """Tests for AnalysisResult.__bool__"""

    def test_bool_empty_is_false(self, empty_analysis_result):
        """__bool__ returns False for empty results."""
        assert bool(empty_analysis_result) is False

    def test_bool_with_warnings_is_true(self):
        """__bool__ returns True when only warnings exist."""
        result = AnalysisResult()
        result.append_warning("warning", "file.py")
        assert bool(result) is True

    def test_bool_with_errors_is_true(self):
        """__bool__ returns True when only errors exist."""
        result = AnalysisResult()
        result.append_error("error", "file.py")
        assert bool(result) is True

    def test_bool_populated_is_true(self, populated_analysis_result):
        """__bool__ returns True when findings exist."""
        assert bool(populated_analysis_result) is True

    def test_bool_in_if_statement(self, empty_analysis_result, populated_analysis_result):
        """Can use AnalysisResult directly in if statements."""
        if empty_analysis_result:
            pytest.fail("Empty result should be falsy")
        if not populated_analysis_result:
            pytest.fail("Populated result should be truthy")


# =============================================================================
# __getitem__ Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultGetitem:
    """Tests for AnalysisResult.__getitem__"""

    def test_getitem_warnings_returns_list(self, populated_analysis_result):
        """Accessing 'warnings' returns a list."""
        assert isinstance(populated_analysis_result["warnings"], list)

    def test_getitem_errors_returns_list(self, populated_analysis_result):
        """Accessing 'errors' returns a list."""
        assert isinstance(populated_analysis_result["errors"], list)

    def test_getitem_warnings_count(self, populated_analysis_result):
        """Accessing 'warnings' returns correct count."""
        assert len(populated_analysis_result["warnings"]) == 2

    def test_getitem_errors_count(self, populated_analysis_result):
        """Accessing 'errors' returns correct count."""
        assert len(populated_analysis_result["errors"]) == 1

    def test_getitem_empty_warnings(self, empty_analysis_result):
        """Empty results returns empty warnings list."""
        assert empty_analysis_result["warnings"] == []

    def test_getitem_empty_errors(self, empty_analysis_result):
        """Empty results returns empty errors list."""
        assert empty_analysis_result["errors"] == []

    def test_getitem_invalid_key_raises_keyerror(self, populated_analysis_result):
        """Invalid key raises KeyError."""
        with pytest.raises(KeyError):
            _ = populated_analysis_result["invalid"]

    def test_getitem_files_key_raises_keyerror(self, populated_analysis_result):
        """'files' key is not accessible via __getitem__."""
        with pytest.raises(KeyError):
            _ = populated_analysis_result["files"]

    def test_getitem_keyerror_message(self, populated_analysis_result):
        """KeyError message is descriptive."""
        with pytest.raises(KeyError) as exc_info:
            _ = populated_analysis_result["bad_key"]
        assert "bad_key" in str(exc_info.value)
        assert "warnings" in str(exc_info.value) or "errors" in str(exc_info.value)


# =============================================================================
# __iter__ Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultIter:
    """Tests for AnalysisResult.__iter__"""

    def test_iter_empty_yields_nothing(self, empty_analysis_result):
        """Iterating over empty results yields nothing."""
        assert list(empty_analysis_result) == []

    def test_iter_yields_all_findings(self, populated_analysis_result):
        """Iterating yields all findings."""
        items = list(populated_analysis_result)
        assert len(items) == 3

    def test_iter_warnings_before_errors(self):
        """Warnings are yielded before errors."""
        result = AnalysisResult()
        result.append_error("error1", "file.py")
        result.append_warning("warning1", "file.py")
        items = list(result)
        # First item should be the warning (warnings come first)
        assert "warning1" in str(items[0].values())

    def test_iter_in_for_loop(self, populated_analysis_result):
        """Can iterate using for loop."""
        count = 0
        for item in populated_analysis_result:
            assert isinstance(item, dict)
            count += 1
        assert count == 3

    def test_iter_items_have_file_key(self, populated_analysis_result):
        """Each yielded item has 'file' key."""
        for item in populated_analysis_result:
            assert "file" in item


# =============================================================================
# __add__ Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultAdd:
    """Tests for AnalysisResult.__add__"""

    def test_add_two_empty_results(self, empty_analysis_result):
        """Adding two empty results yields empty result."""
        other = AnalysisResult()
        combined = empty_analysis_result + other
        assert len(combined) == 0

    def test_add_empty_to_populated(self, empty_analysis_result, populated_analysis_result):
        """Adding empty to populated preserves populated findings."""
        combined = empty_analysis_result + populated_analysis_result
        assert len(combined) == 3

    def test_add_populated_to_empty(self, empty_analysis_result, populated_analysis_result):
        """Adding populated to empty preserves populated findings."""
        combined = populated_analysis_result + empty_analysis_result
        assert len(combined) == 3

    def test_add_combines_warnings(self):
        """__add__ combines warnings from both results."""
        result1 = AnalysisResult()
        result1.append_warning("warn1", "file1.py")
        result2 = AnalysisResult()
        result2.append_warning("warn2", "file2.py")
        combined = result1 + result2
        assert len(combined["warnings"]) == 2

    def test_add_combines_errors(self):
        """__add__ combines errors from both results."""
        result1 = AnalysisResult()
        result1.append_error("err1", "file1.py")
        result2 = AnalysisResult()
        result2.append_error("err2", "file2.py")
        combined = result1 + result2
        assert len(combined["errors"]) == 2

    def test_add_combines_files(self):
        """__add__ combines files sets using union."""
        result1 = AnalysisResult()
        result1.append_warning("warn", "file1.py")
        result2 = AnalysisResult()
        result2.append_error("err", "file2.py")
        combined = result1 + result2
        assert combined.results["files"] == {"file1.py", "file2.py"}

    def test_add_creates_new_instance(self, populated_analysis_result):
        """__add__ returns a new AnalysisResult instance."""
        other = AnalysisResult()
        combined = populated_analysis_result + other
        assert combined is not populated_analysis_result
        assert combined is not other

    def test_add_does_not_modify_originals(self, populated_analysis_result):
        """__add__ does not modify original instances."""
        other = AnalysisResult()
        other.append_warning("new warning", "new.py")
        original_len = len(populated_analysis_result)
        _ = populated_analysis_result + other
        assert len(populated_analysis_result) == original_len

    def test_add_invalid_type_returns_not_implemented(self, empty_analysis_result):
        """__add__ returns NotImplemented for non-AnalysisResult types."""
        result = empty_analysis_result.__add__("not an AnalysisResult")
        assert result is NotImplemented

    def test_add_invalid_type_raises_typeerror(self, empty_analysis_result):
        """Adding non-AnalysisResult raises TypeError."""
        with pytest.raises(TypeError):
            _ = empty_analysis_result + "string"

    def test_add_invalid_type_list_raises_typeerror(self, empty_analysis_result):
        """Adding list raises TypeError."""
        with pytest.raises(TypeError):
            _ = empty_analysis_result + []


# =============================================================================
# append_warning Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultAppendWarning:
    """Tests for AnalysisResult.append_warning"""

    def test_append_warning_adds_to_warnings_list(self, empty_analysis_result):
        """append_warning adds item to warnings list."""
        empty_analysis_result.append_warning("Test warning", "test.py")
        assert len(empty_analysis_result["warnings"]) == 1

    def test_append_warning_adds_file_to_files_set(self, empty_analysis_result):
        """append_warning adds filename to files set."""
        empty_analysis_result.append_warning("Test warning", "test.py")
        assert "test.py" in empty_analysis_result.results["files"]

    def test_append_warning_creates_dict_with_file_key(self, empty_analysis_result):
        """append_warning creates dict with 'file' key."""
        empty_analysis_result.append_warning("Test warning", "test.py")
        warning = empty_analysis_result["warnings"][0]
        assert warning["file"] == "test.py"

    def test_append_warning_multiple(self, empty_analysis_result):
        """Can append multiple warnings."""
        empty_analysis_result.append_warning("warn1", "file1.py")
        empty_analysis_result.append_warning("warn2", "file2.py")
        empty_analysis_result.append_warning("warn3", "file3.py")
        assert len(empty_analysis_result["warnings"]) == 3

    def test_append_warning_same_file_multiple_times(self, empty_analysis_result):
        """Multiple warnings for same file only add file once to set."""
        empty_analysis_result.append_warning("warn1", "file.py")
        empty_analysis_result.append_warning("warn2", "file.py")
        assert len(empty_analysis_result.results["files"]) == 1


# =============================================================================
# append_error Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultAppendError:
    """Tests for AnalysisResult.append_error"""

    def test_append_error_adds_to_errors_list(self, empty_analysis_result):
        """append_error adds item to errors list."""
        empty_analysis_result.append_error("Test error", "test.py")
        assert len(empty_analysis_result["errors"]) == 1

    def test_append_error_adds_file_to_files_set(self, empty_analysis_result):
        """append_error adds filename to files set."""
        empty_analysis_result.append_error("Test error", "test.py")
        assert "test.py" in empty_analysis_result.results["files"]

    def test_append_error_creates_dict_with_file_key(self, empty_analysis_result):
        """append_error creates dict with 'file' key."""
        empty_analysis_result.append_error("Test error", "test.py")
        error = empty_analysis_result["errors"][0]
        assert error["file"] == "test.py"

    def test_append_error_multiple(self, empty_analysis_result):
        """Can append multiple errors."""
        empty_analysis_result.append_error("err1", "file1.py")
        empty_analysis_result.append_error("err2", "file2.py")
        assert len(empty_analysis_result["errors"]) == 2

    def test_append_error_same_file_multiple_times(self, empty_analysis_result):
        """Multiple errors for same file only add file once to set."""
        empty_analysis_result.append_error("err1", "file.py")
        empty_analysis_result.append_error("err2", "file.py")
        assert len(empty_analysis_result.results["files"]) == 1


# =============================================================================
# Integration Tests
# =============================================================================
@pytest.mark.analysis_result
class TestAnalysisResultIntegration:
    """Integration tests for AnalysisResult"""

    def test_mixed_warnings_and_errors_same_file(self):
        """Warnings and errors for same file share file entry."""
        result = AnalysisResult()
        result.append_warning("warning", "shared.py")
        result.append_error("error", "shared.py")
        assert len(result.results["files"]) == 1
        assert len(result) == 2

    def test_full_workflow(self):
        """Test typical usage workflow."""
        result = AnalysisResult()

        # Initially empty
        assert not result
        assert len(result) == 0

        # Add findings
        result.append_warning("Too many functions", "module.py")
        result.append_error("Syntax error", "parser.py")

        # Now has findings
        assert result
        assert len(result) == 2

        # Access by category
        assert len(result["warnings"]) == 1
        assert len(result["errors"]) == 1

        # Iterate
        all_findings = list(result)
        assert len(all_findings) == 2

    def test_combine_multiple_results(self):
        """Combine results from analyzing multiple modules."""
        result1 = AnalysisResult()
        result1.append_warning("warn1", "mod1.py")

        result2 = AnalysisResult()
        result2.append_error("err1", "mod2.py")

        result3 = AnalysisResult()
        result3.append_warning("warn2", "mod3.py")
        result3.append_error("err2", "mod3.py")

        combined = result1 + result2 + result3

        assert len(combined) == 4
        assert len(combined["warnings"]) == 2
        assert len(combined["errors"]) == 2
        assert len(combined.results["files"]) == 3
