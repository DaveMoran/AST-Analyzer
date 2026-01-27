"""
ast_analyzer.utils

A list of helper functions that can be reused throughout the application
"""

import fnmatch
import logging
import os
import pathlib
import pathspec

from typing import Collection, Generator


def read_from_directory(directory: str) -> Generator[pathlib.Path, None, None]:
    dir_path = pathlib.Path(directory)
    if not dir_path.is_dir():
        logging.error(f"Directory {dir_path} is not a valid directory")
        return

    for file_path in dir_path.rglob("*"):
        try:
            if file_path.is_file() and os.access(file_path, os.R_OK):
                yield file_path
        except (PermissionError, OSError) as e:
            logging.warning(f"Cannot access {file_path}: {e}")


def read_lines(filepath: pathlib.Path) -> Generator[str, None, None]:
    with open(filepath) as f:
        for line in f:
            yield line


def filter_python_files(
    files: Generator[pathlib.Path, None, None],
) -> Generator[pathlib.Path, None, None]:
    for file in files:
        file_extension = file.suffix
        if file_extension == ".py":
            yield file


def filter_by_gitignore(files: Generator[pathlib.Path, None, None], ignore_file: str):
    gitignore_path = pathlib.Path(ignore_file)

    if not gitignore_path.exists():
        logging.warning("No gitignore file found. Returning all files")
        yield from files
        return

    lines = gitignore_path.read_text().splitlines()
    spec = pathspec.GitIgnoreSpec.from_lines(lines)

    for file in files:
        if not spec.match_file(str(file)):
            yield file


def filter_by_custom_matches(
    files: Generator[pathlib.Path, None, None], matches: Collection[str] | None
) -> Generator[pathlib.Path, None, None]:
    if not matches:
        yield from files
        return

    for file in files:
        full_path = str(file)
        if not any(match in full_path for match in matches):
            yield file


def skip_virtual_envs(
    files: Generator[pathlib.Path, None, None],
) -> Generator[pathlib.Path, None, None]:
    virtual_envs = ["venv/", ".venv/", "env/"]
    for file in files:
        full_path = str(file)
        if not any(env in full_path for env in virtual_envs):
            yield file


def skip_cache(files: Generator[pathlib.Path, None, None]) -> Generator[pathlib.Path, None, None]:
    caches = ["__pycache__/", ".mypy_cache/", ".pytest_cache/", ".ruff_cache/"]
    for file in files:
        full_path = str(file)
        if not any(cache in full_path for cache in caches):
            yield file


def skip_git(files: Generator[pathlib.Path, None, None]) -> Generator[pathlib.Path, None, None]:
    for file in files:
        full_path = str(file)
        if ".git" not in full_path:
            yield file


def get_working_files(
    directory: str,
    custom_matches: Collection[str] | None = None,
    gitignore_path: str = ".gitignore",
) -> Generator[pathlib.Path, None, None]:
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
                    filter_by_gitignore(filter_python_files(files), gitignore_path),
                    custom_matches,
                )
            )
        )
    )

    return filtered_files
