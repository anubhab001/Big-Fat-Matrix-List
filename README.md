# Big-Fat-Matrix-List

Public collection of binary linear layers (matrices over binary, including bit-permutations) used in cryptography.

Last update: 25 October 2025 <!-- TODO: This is to be updated with each (major) commit/push -->

## Organisation

- [`matrices.yaml`](matrices.yaml): every binary matrix entry, keyed by an UPPERCASE dotted name (e.g. `AES.MIXCOLUMN`, `GF128.MUL`, `SHA3`).
- [`permutations.yaml`](permutations.yaml): bit-permutations as integer lists, keyed by `<CIPHER>.PERM<size>` (e.g. `PRESENT.PERM64`, `GIFT.PERM128`).
- [`bigfatmatrix.py`](bigfatmatrix.py): the Python loader.
- [`__PNG__/`](__PNG__/): one black-and-white PNG per matrix (`<KEY>.png`) in the same binary-grid style as the [`linear-layers-main`](https://github.com/Daemen-Crypto/linear-layers) repository.

Matrix rows are stored as binary strings (`'0'`/`'1'` characters) so that even very large matrices (e.g. SHA-3 at 1600×1600 or $\mathrm{GF}(2^{1024})$ multiplication at 1024×2047) stay compact and human-readable.

## Naming Convention

- Entry keys use UPPERCASE Latin characters with optional dots, no hyphens, no underscores (other than the inevitable disambiguators inside binary-field names like `GF163_0`), no spaces. Example keys: `AES.MIXCOLUMN`, `MIDORI`, `PYJAMASK.MK`, `GF256.MUL`, `GIFT.PERM64`.
- The cipher / source name precedes the dot; the specific matrix or permutation name follows the dot (e.g. `CLEFIA.M0`, `WHIRLWIND.M1`).
- `canonical_name` records the original casing / typography used by the designers (e.g. `"Grøstl"`, `"Pyjamask M_k"`).
- Permutations are tagged by output size: `PRESENT.PERM64`, `GIFT.PERM128`.

## Entry Format

### Matrices (in `matrices.yaml`)

| Field | Type | Description |
|-------|------|-------------|
| `canonical_name`<sup>*</sup> | str | Name as written in the original publication (preserves case, non-Latin characters, subscripts, hyphens, spaces). |
| `rows`<sup>*</sup> | int | Number of rows. |
| `cols`<sup>*</sup> | int | Number of columns. |
| `year` | list | Significant publication years (proposal, journal, standard approval, …). |
| `origin` | str | URL of the original publication / specification. |
| `note` | str | Free-form remark (designer credits, equivalent forms, links to related entries). |
| `involutory` | bool | Present and `true` iff the matrix squares to the identity over $\mathrm{GF}(2)$. |
| `matrix`<sup>*</sup> | list[str] | One bit-string per row; character `c[j]` is the bit in column $j$. |

### Permutations (in `permutations.yaml`)

| Field | Type | Description |
|-------|------|-------------|
| `canonical_name`<sup>*</sup> | str | Original name. |
| `size`<sup>*</sup> | int | Number of bits permuted. |
| `year` | list | Significant publication years. |
| `origin` | str | URL of the original publication / specification. |
| `note` | str | Free-form remark. |
| `perm`<sup>*</sup> | list[int] | The permutation $P$, with `P[i]` being the destination index of input bit $i$. |

## Notes

1. The `_constant/` folder of the [`linear-layers-main`](https://github.com/Daemen-Crypto/linear-layers) repository was the primary mining source. Sage-only constructions (e.g. test matrices like `Lucas`, intermediate Boyar–Peralta tableau matrices) and known non-MDS / non-cipher matrices (e.g. the `DL18` family) are intentionally omitted.
2. Binary-field matrices `GF<n>.MUL` and `GF<n>.SQR` represent multiplication-by-$x$ (companion matrix of the irreducible polynomial) and the Frobenius squaring map, respectively, over $\mathrm{GF}(2^n)$. For $n \in \{163, 283, 571\}$ both the standard NIST-recommended polynomial (variant `_0`) and a second irreducible polynomial used in the literature (variant `_1`) are included.
3. The full Saturnin large-state matrix is not included here in its diffusion-layer form because it is provided in the source as a $\mathrm{GF}(2)$ matrix that is non-MDS as a pure binary matrix; the same diffusion property is captured by the Saturnin paper's algebraic construction over $\mathrm{GF}(2^4)$.
4. PNG renders are produced from the YAML directly (script: `scripts/render_pngs.py`) so a regenerated PNG always matches the catalogued matrix.

## Python Loader

[`bigfatmatrix.py`](bigfatmatrix.py) exposes every YAML entry as a Python object. It requires Python 3.11+ and [PyYAML](https://pypi.org/project/PyYAML/); `numpy` is optional and only needed for `MatrixEntry.as_numpy()`.

With `bigfatmatrix.py` and the YAML files present in the working directory (or anywhere on `sys.path`):

```python
import bigfatmatrix
print(bigfatmatrix.last_update)
```

### Single-entry access

```python
m = bigfatmatrix.aes_mixcolumn          # case-insensitive — hits AES.MIXCOLUMN
m = bigfatmatrix['AES.MIXCOLUMN']       # bracket access (case-insensitive)
print(m)                                # MatrixEntry('AES.MIXCOLUMN', shape=32x32)
print(m.canonical_name)                 # 'AES MixColumn'
print(m.rows, m.cols)                   # 32 32
print(m.matrix[0])                      # '00000001100000011000000010000000'

ints = m.as_int_matrix()                # list[list[int]] of 0/1
arr  = m.as_numpy()                     # numpy.ndarray, dtype=uint8 — needs numpy

# Metadata fields are exposed as attributes
print(m.year)        # [1998, 2001]
print(m.origin)      # 'https://csrc.nist.gov/...'
print(m.note)        # 'Daemen-Rijmen, Rijndael / FIPS-197.'
print(m.fields)      # list of available field names
print(m.to_dict())   # raw YAML dict copy
```

### Group access

Entries sharing a dotted prefix (`AES.*`, `GF128.*`, `PYJAMASK.*`, …) are exposed as a `MatrixGroup`:

```python
gf128 = bigfatmatrix.gf128             # MatrixGroup('GF128', members=['mul', 'sqr'])
print(gf128.mul)                       # MatrixEntry('GF128.MUL', shape=128x255)
for m in gf128:                        # iterate over members
    print(m.name, m.rows, 'x', m.cols)

pyjamask = bigfatmatrix.pyjamask
print(len(pyjamask))                   # 5  (M0, M1, M2, M3, MK)
```

### Permutations

```python
p = bigfatmatrix['GIFT.PERM64']        # MatrixEntry('GIFT.PERM64', perm size=64)
print(p.size)                          # 64
print(p.perm[:8])                      # [0, 17, 34, 51, 48, 1, 18, 35]

# Convert to an n×n permutation matrix over GF(2):
P = p.as_permutation_matrix()          # list[list[int]]
```

### Wildcard search

```python
bigfatmatrix.find('GF*.MUL')           # all multiplication tables
bigfatmatrix.find('SHA*')              # SHA-2 / SHA-3 entries
bigfatmatrix['AES.*']                  # bracket-form wildcard (returns dict)
```

### Raw YAML access

```python
bigfatmatrix.yaml['AES.MIXCOLUMN']     # raw dict
bigfatmatrix.yaml.all_names()          # sorted list of every UPPERCASE key
```

### Command-line

```bash
python bigfatmatrix.py AES.MIXCOLUMN GIFT.PERM128
```
