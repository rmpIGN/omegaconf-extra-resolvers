"""Unit tests for resolvers.os (direct calls, no OmegaConf registration)."""

from pathlib import Path

import pytest
from omegaconf import ListConfig

from omegaconf_extra_resolvers.resolvers.os import oc_glob
from omegaconf_extra_resolvers.resolvers.os import oc_str2path


class TestStr2Path:
    def test_absolute_path(self):
        assert oc_str2path("/some/path") == Path("/some/path")

    def test_relative_path(self):
        assert oc_str2path("relative/path") == Path("relative/path")

    def test_returns_path_instance(self):
        assert isinstance(oc_str2path("/foo"), Path)

    def test_check_exist_true_existing_file(self, tmp_path):
        f = tmp_path / "file.txt"
        f.touch()
        assert oc_str2path(str(f), check_exist=True) == f

    def test_check_exist_true_existing_dir(self, tmp_path):
        assert oc_str2path(str(tmp_path), check_exist=True) == tmp_path

    def test_check_exist_true_missing_raises(self, tmp_path):
        missing = tmp_path / "missing.txt"
        with pytest.raises(FileNotFoundError):
            oc_str2path(str(missing), check_exist=True)

    def test_check_exist_false_missing_ok(self, tmp_path):
        missing = tmp_path / "missing.txt"
        assert oc_str2path(str(missing), check_exist=False) == missing

    def test_check_exist_defaults_to_false(self, tmp_path):
        missing = tmp_path / "missing.txt"
        assert oc_str2path(str(missing)) == missing


class TestGlob:
    def test_finds_matching_files(self, tmp_path):
        (tmp_path / "a.txt").touch()
        (tmp_path / "b.txt").touch()
        result = sorted(oc_glob(str(tmp_path), "*.txt"))
        assert result == sorted([str(tmp_path / "a.txt"), str(tmp_path / "b.txt")])

    def test_no_match_returns_empty(self, tmp_path):
        assert list(oc_glob(str(tmp_path), "*.tif")) == []

    def test_missing_root_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            oc_glob(str(tmp_path / "missing"), "*.txt")

    def test_returns_list_config(self, tmp_path):
        assert isinstance(oc_glob(str(tmp_path), "*"), ListConfig)

    def test_returns_strings(self, tmp_path):
        (tmp_path / "file.txt").touch()
        assert all(isinstance(s, str) for s in oc_glob(str(tmp_path), "*.txt"))
