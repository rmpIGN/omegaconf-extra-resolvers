"""Register extra OmegaConf resolvers provided by the package."""

from enum import Enum

from omegaconf import OmegaConf

from omegaconf_extra_resolvers.resolvers.list import oc_coalesce
from omegaconf_extra_resolvers.resolvers.list import oc_len
from omegaconf_extra_resolvers.resolvers.list import oc_lpad
from omegaconf_extra_resolvers.resolvers.list import oc_pad
from omegaconf_extra_resolvers.resolvers.list import oc_range
from omegaconf_extra_resolvers.resolvers.list import oc_rpad
from omegaconf_extra_resolvers.resolvers.os import oc_glob
from omegaconf_extra_resolvers.resolvers.os import oc_str2path
from omegaconf_extra_resolvers.resolvers.string import oc_lower
from omegaconf_extra_resolvers.resolvers.string import oc_upper


class ResolverEnum(Enum):
    """Available extra OmegaConf resolvers.

    Each enum member stores the resolver name expected by OmegaConf and the
    callable implementing the resolver.
    """

    # OS
    PATH = ("path", oc_str2path)
    GLOB = ("glob", oc_glob)

    # List
    PAD = ("pad", oc_pad)
    LPAD = ("lpad", oc_lpad)
    RPAD = ("rpad", oc_rpad)
    LEN = ("len", oc_len)
    COALESCE = ("coalesce", oc_coalesce)
    RANGE = ("range", oc_range)

    # String
    LOWER = ("lower", oc_lower)
    UPPER = ("upper", oc_upper)


def oc_register_extra_resolvers(
    resolvers: list[ResolverEnum] | None = None, replace: bool = False
):
    """Register extra resolvers in OmegaConf.

    Parameters
    ----------
    resolvers : list[ResolverEnum] or None, optional
        Resolvers to register. When ``None``, all resolvers defined in
        ``ResolverEnum`` are registered.
    replace : bool, optional
        Requested replacement behavior for existing resolvers.

    Returns
    -------
    None
        This function registers resolvers for their side effects only.
    """
    if resolvers is None:
        resolvers = list(ResolverEnum)
    for r in resolvers:
        OmegaConf.register_new_resolver(
            name=r.value[0], resolver=r.value[1], replace=replace
        )
