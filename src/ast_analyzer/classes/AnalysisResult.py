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
        self.results: dict[str, Any] = {
            "warnings": [],
            "errors": [],
            "files": set(),
        }

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"AnalysisResult(results={self.results})"

    def __str__(self) -> str:
        """Return a user-friendly summary of the analysis."""
        if not self:
            return "Congrats! No errors or warnings found in directory"

        warnings_list = self._format_findings(self.results["warnings"])
        errors_list = self._format_findings(self.results["errors"])

        return f"""
Analysis Complete! There are {len(self)} changes to implement

Warnings: {len(self.results["warnings"])}
Errors: {len(self.results["errors"])}
Files to Change: {len(self.results["files"])}

Warnings:
{warnings_list}

Errors:
{errors_list}
"""

    def _format_findings(self, findings: list[dict[str, Any]]) -> str:
        """Format a list of findings as a bulleted list."""
        if not findings:
            return "  (none)"
        return "\n".join(f"  - {f['file']}: {f['message']}" for f in findings)

    def __len__(self) -> int:
        """Return the number of findings in the results."""
        return len(self.results["warnings"] + self.results["errors"])

    def __bool__(self) -> bool:
        """Return True if there are any findings, False otherwise."""
        return bool(self.results["warnings"] or self.results["errors"])

    def __getitem__(self, key: str) -> list[dict[str, Any]]:
        """
        Access findings by category.

        Args:
            key: "warnings" or "errors" to get that category's findings.

        Returns:
            List of findings for that category.

        Raises:
            KeyError: If key is not "warnings" or "errors".
        """
        if key in ("warnings", "errors"):
            return self.results[key]
        raise KeyError(f"Invalid key '{key}'. Use 'warnings' or 'errors'.")

    def __iter__(self) -> Iterator[dict[str, Any]]:
        """Iterate over all findings (warnings then errors)."""
        yield from self.results["warnings"]
        yield from self.results["errors"]

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
            "files": self.results["files"] | other.results["files"],
        }
        return combined

    def append_warning(self, message, filename):
        self.results["warnings"].append({"file": filename, "message": message})
        self.results["files"].add(filename)

    def append_error(self, message, filename):
        self.results["errors"].append({"file": filename, "message": message})
        self.results["files"].add(filename)
