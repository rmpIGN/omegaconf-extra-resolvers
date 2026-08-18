"""Unit tests for resolvers.list (direct calls, no OmegaConf registration)."""

import pytest
from omegaconf import ListConfig

from omegaconf_extra_resolvers.resolvers.list import oc_coalesce
from omegaconf_extra_resolvers.resolvers.list import oc_len
from omegaconf_extra_resolvers.resolvers.list import oc_lpad
from omegaconf_extra_resolvers.resolvers.list import oc_pad
from omegaconf_extra_resolvers.resolvers.list import oc_range
from omegaconf_extra_resolvers.resolvers.list import oc_rpad


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


class TestRange:
    def test_basic(self):
        assert list(oc_range(0, 5)) == [0, 1, 2, 3, 4]

    def test_with_step(self):
        assert list(oc_range(0, 10, 2)) == [0, 2, 4, 6, 8]

    def test_with_start_offset(self):
        assert list(oc_range(2, 6)) == [2, 3, 4, 5]

    def test_empty_range(self):
        assert list(oc_range(5, 5)) == []

    def test_returns_list_config(self):
        assert isinstance(oc_range(0, 3), ListConfig)
