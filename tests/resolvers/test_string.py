"""Unit tests for resolvers.string (direct calls, no OmegaConf registration)."""

from omegaconf_extra_resolvers.resolvers.string import oc_lower
from omegaconf_extra_resolvers.resolvers.string import oc_upper


class TestUpper:
    def test_lower_to_upper(self):
        assert oc_upper("hello") == "HELLO"

    def test_already_upper(self):
        assert oc_upper("HELLO") == "HELLO"

    def test_mixed_case(self):
        assert oc_upper("Hello World") == "HELLO WORLD"


class TestLower:
    def test_upper_to_lower(self):
        assert oc_lower("HELLO") == "hello"

    def test_already_lower(self):
        assert oc_lower("hello") == "hello"

    def test_mixed_case(self):
        assert oc_lower("Hello World") == "hello world"
