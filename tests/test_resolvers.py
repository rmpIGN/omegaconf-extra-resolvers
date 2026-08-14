"""Unit tests for resolver functions (direct calls, no OmegaConf registration)."""

from pathlib import Path

import pytest
from omegaconf import ListConfig

from omegaconf_extra_resolvers.resolvers import oc_coalesce
from omegaconf_extra_resolvers.resolvers import oc_len
from omegaconf_extra_resolvers.resolvers import oc_lpad
from omegaconf_extra_resolvers.resolvers import oc_pad
from omegaconf_extra_resolvers.resolvers import oc_rpad
from omegaconf_extra_resolvers.resolvers import oc_str2path


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


class TestPad:
    def test_right_pad_default(self):
        assert list(oc_pad([1, 2], 0, 5)) == [1, 2, 0, 0, 0]

    def test_right_pad_explicit(self):
        assert list(oc_pad([1, 2], 0, 5, "right")) == [1, 2, 0, 0, 0]

    def test_left_pad(self):
        assert list(oc_pad([1, 2], 0, 5, "left")) == [0, 0, 0, 1, 2]

    def test_no_padding_when_too_short_length(self):
        assert list(oc_pad([1, 2, 3], 0, 2)) == [1, 2, 3]

    def test_no_padding_when_exact_length(self):
        assert list(oc_pad([1, 2, 3], 0, 3)) == [1, 2, 3]

    def test_returns_list_config(self):
        assert isinstance(oc_pad([1, 2], 0, 4), ListConfig)

    def test_string_pad_value(self):
        assert list(oc_pad(["a"], "x", 3)) == ["a", "x", "x"]

    def test_pad_empty_list(self):
        assert list(oc_pad([], 0, 3)) == [0, 0, 0]


class TestLpad:
    def test_pads_on_left(self):
        assert list(oc_lpad([1, 2], 0, 5)) == [0, 0, 0, 1, 2]

    def test_returns_list_config(self):
        assert isinstance(oc_lpad([1], 0, 3), ListConfig)

    def test_no_padding_needed(self):
        assert list(oc_lpad([1, 2, 3], 0, 2)) == [1, 2, 3]


class TestRpad:
    def test_pads_on_right(self):
        assert list(oc_rpad([1, 2], 0, 5)) == [1, 2, 0, 0, 0]

    def test_returns_list_config(self):
        assert isinstance(oc_rpad([1], 0, 3), ListConfig)

    def test_no_padding_needed(self):
        assert list(oc_rpad([1, 2, 3], 0, 2)) == [1, 2, 3]


class TestLen:
    def test_list(self):
        assert oc_len([1, 2, 3]) == 3

    def test_string(self):
        assert oc_len("hello") == 5

    def test_empty_list(self):
        assert oc_len([]) == 0

    def test_tuple(self):
        assert oc_len((1, 2)) == 2

    def test_integer_raises(self):
        with pytest.raises(ValueError, match="no length property"):
            oc_len(42)

    def test_float_raises(self):
        with pytest.raises(ValueError, match="no length property"):
            oc_len(3.14)


class TestCoalesce:
    def test_returns_first_non_none(self):
        assert oc_coalesce([None, None, "a", "b"]) == "a"

    def test_first_item_non_none(self):
        assert oc_coalesce([1, 2, 3]) == 1

    def test_single_non_none(self):
        assert oc_coalesce([None, 42]) == 42

    def test_all_none_raises(self):
        with pytest.raises(ValueError, match="None"):
            oc_coalesce([None, None, None])

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="None"):
            oc_coalesce([])

    def test_not_iterable_raises(self):
        with pytest.raises(ValueError, match="not iterable"):
            oc_coalesce(42)
