from errno import ENOENT
from os import strerror
from pathlib import Path

from omegaconf import ListConfig
from omegaconf import OmegaConf


def oc_str2path(value: str, check_exist: bool = False) -> Path:
    """Convert a string value to a path.

    Parameters
    ----------
    value : str
        String representation of the path.
    check_exist : bool, optional
        Whether to require the path to exist before returning it.

    Returns
    -------
    pathlib.Path
        Path built from ``value``.

    Raises
    ------
    FileNotFoundError
        If ``check_exist`` is ``True`` and the path does not exist.
    """
    p = Path(value)
    if check_exist and not p.exists():
        raise FileNotFoundError(ENOENT, strerror(ENOENT), p)
    return p


def oc_glob(path: str, pattern: str) -> ListConfig:
    """Return files matching a glob pattern as a list of path strings.

    Parameters
    ----------
    path : str
        Root directory to search from. Must exist.
    pattern : str
        Glob pattern passed to :pymeth:`pathlib.Path.glob`.

    Returns
    -------
    ListConfig
        OmegaConf list of matching paths serialised as strings, in
        filesystem order.

    Raises
    ------
    FileNotFoundError
        If ``path`` does not exist.
    """
    root_dir = oc_str2path(path, True)
    return OmegaConf.create([str(f) for f in root_dir.glob(pattern)])
