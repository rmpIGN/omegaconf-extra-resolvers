"""Additional resolver helpers for OmegaConf configurations."""

from errno import ENOENT
from os import strerror
from pathlib import Path
from typing import Any
from typing import Iterable
from typing import Literal


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


def oc_pad(
    value,
    pad_value,
    new_length: int,
    where: Literal["left", "right"] = "right",
) -> list[Any]:
    """Pad a sequence-like value to a target length.

    Parameters
    ----------
    value : Any
        Value to convert to a list and pad. It must support ``len`` and
        iteration.
    pad_value : Any
        Value used to fill the padding positions.
    new_length : int
        Desired length of the returned list.
    where : {"left", "right"}, optional
        Side on which to add padding values.

    Returns
    -------
    list[Any]
        Padded list. If ``new_length`` is smaller than ``len(value)``, the
        original values are returned as a list without truncation.
    """
    pad_len = max(0, new_length - len(value))
    padded_list = [pad_value] * pad_len
    if where == "left":
        padded_list = padded_list + list(value)
    else:
        padded_list = list(value) + padded_list
    return padded_list


def oc_lpad(value: Any, pad_value: Any, new_length: int) -> list[Any]:
    """Pad a sequence-like value on the left.

    Parameters
    ----------
    value : Any
        Value to convert to a list and pad. It must support ``len`` and
        iteration.
    pad_value : Any
        Value used to fill the padding positions.
    new_length : int
        Desired length of the returned list.

    Returns
    -------
    list[Any]
        Left-padded list.
    """
    return oc_pad(value, pad_value, new_length, "left")


def oc_rpad(value: Any, pad_value: Any, new_length: int) -> list[Any]:
    """Pad a sequence-like value on the right.

    Parameters
    ----------
    value : Any
        Value to convert to a list and pad. It must support ``len`` and
        iteration.
    pad_value : Any
        Value used to fill the padding positions.
    new_length : int
        Desired length of the returned list.

    Returns
    -------
    list[Any]
        Right-padded list.
    """
    return oc_pad(value, pad_value, new_length, "right")


def oc_len(value: Any) -> int:
    """Return the length of a value.

    Parameters
    ----------
    value : Any
        Value whose length should be returned.

    Returns
    -------
    int
        Length returned by ``len(value)``.

    Raises
    ------
    ValueError
        If ``value`` does not expose a ``__len__`` attribute.
    """
    if not hasattr(value, "__len__"):
        raise ValueError(f"Object {value} has no length property.")
    return len(value)


def oc_coalesce(arr: Iterable) -> Any:
    """Return the first non-``None`` item from an iterable.

    Parameters
    ----------
    arr : Iterable
        Iterable whose items should be inspected in order.

    Returns
    -------
    Any
        First item in ``arr`` that is not ``None``.

    Raises
    ------
    ValueError
        If ``arr`` is not iterable, or if all items in ``arr`` are ``None``.
    """
    if not isinstance(arr, Iterable):
        raise ValueError(f"Object {arr} is not iterable.")
    try:
        first = next(item for item in arr if item is not None)
        return first
    except StopIteration:
        raise ValueError(f"All items of {arr} are None.")
