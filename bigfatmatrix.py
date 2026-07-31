#!/usr/bin/env python3
"""
bigfatmatrix.py: Big-Fat-Matrix-List loader

Three access modes:

  Python mode
  -----------
  import bigfatmatrix
  m = bigfatmatrix.aes_mixcolumn        # MatrixEntry (case-insensitive)
  m = bigfatmatrix['AES.MIXCOLUMN']     # bracket access (case-insensitive)
  m.matrix                              # tuple of binary strings, one per row
  m.rows, m.cols                        # dimensions
  m.as_int_matrix()                     # tuple of tuples of 0/1
  m.as_numpy()                          # numpy.ndarray (uint8), needs numpy
  m.canonical_name                      # 'AES MixColumn'
  m.year, m.origin, m.note              # metadata as attributes
  m.to_dict()                           # raw YAML dict

  from bigfatmatrix import aes          # MatrixGroup (entries keyed AES.*)
  aes.mixcolumn                         # AES.MIXCOLUMN entry
  for x in bigfatmatrix.gift: ...       # iterate over GIFT.* entries

  Permutation entries expose a `.perm` property (tuple[int]) and `.size`, and
  can also be read as a binary permutation matrix:
  bigfatmatrix.as_matrix('GIFT.64')     # tuple of tuples (Matrix(GF(2)) in Sage)
  bigfatmatrix['GIFT.64'].as_int_matrix()
  bigfatmatrix['GIFT.64'].as_matrix_rows()

  Sage mode (auto-detected when running inside SageMath)
  ------------------------------------------------------
  from bigfatmatrix import aes_mixcolumn  # returns Matrix(GF(2), ...)
  bigfatmatrix.present                    # returns sage.combinat.permutation.Permutation
  m.to_sage()                             # explicit conversion in Python mode

  YAML/raw-dict mode (works in both Python and Sage)
  --------------------------------------------------
  bigfatmatrix.yaml['AES.MIXCOLUMN']    # raw YAML dict (case-insensitive)
  bigfatmatrix.yaml.all_names()         # list of every entry key

  Wildcard search
  ---------------
  bigfatmatrix.find('gf*.mul')          # returns dict of matching entries
  bigfatmatrix['aes.*']                 # bracket-form wildcard search

For `import bigfatmatrix` to work, this script and all `*.yaml` data files
must live in the same directory, which must be either the current working
directory or on `sys.path`. Loading is lazy: no YAML file is read until the
first access. A large size band is published as several `<band>.partNN.yaml`
files; the loader merges it back into one entry, so the access API is the
same either way.
"""

from __future__ import annotations

import fnmatch as _fnmatch
import os
import re
import sys
import types as _types
from pathlib import Path
from typing import Any, Iterator

_HERE = Path(__file__).parent
_PUBLIC = _HERE


def _read_last_update() -> str | None:
    readme = _HERE / 'README.md'
    if not readme.exists():
        return None
    with open(readme, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^Last update:\s*(.+?)\s*<!--', line)
            if m:
                return m.group(1).strip()
    return None


last_update: str | None = _read_last_update()

# ---------------------------------------------------------------------------
# Raw data
# ---------------------------------------------------------------------------

_raw: dict[str, dict] = {}
_aliases: dict[str, str] = {}
_loaded: bool = False


def _ensure_loaded() -> None:
    global _loaded
    if _loaded:
        return
    _loaded = True
    _do_load()


def _do_load() -> None:
    try:
        import yaml as _yaml
        _safe_load = _yaml.safe_load
    except ImportError as exc:
        raise ImportError(
            "PyYAML is required to use bigfatmatrix.\n"
            "Install it with:  pip install pyyaml"
        ) from exc

    parts: dict[str, dict[int, list]] = {}

    for fpath in sorted(_PUBLIC.glob('*.yaml')):
        with open(fpath, encoding='utf-8') as f:
            data = _safe_load(f)
        if not isinstance(data, dict):
            continue
        for key, val in data.items():
            if not isinstance(val, dict):
                continue
            ukey = key.upper()
            if 'matrix_part' in val:
                # Matrix body split across `<band>.partNN.yaml` files, so that
                # every published file stays small enough for GitHub to render.
                parts.setdefault(ukey, {})[int(val['matrix_part'])] = \
                    val.get('matrix') or []
                if 'canonical_name' not in val:
                    continue
                val = {k: v for k, v in val.items()
                       if k not in ('matrix', 'matrix_part', 'matrix_parts')}
            _raw[ukey] = val
            for alias in (val.get('aliases') or []):
                _aliases[str(alias).upper()] = ukey

    for ukey, chunks in parts.items():
        rows: list = []
        for idx in sorted(chunks):
            rows.extend(chunks[idx])
        if ukey in _raw:
            _raw[ukey]['matrix'] = rows
    for key, val in list(_raw.items()):
        if isinstance(val, dict) and 'alias' in val:
            _aliases[key] = str(val['alias']).upper()


def _resolve(name: str) -> str | None:
    _ensure_loaded()
    uname = name.upper()
    candidates = [uname]
    if '_' in uname and '.' not in uname:
        candidates.append(uname.replace('_', '.'))
    visited: set[str] = set()
    for cand in candidates:
        cur = cand
        while cur in _aliases and cur not in visited:
            visited.add(cur)
            cur = _aliases[cur]
        if cur in _raw:
            return cur
    return None


# ---------------------------------------------------------------------------
# MatrixEntry: wrapper for a single matrix or permutation entry
# ---------------------------------------------------------------------------

def _freeze(v):
    """Sequence-valued fields are handed out as tuples, never as lists."""
    if isinstance(v, (list, tuple)):
        return tuple(_freeze(x) for x in v)
    return v


class MatrixEntry:
    """Attribute-access wrapper around a single YAML entry.

    Common fields:
        canonical_name : str
        year           : tuple[int, ...] | None
        origin         : str | None
        note           : str | None
        involutory     : bool | None

    Matrix entries:
        rows, cols     : int
        matrix         : tuple[str]  (each row is a '0'/'1' bit string)
        as_int_matrix(): tuple[tuple[int, ...], ...]
        as_numpy()     : numpy.ndarray (uint8)

    Permutation entries:
        size           : int
        perm           : tuple[int, ...]
    """

    __slots__ = ('_name', '_data')

    def __init__(self, name: str, data: dict) -> None:
        object.__setattr__(self, '_name', name)
        object.__setattr__(self, '_data', data)

    # -- attribute access ----------------------------------------------------

    def __getattr__(self, attr: str) -> Any:
        data = object.__getattribute__(self, '_data')
        if attr in data:
            return _freeze(data[attr])
        alt = attr.replace('_', '-')
        if alt in data:
            return _freeze(data[alt])
        raise AttributeError(
            f"MatrixEntry '{object.__getattribute__(self, '_name')}' "
            f"has no field '{attr}'"
        )

    @property
    def name(self) -> str:
        return object.__getattribute__(self, '_name')

    @property
    def is_permutation(self) -> bool:
        data = object.__getattribute__(self, '_data')
        return 'perm' in data

    @property
    def is_matrix(self) -> bool:
        data = object.__getattribute__(self, '_data')
        return 'matrix' in data

    # -- matrix helpers ------------------------------------------------------

    def as_int_matrix(self) -> tuple[tuple[int, ...], ...]:
        """0/1 rows. A bit-permutation is returned as its permutation matrix."""
        data = object.__getattribute__(self, '_data')
        rows = data.get('matrix')
        if rows is None:
            if 'perm' in data:
                return self.as_permutation_matrix()
            raise ValueError(
                f"MatrixEntry '{self.name}' has no `matrix` field"
            )
        out: list[tuple[int, ...]] = []
        for r in rows:
            if isinstance(r, str):
                out.append(tuple(1 if c == '1' else 0 for c in r))
            else:
                out.append(tuple(int(b) for b in r))
        return tuple(out)

    def as_matrix_rows(self) -> tuple[str, ...]:
        """Bit-strings, one per row, for a matrix or a bit-permutation alike."""
        return tuple(''.join(str(b) for b in row) for row in self.as_int_matrix())

    def as_numpy(self):
        try:
            import numpy as _np
        except ImportError as exc:
            raise ImportError(
                "numpy is required for MatrixEntry.as_numpy()"
            ) from exc
        return _np.asarray(self.as_int_matrix(), dtype=_np.uint8)

    # -- permutation helpers -------------------------------------------------

    def as_permutation_matrix(self) -> tuple[tuple[int, ...], ...]:
        """Return the n x n permutation matrix M such that y = M x acts as
        y[P[i]] = x[i], that is, M[P[i]][i] = 1.
        """
        data = object.__getattribute__(self, '_data')
        perm = data.get('perm')
        if perm is None:
            raise ValueError(
                f"MatrixEntry '{self.name}' has no `perm` field"
            )
        n = int(data.get('size', len(perm)))
        M = [[0] * n for _ in range(n)]
        for i, p in enumerate(perm):
            M[p][i] = 1
        return tuple(tuple(r) for r in M)

    # -- Sage conversion ------------------------------------------------------

    def to_sage(self, as_matrix: bool = False):
        """Return the Sage-native object for this entry.

        Matrix entries  → ``Matrix(GF(2), rows, cols, [[…]])``.
        Permutation entries → ``sage.combinat.permutation.Permutation`` (1-based),
        or, with ``as_matrix=True``, the ``Matrix(GF(2), …)`` of that permutation.
        Requires SageMath to be importable.
        """
        data = object.__getattribute__(self, '_data')
        if 'matrix' in data:
            return _sage_matrix(self.as_int_matrix())
        if 'perm' in data:
            if as_matrix:
                return _sage_matrix(self.as_permutation_matrix())
            return _sage_permutation(data['perm'])
        raise ValueError(
            f"MatrixEntry '{self.name}' has neither `matrix` nor `perm`"
        )

    # -- generic --------------------------------------------------------------

    def keys(self):
        return object.__getattribute__(self, '_data').keys()

    @property
    def fields(self) -> list[str]:
        return list(object.__getattribute__(self, '_data').keys())

    def to_dict(self) -> dict:
        return dict(object.__getattribute__(self, '_data'))

    def __repr__(self) -> str:
        data = object.__getattribute__(self, '_data')
        if 'matrix' in data:
            shape = f"{data.get('rows', '?')}x{data.get('cols', '?')}"
            return f"MatrixEntry({self.name!r}, shape={shape})"
        if 'perm' in data:
            return f"MatrixEntry({self.name!r}, perm size={data.get('size', '?')})"
        return f"MatrixEntry({self.name!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MatrixEntry):
            return self.name == other.name
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.name)


# ---------------------------------------------------------------------------
# MatrixGroup: entries sharing a dotted prefix (e.g. AES.*)
# ---------------------------------------------------------------------------

class MatrixGroup:
    """Namespace for related entries, e.g. all AES.* or all GF128.* entries."""

    def __init__(self, group_name: str) -> None:
        object.__setattr__(self, '_gname', group_name)
        object.__setattr__(self, '_members', {})

    def _add(self, sub_key: str, entry: MatrixEntry) -> None:
        object.__getattribute__(self, '_members')[sub_key.lower()] = entry

    def __getattr__(self, name: str) -> MatrixEntry:
        members = object.__getattribute__(self, '_members')
        key = name.lower()
        if key in members:
            return members[key]
        gname = object.__getattribute__(self, '_gname')
        entry = _get_entry(f'{gname}.{name.upper()}')
        if entry is not None:
            return entry
        raise AttributeError(
            f"MatrixGroup '{gname}' has no member '{name}'"
        )

    def __getitem__(self, name: str) -> MatrixEntry:
        return self.__getattr__(name)

    def __iter__(self) -> Iterator[MatrixEntry]:
        return iter(object.__getattribute__(self, '_members').values())

    def __len__(self) -> int:
        return len(object.__getattribute__(self, '_members'))

    def __repr__(self) -> str:
        gname = object.__getattribute__(self, '_gname')
        members = object.__getattribute__(self, '_members')
        return f"MatrixGroup({gname!r}, members={sorted(members.keys())})"


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Sage detection / native conversion
# ---------------------------------------------------------------------------

def _in_sage() -> bool:
    """Return True when running inside a SageMath session."""
    return 'sage.all' in sys.modules or 'sage' in sys.modules


def _sage_matrix(rows: list[list[int]]):
    """Return a Sage Matrix over GF(2) for the given 0/1 rows."""
    from sage.all import Matrix, GF   # type: ignore
    nrows = len(rows)
    ncols = len(rows[0]) if rows else 0
    return Matrix(GF(2), nrows, ncols, rows)


def _sage_permutation(perm: list[int]):
    """Return a Sage Permutation (1-based) for the given 0-based mapping."""
    from sage.all import Permutation   # type: ignore
    return Permutation([int(p) + 1 for p in perm])


def _wrap(name: str, data: dict):
    """Inside Sage return native object directly; otherwise return MatrixEntry."""
    if _in_sage():
        try:
            if 'matrix' in data:
                rows = [[1 if (c == '1' if isinstance(r, str) else int(c))
                         else 0 for c in r] for r in data['matrix']]
                return _sage_matrix(rows)
            if 'perm' in data:
                return _sage_permutation(data['perm'])
        except ImportError:
            pass
    return MatrixEntry(name, data)


def _get_entry(name: str):
    _ensure_loaded()
    canonical = _resolve(name)
    if canonical is None:
        return None
    data = _raw[canonical]
    if 'alias' in data:
        return _get_entry(str(data['alias']))
    return _wrap(canonical, data)


def _get_raw(name: str) -> dict | None:
    _ensure_loaded()
    canonical = _resolve(name)
    if canonical is None:
        return None
    data = _raw[canonical]
    if 'alias' in data:
        return _get_raw(str(data['alias']))
    return data


_groups_cache: dict[str, MatrixGroup] | None = None


def _build_groups() -> dict[str, MatrixGroup]:
    _ensure_loaded()
    groups: dict[str, MatrixGroup] = {}
    for ukey in _raw:
        if '.' in ukey:
            prefix = ukey.split('.', 1)[0]
            sub = ukey.split('.', 1)[1]
            if prefix not in groups:
                groups[prefix] = MatrixGroup(prefix)
            entry = _get_entry(ukey)
            if entry is not None:
                groups[prefix]._add(sub, entry)
    return groups


def _get_group(name: str) -> MatrixGroup | None:
    global _groups_cache
    if _groups_cache is None:
        _groups_cache = _build_groups()
    return _groups_cache.get(name.upper())


# ---------------------------------------------------------------------------
# YAML proxy
# ---------------------------------------------------------------------------

class _YAMLProxy:
    """bigfatmatrix.yaml.aes_mixcolumn or bigfatmatrix.yaml['AES.MIXCOLUMN']
    returns the raw YAML dict, with case-insensitive lookup."""

    def __getattr__(self, name: str) -> dict:
        if name.startswith('_'):
            raise AttributeError(name)
        data = _get_raw(name)
        if data is not None:
            return data
        raise AttributeError(f"bigfatmatrix.yaml: no entry '{name}'")

    def __getitem__(self, name: str) -> dict:
        return self.__getattr__(name)

    def __repr__(self) -> str:
        return 'bigfatmatrix.yaml  (raw YAML dict access)'

    def all_entries(self) -> dict[str, dict]:
        _ensure_loaded()
        return dict(_raw)

    def all_names(self) -> list[str]:
        _ensure_loaded()
        return sorted(_raw.keys())


yaml = _YAMLProxy()


# ---------------------------------------------------------------------------
# Wildcard search
# ---------------------------------------------------------------------------

def as_matrix(name: str):
    """Matrix form of any entry, bit-permutation included.

    Inside SageMath this is ``Matrix(GF(2), ...)``; in plain Python it is a
    tuple of tuples of 0/1. A bit-permutation P becomes the matrix M with
    ``M[P[i]][i] = 1``, so ``bigfatmatrix['GIFT.64'].perm`` gives the tuple
    form and ``bigfatmatrix.as_matrix('GIFT.64')`` the matrix form.
    """
    data = _get_raw(name)
    if data is None:
        raise KeyError(f"bigfatmatrix: no entry '{name}'")
    rows = MatrixEntry(name.upper(), data).as_int_matrix()
    if _in_sage():
        try:
            return _sage_matrix(rows)
        except ImportError:
            pass
    return rows


def find(pattern: str) -> dict[str, MatrixEntry]:
    """Return entries whose UPPERCASE key matches *pattern* (fnmatch syntax)."""
    _ensure_loaded()
    upat = pattern.upper()
    out: dict[str, MatrixEntry] = {}
    for ukey in sorted(_raw):
        if _fnmatch.fnmatchcase(ukey, upat):
            entry = _get_entry(ukey)
            if entry is not None:
                out[ukey] = entry
    return out


# ---------------------------------------------------------------------------
# Module-level attribute & subscription support
# ---------------------------------------------------------------------------

_RESERVED = {
    '__file__', '__spec__', '__loader__', '__path__',
    '__package__', '__builtins__', '__name__', '__doc__',
    '__class__', '__dict__',
    'yaml', 'last_update', 'find', 'as_matrix',
    'MatrixEntry', 'MatrixGroup',
}


def __getattr__(name: str) -> Any:
    if name.startswith('_') or name in _RESERVED:
        raise AttributeError(name)
    _ensure_loaded()
    entry = _get_entry(name)
    if entry is not None:
        return entry
    group = _get_group(name)
    if group is not None:
        return group
    raise AttributeError(
        f"bigfatmatrix has no entry or group named '{name}'.\n"
        f"Use bigfatmatrix.yaml.all_names() to see all available entries."
    )


def __dir__() -> list[str]:
    _ensure_loaded()
    return sorted(
        set(_raw.keys()) | set(_aliases.keys()) |
        {'yaml', 'last_update', 'find', 'as_matrix', 'MatrixEntry',
         'MatrixGroup'}
    )


def _make_all() -> list[str]:
    _ensure_loaded()
    return [k for k in _raw if not k.startswith('_')]


__all__ = _make_all()


class _BigFatModule(_types.ModuleType):
    """Module subclass enabling subscript syntax."""

    def __getitem__(self, name: str) -> Any:
        if '*' in name or '?' in name:
            return find(name)
        entry = _get_entry(name)
        if entry is not None:
            return entry
        group = _get_group(name)
        if group is not None:
            return group
        raise KeyError(f"bigfatmatrix: no entry '{name}'")


sys.modules[__name__].__class__ = _BigFatModule


# ---------------------------------------------------------------------------
# CLI helper:  python bigfatmatrix.py <name> [<name> ...]
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import json

    names = sys.argv[1:]
    if not names:
        _ensure_loaded()
        print(f"bigfatmatrix: {len(_raw)} entries available")
        print(f"  example:  python bigfatmatrix.py AES.MIXCOLUMN")
        sys.exit(0)

    _ensure_loaded()
    for name in names:
        raw = _get_raw(name)
        if raw is None:
            print(f"Not found: {name}", file=sys.stderr)
            continue
        print(f"# {name.upper()}")
        for k, v in raw.items():
            if k in ('matrix', 'perm'):
                if isinstance(v, list) and len(v) > 6:
                    print(f"  {k}: <{len(v)} rows/items, suppressed>")
                else:
                    print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
            else:
                print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
