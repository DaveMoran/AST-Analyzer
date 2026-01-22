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
        self.results: list[dict[str, Any]] = []

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"AnalysisResult(results={self.results})"

    def __str__(self) -> str:
        """Return a user-friendly summary of the analysis."""
        return f"Analysis Complete! There are {len(self)} changes to implement"

    def __len__(self) -> int:
        """Return the number of findings in the results."""
        return len(self.results)

    def __bool__(self) -> bool:
        """Return True if there are any findings, False otherwise."""
        return len(self.results) > 0

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
        combined.results = self.results + other.results
        return combined
