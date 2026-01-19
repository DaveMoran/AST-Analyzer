from pathlib import Path

import pytest

from ast_analyzer.generators.file_traversal import (
    filter_by_custom_matches,
    filter_by_gitignore,
    filter_python_files,
    get_working_files,
    read_from_directory,
    read_lines,
    skip_cache,
    skip_git,
    skip_virtual_envs,
)


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project structure for testing."""
    # Create directories
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / ".venv" / "lib").mkdir(parents=True)
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / ".git" / "objects").mkdir(parents=True)

    # Create Python files
    (tmp_path / "src" / "main.py").write_text("print('hello')")
    (tmp_path / "src" / "utils.py").write_text("def helper(): pass")
    (tmp_path / "tests" / "test_main.py").write_text("def test_main(): pass")

    # Create non-Python files
    (tmp_path / "README.md").write_text("# Project")
    (tmp_path / "config.json").write_text("{}")

    # Create files in ignored directories
    (tmp_path / ".venv" / "lib" / "module.py").write_text("# venv file")
    (tmp_path / "__pycache__" / "main.cpython-312.pyc").write_bytes(b"cache")
    (tmp_path / ".git" / "objects" / "abc123").write_bytes(b"git object")

    # Create .gitignore
    (tmp_path / ".gitignore").write_text("*.pyc\n__pycache__/\n.env\n# comment\n\n")

    return tmp_path


class TestReadFromDirectory:
    def test_returns_generator(self, temp_project):
        result = read_from_directory(str(temp_project))
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_finds_all_files(self, temp_project):
        files = list(read_from_directory(str(temp_project)))
        filenames = [f.name for f in files]

        assert "main.py" in filenames
        assert "README.md" in filenames
        assert "config.json" in filenames

    def test_only_returns_files_not_directories(self, temp_project):
        files = list(read_from_directory(str(temp_project)))

        for f in files:
            assert f.is_file()


class TestReadLines:
    def test_yields_lines_from_file(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\n")

        lines = list(read_lines(test_file))

        assert lines == ["line1\n", "line2\n", "line3\n"]

    def test_returns_generator(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = read_lines(test_file)

        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")


class TestFilterPythonFiles:
    def test_only_yields_python_files(self):
        files = [
            Path("main.py"),
            Path("README.md"),
            Path("utils.py"),
            Path("config.json"),
        ]

        result = list(filter_python_files(iter(files)))

        assert len(result) == 2
        assert Path("main.py") in result
        assert Path("utils.py") in result

    def test_empty_input_yields_nothing(self):
        result = list(filter_python_files(iter([])))
        assert result == []


class TestFilterByGitignore:
    def test_filters_files_matching_patterns(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("*.pyc\n*.log\n")

        files = [
            Path("main.py"),
            Path("cache.pyc"),
            Path("debug.log"),
            Path("utils.py"),
        ]

        result = list(filter_by_gitignore(iter(files), str(gitignore)))

        assert len(result) == 2
        assert Path("main.py") in result
        assert Path("utils.py") in result

    def test_filters_directory_patterns(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("__pycache__/\nbuild/\n")

        files = [
            Path("src/main.py"),
            Path("__pycache__/module.pyc"),
            Path("build/output.py"),
        ]

        result = list(filter_by_gitignore(iter(files), str(gitignore)))

        assert len(result) == 1
        assert Path("src/main.py") in result

    def test_ignores_comments_and_empty_lines(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("# This is a comment\n\n*.pyc\n")

        files = [Path("main.py"), Path("cache.pyc")]

        result = list(filter_by_gitignore(iter(files), str(gitignore)))

        assert len(result) == 1
        assert Path("main.py") in result

    def test_missing_gitignore_yields_all_files(self, tmp_path, caplog):
        files = [Path("main.py"), Path("utils.py")]

        result = list(filter_by_gitignore(iter(files), str(tmp_path / "nonexistent")))

        assert len(result) == 2
        assert "Could not read" in caplog.text


class TestFilterByCustomMatches:
    def test_filters_matching_paths(self):
        files = [
            Path("src/main.py"),
            Path("tests/test_main.py"),
            Path("tests/test_utils.py"),
        ]

        result = list(filter_by_custom_matches(iter(files), ["tests/"]))

        assert len(result) == 1
        assert Path("src/main.py") in result

    def test_none_matches_yields_all_files(self):
        files = [Path("main.py"), Path("utils.py")]

        result = list(filter_by_custom_matches(iter(files), None))

        assert len(result) == 2

    def test_empty_matches_yields_all_files(self):
        files = [Path("main.py"), Path("utils.py")]

        result = list(filter_by_custom_matches(iter(files), []))

        assert len(result) == 2


class TestSkipVirtualEnvs:
    def test_skips_venv_directories(self):
        files = [
            Path("src/main.py"),
            Path("venv/lib/python.py"),
            Path(".venv/bin/activate.py"),
            Path("env/lib/site.py"),
        ]

        result = list(skip_virtual_envs(iter(files)))

        assert len(result) == 1
        assert Path("src/main.py") in result

    def test_passes_non_venv_files(self):
        files = [Path("src/main.py"), Path("tests/test_main.py")]

        result = list(skip_virtual_envs(iter(files)))

        assert len(result) == 2


class TestSkipCache:
    def test_skips_cache_directories(self):
        files = [
            Path("src/main.py"),
            Path("__pycache__/main.cpython-312.pyc"),
            Path(".mypy_cache/cache.json"),
            Path(".pytest_cache/v/cache"),
            Path(".ruff_cache/content.json"),
        ]

        result = list(skip_cache(iter(files)))

        assert len(result) == 1
        assert Path("src/main.py") in result


class TestSkipGit:
    def test_skips_git_directory(self):
        files = [
            Path("src/main.py"),
            Path(".git/objects/abc123"),
            Path(".git/HEAD"),
        ]

        result = list(skip_git(iter(files)))

        assert len(result) == 1
        assert Path("src/main.py") in result


class TestGetWorkingFiles:
    def test_returns_only_python_files(self, temp_project):
        files = list(get_working_files(str(temp_project), gitignore_path=str(temp_project / ".gitignore")))
        extensions = {f.suffix for f in files}

        assert extensions == {".py"}

    def test_excludes_venv_files(self, temp_project):
        files = list(get_working_files(str(temp_project), gitignore_path=str(temp_project / ".gitignore")))
        paths_str = [str(f) for f in files]

        assert not any(".venv" in p for p in paths_str)

    def test_excludes_cache_files(self, temp_project):
        files = list(get_working_files(str(temp_project), gitignore_path=str(temp_project / ".gitignore")))
        paths_str = [str(f) for f in files]

        assert not any("__pycache__" in p for p in paths_str)

    def test_excludes_git_files(self, temp_project):
        files = list(get_working_files(str(temp_project), gitignore_path=str(temp_project / ".gitignore")))
        paths_str = [str(f) for f in files]

        assert not any(".git" in p for p in paths_str)

    def test_custom_matches_filter(self, temp_project):
        files = list(
            get_working_files(
                str(temp_project),
                custom_matches=["tests/"],
                gitignore_path=str(temp_project / ".gitignore"),
            )
        )
        paths_str = [str(f) for f in files]

        assert not any("tests/" in p for p in paths_str)
        assert any("src/" in p for p in paths_str)

    def test_returns_expected_source_files(self, temp_project):
        files = list(get_working_files(str(temp_project), gitignore_path=str(temp_project / ".gitignore")))
        filenames = [f.name for f in files]

        assert "main.py" in filenames
        assert "utils.py" in filenames
        assert "test_main.py" in filenames
