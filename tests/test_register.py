"""Integration tests for resolver registration and OmegaConf interpolation."""

from pathlib import Path

import pytest
from omegaconf import OmegaConf

from omegaconf_extra_resolvers import ResolverEnum
from omegaconf_extra_resolvers import oc_register_extra_resolvers


@pytest.fixture(autouse=True)
def registered():
    oc_register_extra_resolvers(replace=True)


class TestRegisterAll:
    def test_all_resolvers_by_default(self):
        registered_names = {r.value[0] for r in ResolverEnum}
        assert registered_names == {
            "pad",
            "lpad",
            "rpad",
            "path",
            "len",
            "coalesce",
            "range",
            "glob",
            "upper",
            "lower",
        }

    def test_path_resolver(self):
        cfg = OmegaConf.create({"p": "${path:/some/path}"})
        assert cfg.p == Path("/some/path")

    def test_len_resolver(self):
        cfg = OmegaConf.create({"items": [1, 2, 3], "n": "${len:${items}}"})
        assert cfg.n == 3

    def test_rpad_resolver(self):
        cfg = OmegaConf.create({"items": [1, 2], "padded": "${rpad:${items},0,5}"})
        assert list(cfg.padded) == [1, 2, 0, 0, 0]

    def test_lpad_resolver(self):
        cfg = OmegaConf.create({"items": [1, 2], "padded": "${lpad:${items},0,5}"})
        assert list(cfg.padded) == [0, 0, 0, 1, 2]

    def test_pad_resolver_right_default(self):
        cfg = OmegaConf.create({"items": [1, 2], "padded": "${pad:${items},0,5}"})
        assert list(cfg.padded) == [1, 2, 0, 0, 0]

    def test_coalesce_resolver(self):
        cfg = OmegaConf.create(
            {"items": [None, None, "hello"], "result": "${coalesce:${items}}"}
        )
        assert cfg.result == "hello"

    def test_range_resolver(self):
        cfg = OmegaConf.create({"epochs": "${range:0,6,2}"})
        assert list(cfg.epochs) == [0, 2, 4]

    def test_glob_resolver(self, tmp_path):
        (tmp_path / "img.tif").touch()
        cfg = OmegaConf.create({"files": "${glob:" + str(tmp_path) + ",*.tif}"})
        assert list(cfg.files) == [str(tmp_path / "img.tif")]

    def test_upper_resolver(self):
        cfg = OmegaConf.create({"tag": "${upper:resnet50}"})
        assert cfg.tag == "RESNET50"

    def test_lower_resolver(self):
        cfg = OmegaConf.create({"env": "${lower:PRODUCTION}"})
        assert cfg.env == "production"


class TestRegisterSubset:
    def test_register_single_resolver(self):
        oc_register_extra_resolvers([ResolverEnum.LEN], replace=True)
        cfg = OmegaConf.create({"items": [1, 2, 3], "n": "${len:${items}}"})
        assert cfg.n == 3

    def test_register_multiple_resolvers(self):
        oc_register_extra_resolvers([ResolverEnum.PATH, ResolverEnum.LEN], replace=True)
        cfg = OmegaConf.create(
            {"p": "${path:/foo}", "items": [1], "n": "${len:${items}}"}
        )
        assert cfg.p == Path("/foo")
        assert cfg.n == 1

    def test_replace_false_raises_on_duplicate(self):
        oc_register_extra_resolvers([ResolverEnum.LEN], replace=True)
        with pytest.raises(Exception):
            oc_register_extra_resolvers([ResolverEnum.LEN], replace=False)
