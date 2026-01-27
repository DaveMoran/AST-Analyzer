import pathlib

import pytest

from ast_analyzer.generators import file_traversal


class TestReadFromDirectory:
    def test_returns_generator(self, temp_project):
        result = file_traversal.read_from_directory(str(temp_project))
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_finds_all_files(self, temp_project):
        files = list(file_traversal.read_from_directory(str(temp_project)))
        filenames = [f.name for f in files]

        assert "main.py" in filenames
        assert "README.md" in filenames
        assert "config.json" in filenames

    def test_only_returns_files_not_directories(self, temp_project):
        files = list(file_traversal.read_from_directory(str(temp_project)))

        for f in files:
            assert f.is_file()


class TestReadLines:
    def test_yields_lines_from_file(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\n")

        lines = list(file_traversal.read_lines(test_file))

        assert lines == ["line1\n", "line2\n", "line3\n"]

    def test_returns_generator(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = file_traversal.read_lines(test_file)

        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")


class TestFilterPythonFiles:
    def test_only_yields_python_files(self):
        files = [
            pathlib.Path("main.py"),
            pathlib.Path("README.md"),
            pathlib.Path("utils.py"),
            pathlib.Path("config.json"),
        ]

        result = list(file_traversal.filter_python_files(iter(files)))

        assert len(result) == 2
        assert pathlib.Path("main.py") in result
        assert pathlib.Path("utils.py") in result

    def test_empty_input_yields_nothing(self):
        result = list(file_traversal.filter_python_files(iter([])))
        assert result == []


class TestFilterByGitignore:
    def test_filters_files_matching_patterns(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("*.pyc\n*.log\n")

        files = [
            pathlib.Path("main.py"),
            pathlib.Path("cache.pyc"),
            pathlib.Path("debug.log"),
            pathlib.Path("utils.py"),
        ]

        result = list(file_traversal.filter_by_gitignore(iter(files), str(gitignore)))

        assert len(result) == 2
        assert pathlib.Path("main.py") in result
        assert pathlib.Path("utils.py") in result

    def test_filters_directory_patterns(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("__pycache__/\nbuild/\n")

        files = [
            pathlib.Path("src/main.py"),
            pathlib.Path("__pycache__/module.pyc"),
            pathlib.Path("build/output.py"),
        ]

        result = list(file_traversal.filter_by_gitignore(iter(files), str(gitignore)))

        assert len(result) == 1
        assert pathlib.Path("src/main.py") in result

    def test_ignores_comments_and_empty_lines(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("# This is a comment\n\n*.pyc\n")

        files = [pathlib.Path("main.py"), pathlib.Path("cache.pyc")]

        result = list(file_traversal.filter_by_gitignore(iter(files), str(gitignore)))

        assert len(result) == 1
        assert pathlib.Path("main.py") in result

    def test_missing_gitignore_yields_all_files(self, tmp_path, caplog):
        files = [pathlib.Path("main.py"), pathlib.Path("utils.py")]

        result = list(file_traversal.filter_by_gitignore(iter(files), str(tmp_path / "nonexistent")))

        assert len(result) == 2
        assert "No gitignore file found" in caplog.text

    def test_works_with_relative_paths(self, tmp_path):
        """Verify pathspec matching works correctly with relative paths."""
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("*.pyc\n__pycache__/\nnode_modules/\n")

        # Relative paths (as would come from rglob with a relative base)
        files = [
            pathlib.Path("src/main.py"),
            pathlib.Path("src/__pycache__/main.cpython-312.pyc"),
            pathlib.Path("node_modules/package/index.js"),
            pathlib.Path("tests/test_main.py"),
        ]

        result = list(file_traversal.filter_by_gitignore(iter(files), str(gitignore)))

        assert pathlib.Path("src/main.py") in result
        assert pathlib.Path("tests/test_main.py") in result
        assert pathlib.Path("src/__pycache__/main.cpython-312.pyc") not in result
        assert pathlib.Path("node_modules/package/index.js") not in result

    def test_works_with_absolute_paths(self, tmp_path):
        """Verify pathspec matching works with absolute paths."""
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("*.pyc\n__pycache__/\n")

        # Absolute paths (as would come from rglob with an absolute base)
        files = [
            tmp_path / "src" / "main.py",
            tmp_path / "src" / "__pycache__" / "main.cpython-312.pyc",
            tmp_path / "tests" / "test_main.py",
        ]

        result = list(file_traversal.filter_by_gitignore(iter(files), str(gitignore)))
        result_names = [f.name for f in result]

        assert "main.py" in result_names
        assert "test_main.py" in result_names
        # This checks if pathspec handles absolute paths correctly
        assert "main.cpython-312.pyc" not in result_names


class TestFilterByCustomMatches:
    def test_filters_matching_paths(self):
        files = [
            pathlib.Path("src/main.py"),
            pathlib.Path("tests/test_main.py"),
            pathlib.Path("tests/test_utils.py"),
        ]

        result = list(file_traversal.filter_by_custom_matches(iter(files), ["tests/"]))

        assert len(result) == 1
        assert pathlib.Path("src/main.py") in result

    def test_none_matches_yields_all_files(self):
        files = [pathlib.Path("main.py"), pathlib.Path("utils.py")]

        result = list(file_traversal.filter_by_custom_matches(iter(files), None))

        assert len(result) == 2

    def test_empty_matches_yields_all_files(self):
        files = [pathlib.Path("main.py"), pathlib.Path("utils.py")]

        result = list(file_traversal.filter_by_custom_matches(iter(files), []))

        assert len(result) == 2


class TestSkipVirtualEnvs:
    def test_skips_venv_directories(self):
        files = [
            pathlib.Path("src/main.py"),
            pathlib.Path("venv/lib/python.py"),
            pathlib.Path(".venv/bin/activate.py"),
            pathlib.Path("env/lib/site.py"),
        ]

        result = list(file_traversal.skip_virtual_envs(iter(files)))

        assert len(result) == 1
        assert pathlib.Path("src/main.py") in result

    def test_passes_non_venv_files(self):
        files = [pathlib.Path("src/main.py"), pathlib.Path("tests/test_main.py")]

        result = list(file_traversal.skip_virtual_envs(iter(files)))

        assert len(result) == 2


class TestSkipCache:
    def test_skips_cache_directories(self):
        files = [
            pathlib.Path("src/main.py"),
            pathlib.Path("__pycache__/main.cpython-312.pyc"),
            pathlib.Path(".mypy_cache/cache.json"),
            pathlib.Path(".pytest_cache/v/cache"),
            pathlib.Path(".ruff_cache/content.json"),
        ]

        result = list(file_traversal.skip_cache(iter(files)))

        assert len(result) == 1
        assert pathlib.Path("src/main.py") in result


class TestSkipGit:
    def test_skips_git_directory(self):
        files = [
            pathlib.Path("src/main.py"),
            pathlib.Path(".git/objects/abc123"),
            pathlib.Path(".git/HEAD"),
        ]

        result = list(file_traversal.skip_git(iter(files)))

        assert len(result) == 1
        assert pathlib.Path("src/main.py") in result


class TestGetWorkingFiles:
    def test_returns_only_python_files(self, temp_project):
        files = list(
            file_traversal.get_working_files(str(temp_project), gitignore_path=str(temp_project / ".gitignore"))
        )
        extensions = {f.suffix for f in files}

        assert extensions == {".py"}

    def test_excludes_venv_files(self, temp_project):
        files = list(
            file_traversal.get_working_files(str(temp_project), gitignore_path=str(temp_project / ".gitignore"))
        )
        paths_str = [str(f) for f in files]

        assert not any(".venv" in p for p in paths_str)

    def test_excludes_cache_files(self, temp_project):
        files = list(
            file_traversal.get_working_files(str(temp_project), gitignore_path=str(temp_project / ".gitignore"))
        )
        paths_str = [str(f) for f in files]

        assert not any("__pycache__" in p for p in paths_str)

    def test_excludes_git_files(self, temp_project):
        files = list(
            file_traversal.get_working_files(str(temp_project), gitignore_path=str(temp_project / ".gitignore"))
        )
        paths_str = [str(f) for f in files]

        assert not any(".git" in p for p in paths_str)

    def test_custom_matches_filter(self, temp_project):
        files = list(
            file_traversal.get_working_files(
                str(temp_project),
                custom_matches=["tests/"],
                gitignore_path=str(temp_project / ".gitignore"),
            )
        )
        paths_str = [str(f) for f in files]

        assert not any("tests/" in p for p in paths_str)
        assert any("src/" in p for p in paths_str)

    def test_returns_expected_source_files(self, temp_project):
        files = list(
            file_traversal.get_working_files(str(temp_project), gitignore_path=str(temp_project / ".gitignore"))
        )
        filenames = [f.name for f in files]

        assert "main.py" in filenames
        assert "utils.py" in filenames
        assert "test_main.py" in filenames
