"""
ast_analyzer.utils

A list of helper functions that can be reused throughout the application
"""

import fnmatch
import logging
import os

from pathlib import Path
from typing import Generator, Collection


def read_from_directory(directory: str) -> Generator[Path, None, None]:
    try:
        filenames = (
            file_path
            for file_path in Path(directory).rglob("*", followlinks=False)
            if os.access(str(file_path), os.R_OK) and file_path.is_file()
        )
        return filenames
    except:
        logging.exception(
            "Warning, you do not have permission to view one of these files "
        )


def read_lines(filepath: Path) -> Generator[str, None, None]:
    with open(filepath) as f:
        for line in f:
            yield line


def filter_python_files(
    files: Generator[Path, None, None],
) -> Generator[Path, None, None]:
    for file in files:
        file_extension = file.suffix
        if file_extension == ".py":
            yield file


def filter_by_gitignore(files: Generator[Path, None, None], ignore_file: str):
    patterns = []

    try:
        with open(ignore_file, "r") as f:
            gen_gitignore = f.readlines()

        for line in gen_gitignore:
            pattern = line.strip()
            if pattern and not pattern.startswith("#"):
                patterns.append(pattern)

    except (FileNotFoundError, PermissionError):
        # No .gitignore or can't read it - yield all files
        logging.warning(f"Could not read {ignore_file}, skipping gitignore filtering")
        yield from files
        return

    for file in files:
        is_match = False
        relative_path = str(file)

        for pattern in patterns:
            # Handle directory patterns (ending with /)
            if pattern.endswith("/"):
                # Check if any part of the path contains this directory
                if (
                    pattern[:-1] in relative_path
                    or f"/{pattern[:-1]}/" in relative_path
                ):
                    is_match = True
                    break
            # Match against filename
            elif fnmatch.fnmatch(file.name, pattern):
                is_match = True
                break
            # Match against full relative path for patterns with /
            elif "/" in pattern and fnmatch.fnmatch(relative_path, pattern):
                is_match = True
                break

        if not is_match:
            yield file


def filter_by_custom_matches(
    files: Generator[Path, None, None], matches: Collection[str] | None
) -> Generator[Path, None, None]:
    if not matches:
        yield from files
        return

    for file in files:
        full_path = str(file)
        if not any(match in full_path for match in matches):
            yield file


def skip_virtual_envs(
    files: Generator[Path, None, None],
) -> Generator[Path, None, None]:
    virtual_envs = ["venv/", ".venv/", "env/"]
    for file in files:
        full_path = str(file)
        if not any(env in full_path for env in virtual_envs):
            yield file


def skip_cache(files: Generator[Path, None, None]) -> Generator[Path, None, None]:
    caches = ["__pycache__/", ".mypy_cache/", ".pytest_cache/", ".ruff_cache/"]
    for file in files:
        full_path = str(file)
        if not any(cache in full_path for cache in caches):
            yield file


def skip_git(files: Generator[Path, None, None]) -> Generator[Path, None, None]:
    for file in files:
        full_path = str(file)
        if ".git" not in full_path:
            yield file


def get_working_files(
    directory: str,
    custom_matches: Collection[str] | None = None,
    gitignore_path: str = ".gitignore",
) -> Generator[Path, None, None]:
    """Parent generator for getting a final list of files to traverse

    Using a number of generators, this function traverses a parent directory and
    pulls out all relevant files that we want to test our AST_Analyzer against

    Args:
        directory | str: Parent directory to grab all files from
        custom_matches | Collection: Custom strings to check file names against

    Example:
        >>> curr_python_files = get_working_files('./')

        >>> curr_python_files_no_tests = get_working_files('./', ['test/', 'tests/'])
    """
    files = read_from_directory(directory)

    filtered_files = skip_git(
        skip_cache(
            skip_virtual_envs(
                filter_by_custom_matches(
                    filter_python_files(filter_by_gitignore(files, gitignore_path)),
                    custom_matches,
                )
            )
        )
    )

    return filtered_files
