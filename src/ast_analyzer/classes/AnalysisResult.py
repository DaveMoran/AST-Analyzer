from __future__ import annotations
from typing import Any, Iterator


class AnalysisResult:
    """
    Container for code analysis findings.

    Takes all of the findings from the CodeAnalyzer class and provides
    an intuitive interface for working with analysis data.

    Attributes:
        results: List of finding dictionaries, each containing 'type' and 'message' keys.

    Examples:
        >>> result = AnalysisResult()
        >>> result.results.append({"type": "warning", "message": "Too many functions"})
        >>> len(result)
        1
        >>> bool(result)
        True
        >>> for finding in result:
        ...     print(finding["message"])
        Too many functions
    """

    def __init__(self) -> None:
        """Initialize an empty AnalysisResult with no findings."""
        self.results: list[dict[str, Any]] = {"warnings": [], "errors": []}

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"AnalysisResult(results={self.results})"

    def __str__(self) -> str:
        """Return a user-friendly summary of the analysis."""
        if self:
            return "Congrats! No errors or warnings found in directory"
        else:
            return f"""
            Analysis Complete! There are {len(self)} changes to implement

            Warnings: {len(self.results['warnings'])}
            Errors: {len(self.results['errors'])}
            """

    def __len__(self) -> int:
        """Return the number of findings in the results."""
        return len(self.results)

    def __bool__(self) -> bool:
        """Return True if there are any findings, False otherwise."""
        return len(self.results) > 0

    def __getitem__(self, key: int | str) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Access findings by index or by type.

        When given an integer, returns the finding at that index.
        When given a string, returns all findings matching that type.
        """
        if isinstance(key, int):
            return self.results[key]
        elif isinstance(key, str):
            matches = [r for r in self.results if r.get("type") == key]
            if not matches:
                raise KeyError(f"No findings of type '{key}'")
            return matches
        else:
            raise TypeError(f"Key must be int or str, not {type(key).__name__}")

    def __iter__(self) -> Iterator[dict[str, Any]]:
        """Iterate over all findings in the results."""
        return iter(self.results)

    def __add__(self, other: AnalysisResult) -> AnalysisResult:
        """
        Combine results from multiple analyses.

        Creates a new AnalysisResult containing findings from both
        this result and the other result.
        """
        if not isinstance(other, AnalysisResult):
            return NotImplemented
        combined = AnalysisResult()
        combined.results = {
            "warnings": self.results["warnings"] + other.results["warnings"],
            "errors": self.results["errors"] + other.results["errors"],
        }
        return combined

    def append_warning(self, message):
        self.results["warnings"].append({"file": "TODO", message: message})

    def append_error(self, message):
        self.results["errors"].append({"file": "TODO", message: message})
