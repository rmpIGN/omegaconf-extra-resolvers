"""Register extra OmegaConf resolvers provided by the package."""

from enum import Enum

from omegaconf import OmegaConf

from .resolvers import oc_coalesce
from .resolvers import oc_len
from .resolvers import oc_lpad
from .resolvers import oc_pad
from .resolvers import oc_rpad
from .resolvers import oc_str2path


class ResolverEnum(Enum):
    """Available extra OmegaConf resolvers.

    Each enum member stores the resolver name expected by OmegaConf and the
    callable implementing the resolver.
    """

    PAD = ("pad", oc_pad)
    LPAD = ("lpad", oc_lpad)
    RPAD = ("rpad", oc_rpad)
    PATH = ("path", oc_str2path)
    LEN = ("len", oc_len)
    COALESCE = ("coalesce", oc_coalesce)


def register(resolvers: list[ResolverEnum] | None = None, replace: bool = False):
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
