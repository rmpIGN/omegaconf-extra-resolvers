# omegaconf-extra-resolvers

A small Python package that registers additional custom resolvers for [OmegaConf](https://omegaconf.readthedocs.io/).

**WARNING: This package is recent. The API may change significantly in the coming weeks.**

## Installation

**This package is not yet published on PyPI.**

But you can still install it from GitHub.

```bash
# With pip
pip install git+https://github.com/rmpIGN/omegaconf-extra-resolvers.git

# With uv
uv add "omegaconf-extra-resolvers @ git+https://github.com/rmpIGN/omegaconf-extra-resolvers.git"
```

## Usage

Register all resolvers at once:

```python
from omegaconf_extra_resolvers import oc_register_extra_resolvers

oc_register_extra_resolvers()
```

Or register a specific subset using the `ResolverEnum`:

```python
from omegaconf_extra_resolvers import ResolverEnum, oc_register_extra_resolvers

oc_register_extra_resolvers(resolvers=[ResolverEnum.PATH, ResolverEnum.LEN])
```

## Available resolvers

| Resolver | Signature | Description |
|---|---|---|
| `path` | `path: str, check_exist: bool = False` | Converts a string to a `pathlib.Path`. Optionally raises `FileNotFoundError` if the path does not exist. |
| `pad` | `value, pad_value, new_length: int, where: str = "right"` | Pads a list to `new_length` with `pad_value`. `where` accepts `"left"` or `"right"`. |
| `lpad` | `value, pad_value, new_length: int` | Shorthand for left-padding a list (equivalent to `pad` with `where="left"`). |
| `rpad` | `value, pad_value, new_length: int` | Shorthand for right-padding a list (equivalent to `pad` with `where="right"`). |
| `len` | `value` | Returns the length of any sized object. Raises `ValueError` if the value has no `__len__`. |
| `coalesce` | `arr` | Returns the first non-`null` item from a list. Raises `ValueError` if all items are `null`. |

### Examples

```yaml
data_dir: /data/raw
# Convert a string key to a Path
data_path: ${path:${data_dir}}

# Pad a list to length 5 with zeros on the right
padded: ${rpad:[1,2,3],0,5}   # [1, 2, 3, 0, 0]

# Left-pad to length 4
lpadded: ${lpad:[7,8],0,4}    # [0, 0, 7, 8]

# Length of a list
n_items: ${len:${padded}}     # 5

# First non-null value
active_model: ${coalesce:[null, null, resnet50]}  # resnet50
```

## Requirements

- Python ≥ 3.12
- omegaconf ≥ 2.3.1
