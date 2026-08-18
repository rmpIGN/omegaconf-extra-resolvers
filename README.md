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

### OS (`resolvers.os`)

| Resolver | Description | Example |
|---|---|---|
| `path` | Converts a string to a `pathlib.Path`. Optionally raises `FileNotFoundError` if the path does not exist. | `${path:/data/raw}` → `Path("/data/raw")` |
| `glob` | Returns files matching a glob pattern under `path` as a list of path strings. Raises `FileNotFoundError` if `path` does not exist. | `${glob:/data/raw,*.tif}` → `["/data/raw/a.tif", …]` |

### List (`resolvers.list`)

| Resolver | Description | Example |
|---|---|---|
| `pad` | Pads a list to `new_length` with `pad_value`. `where` accepts `"left"` or `"right"` (default). | `${pad:[1,2],0,5}` → `[1, 2, 0, 0, 0]` |
| `lpad` | Shorthand for left-padding a list. | `${lpad:[7,8],0,4}` → `[0, 0, 7, 8]` |
| `rpad` | Shorthand for right-padding a list. | `${rpad:[1,2,3],0,5}` → `[1, 2, 3, 0, 0]` |
| `len` | Returns the length of any sized object. Raises `ValueError` if the value has no `__len__`. | `${len:${items}}` → `3` |
| `coalesce` | Returns the first non-`null` item from a list. Raises `ValueError` if all items are `null`. | `${coalesce:[null, null, resnet50]}` → `resnet50` |
| `range` | Returns a list of evenly spaced integers, mirroring Python's built-in `range`. | `${range:0,10,2}` → `[0, 2, 4, 6, 8]` |

### String (`resolvers.string`)

| Resolver | Description | Example |
|---|---|---|
| `upper` | Returns the string converted to upper-case. | `${upper:resnet50}` → `RESNET50` |
| `lower` | Returns the string converted to lower-case. | `${lower:PRODUCTION}` → `production` |

## Requirements

- Python ≥ 3.12
- omegaconf ≥ 2.3.1
