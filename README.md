# Big-Fat-Matrix-List

Public collection of binary linear layers (matrices over $\mathrm{GF}(2)$ and bit-permutations) used in cryptography

Last update: 31 July 2026 <!-- TODO: To be updated in UTC with each (major) commit/push -->

## Organisation

- YAML files containing details about multiple binary linear layers, dimensions, historical notes etc.

- Files are written by size band and by shape. A square matrix goes to `<N>bit.yaml`, a rectangular one to `rectangular<N>bit.yaml`, where $N$ is the next power of two up to $256$ and the exact column count above that. Bit-permutations live in `permutations.yaml`.

- No published file is larger than $400$ KB, so all of it renders in the GitHub web interface. A band above that size is published as several parts, `<band>.part01.yaml`, `<band>.part02.yaml` and so on, so that every file is relatively small; [`bigfatmatrix.py`](bigfatmatrix.py) merges them back into one entry per key. The split falls on an entry boundary where it can; where a single matrix is itself too large, its body is continued across parts and each piece carries `matrix_parts` and `matrix_part`, so an entry spread over seven files is still read as one `matrix`. The tables below list every part.

- How many parts a band takes follows the bodies it holds, at roughly $N + 1$ bytes per row: a single $1024 \times 1024$ matrix is about $1$ MB and takes three parts, a $1600 \times 1600$ one takes seven. Every entry carries its rows, including those also expressible as a composition of other entries.

- Entries within each YAML file are in alphabetical order by key.

- Every square matrix in the catalogue is non-singular, and the build refuses to publish one that is not. A round layer has to be invertible for decryption to exist, so a map that is not invertible is not a linear layer: the linear part of a key schedule, for instance, is under no such obligation and is not catalogued here. Renders of every entry are collected in [`visualisation.md`](visualisation.md).

## Naming Convention

- Entry keys use an all-uppercase Latin with/without dot convention (e.g., `PRESENT` as without dot; `AES.MIXCOLUMN`, `GIFT.64` as with dot), with no hyphen/underscore and no space. Note that the cipher name preceeds the dot and the linear-layer name (or its size when there are several layers in the same family) is after dot. If a cipher has only one linear layer with no specific name, only the cipher's name is used.

- `canonical_name` records the exact name as it appears in the original paper, as a tuple of the family name and the layer name, so that casing, non-Latin characters, subscript, hyphen and space all survive. For example, `SHA2.SMALLSIGMA0` carries `["SHA-2", "σ₀"]`.

- Lowercase `v` indicates a version number and is not part of the cipher name.

## Data Files

Each YAML file holds entries binned by `max(rows, cols)`. For sizes up to $256$ the bin is the next power of two ($1$ to $16$, $17$ to $32$, $33$ to $64$, $65$ to $128$, $129$ to $256$); above $256$, each distinct size gets its own file. Every band ships with a sibling `<band>.md` index carrying a preview table.

### Square Matrices

| File | # Entry | Size | Index |
|:------|:-------:|:-------------|:------|
| [`16bit.yaml`](16bit.yaml) | 35 | $4 \times 4$, $8 \times 8$, $16 \times 16$ | [`16bit.md`](16bit.md) |
| [`32bit.yaml`](32bit.yaml) | 53 | $20 \times 20$, $25 \times 25$, $32 \times 32$ | [`32bit.md`](32bit.md) |
| [`64bit.yaml`](64bit.yaml) | 42 | $50 \times 50$, $60 \times 60$, $64 \times 64$ | [`64bit.md`](64bit.md) |
| [`128bit.yaml`](128bit.yaml) | 17 | $100 \times 100$, $127 \times 127$, $128 \times 128$ | [`128bit.md`](128bit.md) |
| [`256bit.part01.yaml`](256bit.part01.yaml), [`256bit.part02.yaml`](256bit.part02.yaml) | 10 | $163 \times 163$, $192 \times 192$, $200 \times 200$, $233 \times 233$, $256 \times 256$ | [`256bit.md`](256bit.md) |
| [`283bit.yaml`](283bit.yaml) | 2 | $283 \times 283$ | [`283bit.md`](283bit.md) |
| [`320bit.yaml`](320bit.yaml) | 1 | $320 \times 320$ | [`320bit.md`](320bit.md) |
| [`400bit.yaml`](400bit.yaml) | 1 | $400 \times 400$ | [`400bit.md`](400bit.md) |
| [`571bit.part01.yaml`](571bit.part01.yaml), [`571bit.part02.yaml`](571bit.part02.yaml) | 2 | $571 \times 571$ | [`571bit.md`](571bit.md) |
| [`800bit.part01.yaml`](800bit.part01.yaml), [`800bit.part02.yaml`](800bit.part02.yaml) | 1 | $800 \times 800$ | [`800bit.md`](800bit.md) |
| [`1024bit.part01.yaml`](1024bit.part01.yaml), [`1024bit.part02.yaml`](1024bit.part02.yaml), [`1024bit.part03.yaml`](1024bit.part03.yaml) | 1 | $1024 \times 1024$ | [`1024bit.md`](1024bit.md) |
| [`1280bit.part01.yaml`](1280bit.part01.yaml), [`1280bit.part02.yaml`](1280bit.part02.yaml), [`1280bit.part03.yaml`](1280bit.part03.yaml), [`1280bit.part04.yaml`](1280bit.part04.yaml), [`1280bit.part05.yaml`](1280bit.part05.yaml) | 1 | $1280 \times 1280$ | [`1280bit.md`](1280bit.md) |
| [`1600bit.part01.yaml`](1600bit.part01.yaml), [`1600bit.part02.yaml`](1600bit.part02.yaml), [`1600bit.part03.yaml`](1600bit.part03.yaml), [`1600bit.part04.yaml`](1600bit.part04.yaml), [`1600bit.part05.yaml`](1600bit.part05.yaml), [`1600bit.part06.yaml`](1600bit.part06.yaml), [`1600bit.part07.yaml`](1600bit.part07.yaml) | 1 | $1600 \times 1600$ | [`1600bit.md`](1600bit.md) |

### Rectangular Matrices

| File | # Entry | Size | Index |
|:------|:-------:|:-------------|:------|
| [`rectangular16bit.yaml`](rectangular16bit.yaml) | 2 | $4 \times 7$, $8 \times 15$ | [`rectangular16bit.md`](rectangular16bit.md) |
| [`rectangular32bit.yaml`](rectangular32bit.yaml) | 1 | $16 \times 31$ | [`rectangular32bit.md`](rectangular32bit.md) |
| [`rectangular64bit.yaml`](rectangular64bit.yaml) | 1 | $32 \times 63$ | [`rectangular64bit.md`](rectangular64bit.md) |
| [`rectangular128bit.yaml`](rectangular128bit.yaml) | 1 | $64 \times 127$ | [`rectangular128bit.md`](rectangular128bit.md) |
| [`rectangular256bit.yaml`](rectangular256bit.yaml) | 2 | $127 \times 253$, $128 \times 255$ | [`rectangular256bit.md`](rectangular256bit.md) |
| [`rectangular325bit.yaml`](rectangular325bit.yaml) | 1 | $163 \times 325$ | [`rectangular325bit.md`](rectangular325bit.md) |
| [`rectangular465bit.yaml`](rectangular465bit.yaml) | 1 | $233 \times 465$ | [`rectangular465bit.md`](rectangular465bit.md) |
| [`rectangular511bit.yaml`](rectangular511bit.yaml) | 1 | $256 \times 511$ | [`rectangular511bit.md`](rectangular511bit.md) |
| [`rectangular565bit.yaml`](rectangular565bit.yaml) | 1 | $283 \times 565$ | [`rectangular565bit.md`](rectangular565bit.md) |
| [`rectangular1141bit.part01.yaml`](rectangular1141bit.part01.yaml), [`rectangular1141bit.part02.yaml`](rectangular1141bit.part02.yaml) | 1 | $571 \times 1141$ | [`rectangular1141bit.md`](rectangular1141bit.md) |
| [`rectangular2047bit.part01.yaml`](rectangular2047bit.part01.yaml), [`rectangular2047bit.part02.yaml`](rectangular2047bit.part02.yaml), [`rectangular2047bit.part03.yaml`](rectangular2047bit.part03.yaml), [`rectangular2047bit.part04.yaml`](rectangular2047bit.part04.yaml), [`rectangular2047bit.part05.yaml`](rectangular2047bit.part05.yaml), [`rectangular2047bit.part06.yaml`](rectangular2047bit.part06.yaml) | 1 | $1024 \times 2047$ | [`rectangular2047bit.md`](rectangular2047bit.md) |

### Bit-Permutations

| File | # Entry | Index |
|:------|:-------:|:------|
| [`permutations.yaml`](permutations.yaml) | 36 | [`permutations.md`](permutations.md) |

### Visual Renders

Folder [`__renders__/`](__renders__) contains one PNG and one SVG render per entry (file `<KEY>.png` and `<KEY>.svg`). Cells with value $0$ are filled yellow; cells with value $1$ are filled blue. The colour scheme matches the [`linear-layers`](https://github.com/Daemen-Crypto/linear-layers) repository. A bit-permutation $P$ of size $N$ is rendered as the $N \times N$ matrix $M$ defined by $M[P[i]][i] = 1$. All of the renders are gathered in [`visualisation.md`](visualisation.md).

## Entry Format

A bit-permutation is a matrix too, so one table covers both. An entry carries a
`matrix` or a `perm`, and the fields that only make sense for
one of it are absent from the others. Mandatory fields are marked with *, and
a field compulsory only for one kind of entry with †.

| Field | Type | Description |
|-------|------|-------------|
| `canonical_name`<sup>*</sup> | tuple | Name as written in the original paper, as (family, layer), preserving case, non-Latin character, subscript, hyphen and space; a family with a single unnamed layer gives a one-element tuple |
| `aliases` | tuple[str] | Alternative names for the same entry used in the literature, including the identifier a public circuit corpus files it under |
| `reuse` | tuple[str] | Layers elsewhere that are this same matrix, written `CIPHER.LAYER`; see Notes 15 |
| `similarity` | tuple[str] | Entries that are this matrix under a relabelling of rows and columns rather than the same matrix; see Notes 16 |
| `rows`, `cols`<sup>*</sup> | int | Number of rows (output bit width) and columns (input bit width); absent for a bit-permutation, which is square of side `size` |
| `size`<sup>*</sup> | int | Side of a bit-permutation |
| `year` | tuple | Significant publication years (e.g., proposal, journal, standardisation); absent when no dated publication defines the entry |
| `cipher`<sup>*</sup> | bool | True iff the entry is the linear layer of a primitive, rather than a construction proposed in a paper on matrices, or plain finite-field arithmetic |
| `origin`<sup>*</sup> | str | URL of the original publication or specification |
| `source` | str | URL of code or related resource whence some information is mined |
| `paper_title` | str | Free-form citation pointer to the originating paper |
| `note` | str | Free-form remark; designer credit, equivalent form, link to a related entry |
| `formula` | str | Algorithmic description of how the entry is constructed, in pseudo-code, formulas, or rotation and shift recipes; emitted as a YAML literal block scalar (`\|-`) when multi-line |
| `augmentation` | str | Symbolic expression building this matrix from other catalogued entries (e.g., `block_diag(...)`, `kron(...)`); see Notes 6 |
| `involution` | bool | True iff $M^2 = I$ over $\mathrm{GF}(2)$, that is, the entry is its own inverse |
| `symmetric` | bool | True iff $M = M^	op$ |
| `rank` | int | Rank of $M$ over $\mathrm{GF}(2)$ |
| `invertible` | bool | True iff $M$ has full rank |
| `order` | int | Least $k$ with $M^k = I$, the identity matrix, which for a bit-permutation $P$ is the least $k$ with $P$ applied $k$ times leaving every bit where it started (absent for sizes $> 320$) |
| `branch_number` | int | Branch number in the word size the designers use, recorded when the specification states it |
| `mds` | bool | True iff the matrix is MDS in that word size |
| `hamming_weight` | int | Total number of $1$ entries in the matrix |
| `inversion`<sup>†</sup> | int | Number of pairs of positions the permutation puts out of order, for an entry that acts as one; see Notes 18 |
| `orbit` | int | Number of orbits on the $N$ rows of the smallest shift $\sigma\colon i \mapsto i + k \pmod N$ that commutes with $M$; see Notes 11 |
| `hamming_weight_per_row` | tuple[int] | Number of $1$ entries per row |
| `fixed_points` | tuple[int] | Indices $i$ with $M e_i = e_i$, that is, the bits a permutation leaves in place (only for square entries) |
| `cycle_lengths` | tuple[int] | Sorted cycle-length multiset, when the entry acts as a bit-permutation |
| `disjoint_cycles` | tuple | Explicit disjoint-cycle decomposition, for a bit-permutation |
| `matrix`<sup>*</sup> | tuple[str] | One bit-string per row; character `c[j]` is the bit in column $j$. Present for every matrix entry, including one that also carries an `augmentation`; absent only for a bit-permutation |
| `perm`<sup>*</sup> | tuple[int] | Permutation $P$, with `P[i]` the destination index of input bit $i$, that is, `output[P[i]] = input[i]`. The matrix of $P$ is $M$ with $M[P[i]][i] = 1$, which the loader builds on demand |
| `trivium` | str | Lesser-known aside about the entry, such as the etymology of the cipher's name; never a cryptographic property |
| `alias` | str | Present instead of a body when the key resolves to another entry, which is where the entry is held |
| `matrix_parts`, `matrix_part` | int | Present only when a body is continued across part files; see Organisation |

### Notes

1. A word of $n$ bits is numbered from the most significant, so bit $0$ of a $32$-bit word carries weight $2^{31}$. This is how the specifications write it, and it is what fixes the matrix of an entry defined by rotations: read the other way round, a left rotation becomes a right one and the matrix comes out transposed. `ZUC.L1` and `ZUC.L2` are transposes of one another, the rotation offsets of the two, $0, 2, 10, 18, 24$ and $0, 8, 14, 22, 30$, being negatives modulo $32$; `ZUC.L1` is the `SM4` layer, so `SM4` and `ZUC.L2` are transposes too.

2. Convention is uppercase Latin characters with only dot allowed, this enforces uniformity and ASCII searchability, but it destroys the original typographic formatting used by the designers, such as mixed case (e.g., `Midori`), non-Latin characters, subscript notation (e.g., $L_0$, $\sigma_0$), hyphen (like `SHA-3`) and space (like `SNOW 3G`).

3. `canonical_name` is used to preserve the original formatting as intended by the designer(s). Where a family is named after its authors rather than a cipher, the family element gives the author surnames and the layer element the designation of the matrix.

4. Binary-field entries `GF<n>.MUL` and `GF<n>.SQR` represent multiplication-by-$x$ (the companion matrix of the irreducible polynomial) and the Frobenius squaring map, respectively, over $\mathrm{GF}(2^n)$, one reduction polynomial per degree, named in `formula`. Entries `GF<n>.ECCSQR` are the squaring matrices of the binary-curve elliptic-curve setting, taken from [`Binary_ECC`](https://github.com/starj1023/Binary_ECC); it is a different basis from the cipher-oriented entry of the same degree, and the permutation between it is not published there.

5. Each URL is prefixed with `URL: ` only when more than one URL appears in the same `source` field; multiple URLs are separated by `; `.

6. The `augmentation` field, when present, records that the matrix is built by composing other catalogued entries via `block_diag(...)` (block-diagonal sum), `kron(A, B)` (Kronecker product), `I_n` (identity of size $n$), or matrix product (`*`). For example, `ASCON` carries `augmentation: block_diag(ASCON.SIGMA0, ..., ASCON.SIGMA4)` because the 320-bit linear layer is the direct sum of five 64-bit lane mixers; `ICEPOLE` carries `augmentation: kron(ICEPOLE.SLICE, I_64)` because the 1280-bit linear layer is the slice-wise tensor of a $20 \times 20$ slice mixer with $I_{64}$. The expression is an explanation of how the matrix is put together, not a substitute for it: every such entry also carries its `matrix` body in full, so a reader lifting a binary matrix out of the catalogue never has to evaluate one.

7. `AES.SHIFTROW` is catalogued only as a $128 \times 128$ matrix entry (not as a separate permutation), because the matrix form fully captures the bit-permutation; the permutation field can be recovered by reading the unique `1` in each row.

8. Fields that only make sense for square matrices (`involution`, `symmetric`, `invertible`, `order`, `fixed_points`, `cycle_lengths`, `disjoint_cycles`, `orbit`) are omitted from rectangular matrix entries (e.g., the `GF<n>.MUL` companion matrices, of shape $n \times (2n - 1)$). Any field whose value would be `null` is also omitted.

9. Every `matrix` row is a quoted string. An unquoted bit-string such as `0001100010111011` is a valid YAML 1.1 octal integer, which a YAML parser returns as a number with the leading zeros gone.

10. `SHA256.SMALLSIGMA0` and `SHA256.SMALLSIGMA1` are the FIPS 180-4 matrices, whose third term is a shift ($\mathrm{SHR}^3$ and $\mathrm{SHR}^{10}$) rather than a rotation. Several circuit corpora implement a rotate-only variant under those names; that variant is a different matrix and is not catalogued here. The eight `SHA256.*` and `SHA512.*` entries number a word from the least significant bit, against Note 1 and the rest of the catalogue: each is therefore the transpose of what the other numbering gives, and each says so in its `note`. The message expansion that surrounds it adds modulo $2^{32}$ or $2^{64}$, so it is not linear over $\mathrm{GF}(2)$ and no matrix for it exists.

11. `orbit` stands in for the higher-field structure of the matrix. Let $k$ be the smallest positive shift with $\sigma_k\colon i \mapsto i + k \pmod N$ commuting with $M$ on both rows and columns. Minimality forces $k$ to divide $N$, so $k$ is at once the shift and the number of orbits of $\sigma_k$ on the $N$ rows, which is the value recorded; $\sigma_k$ then has order $N / \mathrm{orbit}$. An orbit count of $N$ means no nontrivial shift commutes, hence no such structure. For `AES.MIXCOLUMN` the value is $8$, the byte rotation $i \mapsto i + 8$ of the underlying $\mathrm{GF}(2^8)$ MDS matrix, giving $8$ orbits of length $4$.

12. No implementation cost is recorded, neither gate count nor depth. Where a body or a cross-reference comes from the [NIST Circuit Complexity project](https://csrc.nist.gov/Projects/circuit-complexity/list-of-circuits), `source` points at the project and the circuit it publishes can be read there. A file name in that project lists every cipher one matrix serves, which is where several of the cross-references come from; the name each cipher gives its own layer is not recorded there, so a `reuse` entry is written as `Cipher.Layer` only where a specification was read.

13. Matrices whose entries are $0/1$ but that a specification applies to $c$-bit cells are catalogued the way the source paper writes it. `MIDORI`, `DL18C` and `SPOOK.DBOX` are stored as the binary expansion $\mathrm{kron}(M, I_c)$, while `AETHER.MB` is stored as the $16 \times 16$ matrix over nibbles printed in its specification, with the expansion given in `formula`.

14. Not every relation the catalogue records is stated by the specifications. Where it is not, it was established here by comparing the bodies, which applies to every `reuse`, every `similarity`, and the keys of Notes 17. The reasoning sits in the `note` of the entries concerned, so a reader can weigh it.

15. `reuse` lists the layers elsewhere whose body is this one, byte for byte, written `CIPHER.LAYER`. It is recorded on the earlier publication, and it does not wait for the later design to say where the matrix came from: `PRIDE.L0` lists `MIDORI.MIXCOLUMN` although the Midori specification attaches no citation to the matrix, and `SM4` lists `ZUC.L1` although the two are simply the same definition. Where a design does acknowledge the source, as MANTIS does for Midori, the `note` says so.

16. `similarity` is the weaker relation: the entries carried to this one by a permutation of the rows, of the columns, or of both. It is searched against four forms of the other entry, its matrix as it stands, its transpose, its inverse and the transpose of its inverse, and the `note` says which form it was. The matrix is not the same, but a circuit for one becomes a circuit for the other by renaming wires, and for the inverse cases by reversing the direction as well. Each such entry is kept in its own right, since a permutation of a matrix is not that matrix. Two bit-permutations of a size are always related this way, so that case is not recorded. The relation is decided rather than searched for within a budget: a permutation of rows and columns is exactly an isomorphism of the bipartite row/column graph, so each question is graph isomorphism and is answered.

17. Some keys no longer carry a body. `SKOP15.IS16` is retired into `JOLTIK`, and `MIDORI` and `ZUC.L1` resolve to `PRIDE.L0` and `SM4`, each pair having been found byte-identical. `BAKSHEESH` is now `BAKSHEESH.P` for the bit permutation and `BAKSHEESH.T` for the matrix, the cipher being specified with either. `GF163_0`, `GF283_0` and `GF571_0` lost the suffix, and `GF163_1`, `GF283_1` and `GF571_1` are gone, a second reduction polynomial with no recorded first use not earning a second entry. The four `SHA2.*` sigma keys are now `SHA256.*`, the word width having to be named once `SHA512.*` joined it, and the six keys that carried an underscore are now `SKOP15.S4GF8`, `SKOP15.IS4GF8`, `SKOP15.S8GF4`, `SKOP15.IS8GF4`, `KLSW17.S8GF4` and `KLSW17.IS8GF4`. Each old spelling is kept in the `aliases` of the entry. [`visualisation.md`](visualisation.md) lists the keys that resolve elsewhere.

18. `inversion` counts the pairs of positions the permutation puts out of order, that is the pairs $i < j$ with $P[i] > P[j]$. It is the number of adjacent swaps needed to sort it back to the identity, so it says how far the permutation moves its inputs, and it runs from $0$ for the identity to $N(N-1)/2$ for the reversal. It is recorded for a `perm` entry and for a matrix whose body is a permutation matrix. The parity of the permutation is this count modulo two, so it is not recorded separately, and it is invisible in the matrix itself: over $\mathrm{GF}(2)$ every permutation matrix has determinant $1$. That parity is what decides the fifteen puzzle, whose position is reachable exactly when the permutation of the tiles, composed with the moves of the blank, is even. Of the bit-permutations catalogued here, `GLEEOK.PI128B3`, `GLEEOK.PI256B3`, `SPEEDY.SC` and `TWINKLE.LANEROTATION0` have an odd count and the rest an even one.

19. Two matrices can share a size, a Hamming weight and a coarse invariant while being different, and a total weight alone is not evidence of anything. `ANUBIS` and `CLEFIA.M0` are the same Hadamard array $(1, 2, 4, 6)$ over $\mathrm{GF}(2^8)$, differing only in the reduction polynomial, $x^8 + x^4 + x^3 + x + 1$ for the first and $x^8 + x^4 + x^3 + x^2 + 1$ for the second. Both carry $216$ ones, which is why a corpus files it under one name, but the two are not related by any permutation of rows and columns: the multiset of row weights already differs, $12$ rows of weight $5$, $12$ of $7$ and $8$ of $9$ against $16$, $4$ and $12$. The `hamming_weight_per_row` of each entry settles this at a glance, and `similarity` records only relations a search has established.

20. A trailing `T` in a key is not a transpose. `BEANIE.MIXCOLUMNST` is the `MixColumnsT` of the BEANIE tweakey schedule, that cipher naming its whole tweakey path `SubCellsT`, `ShiftRowsT` and `MixColumnsT`, and `BAKSHEESH.T` is the matrix the BAKSHEESH specification calls $T$. Neither is the transpose of anything. Where a transpose really is meant the `note` says so in words: `ZUC.L1` and `ZUC.L2` are transposes of one another, and no key in the catalogue is spelled to indicate it.

## Python Loader

### Installing / Importing

[`bigfatmatrix.py`](bigfatmatrix.py) is a lazy loader that exposes every YAML entry as a Python object; no data file is read until the first access. It requires Python 3.11+ on top of [PyYAML](https://pypi.org/project/PyYAML/); `numpy` is optional and used only by `MatrixEntry.as_numpy()`.

With all files (including YAML data files) available in the working directory (or on `sys.path`), the following should work inside a Python REPL:

```python
import bigfatmatrix
print(bigfatmatrix.last_update)         # Prints the date in the README heading
```

### Single-Entry Access

The following data types (case-insensitive) are accessible:
- `MatrixEntry` is the Python class wrapping a single YAML entry (matrix or permutation).
- `MatrixGroup` groups related entries under a common cipher prefix (e.g., all `AES.*` entries together).

```python
m = bigfatmatrix.aes_mixcolumn          # MatrixEntry('AES.MIXCOLUMN', shape=32x32)
m = bigfatmatrix['AES.MIXCOLUMN']       # Bracket access (case-insensitive)
print(m.canonical_name)                 # Prints ('AES', 'MixColumns')
print(m.rows, m.cols)                   # Prints 32 32
print(m.matrix[0])                      # Prints '00000001100000011000000010000000'

ints = m.as_int_matrix()                # Tuple of tuples of 0/1
arr  = m.as_numpy()                     # numpy.ndarray, dtype=uint8 (needs numpy)

print(m.year)                           # Prints (1998, 2001)
print(m.origin)                         # URL string
print(m.note)                           # Free-form note
print(m.fields)                         # List of available field names
print(m.to_dict())                      # Raw YAML dict copy

# Case-insensitive access
assert bigfatmatrix.AES_MIXCOLUMN == bigfatmatrix.aes_mixcolumn
```

### Group Access

Ciphers with multiple linear layers are accessible as `MatrixGroup` objects:

```python
gf128 = bigfatmatrix.gf128              # MatrixGroup('GF128', members=['mul', 'sqr'])
print(gf128.mul)                        # MatrixEntry('GF128.MUL', shape=128x255)
for m in gf128:
    print(m.name, m.rows, 'x', m.cols)

pyjamask = bigfatmatrix.pyjamask        # MatrixGroup for PYJAMASK.M0..M3, MK
print(len(pyjamask))                    # Prints 167
```

### Permutations

A bit-permutation reads either as the tuple or as the binary permutation matrix:

```python
p = bigfatmatrix['GIFT.128']            # MatrixEntry('GIFT.128', perm size=128)
print(p.size)                           # Prints 167
print(p.perm[:8])                       # Prints (0, 33, 66, 99, 96, 1, 34, 67)

P = p.as_permutation_matrix()           # Tuple of tuples with M[P[i]][i] = 1
P = p.as_int_matrix()                   # Same thing, uniform with matrix entries
rows = p.as_matrix_rows()               # Tuple of bit-strings
P = bigfatmatrix.as_matrix('GIFT.128')  # Matrix form of any entry by name
```

### SageMath

Running inside SageMath, attribute and bracket access return the Sage-native object directly, so no separate loader is needed:

```python
m = bigfatmatrix.aes_mixcolumn          # Matrix(GF(2), 32, 32, [[...]])
p = bigfatmatrix.present                # sage.combinat.permutation.Permutation
```

In plain Python the conversion is explicit, and a permutation converts either way:

```python
m = bigfatmatrix['AES.MIXCOLUMN'].to_sage()             # Matrix(GF(2), ...)
p = bigfatmatrix['GIFT.128'].to_sage()                  # Permutation
P = bigfatmatrix['GIFT.128'].to_sage(as_matrix=True)    # Matrix(GF(2), ...)
```

### Wildcard Search

`bigfatmatrix.find(pattern)` returns a dict of all entries matching a wildcard pattern. Bracket notation `bigfatmatrix['pattern']` is equivalent for wildcards:

```python
matches = bigfatmatrix.find('GF*.MUL')      # All multiplication tables
matches = bigfatmatrix.find('AES.*')        # All AES.* entries
matches = bigfatmatrix.find('SHA*')         # All SHA-* entries
matches = bigfatmatrix['*.PERM*']           # Bracket-form wildcard

for name, m in bigfatmatrix.find('PYJAMASK.*').items():
    print(name, m.rows, 'x', m.cols)

# Exact bracket access (non-wildcard, case-insensitive)
m = bigfatmatrix['AES.MIXCOLUMN']
```

### Listing All Entries

```python
all_keys = bigfatmatrix.yaml.all_names()    # Sorted list of every UPPERCASE key
print(len(all_keys))                        # Prints 167
data = bigfatmatrix.yaml.all_entries()      # Full dict: key -> raw YAML dict
```

### Raw YAML Access

Raw dictionary access is available via the `yaml` proxy:

```python
data = bigfatmatrix.yaml.aes_mixcolumn      # Plain Python dict with all YAML fields
print(data['rows'])                         # Prints 167
print(data['year'])                         # Prints [1998, 2001] (raw list)
data = bigfatmatrix.yaml['BAKSHEESH.T']     # Same, case-insensitive bracket access
```

### Command-Line

Quick lookup for one or more keys directly from the shell:

```bash
python bigfatmatrix.py AES.MIXCOLUMN GIFT.128 BAKSHEESH.T
```

### Notes

1. Python identifiers cannot contain a dot, so dotted entry keys are accessed via bracket notation (`bigfatmatrix['AES.MIXCOLUMN']`) or via group attributes (`bigfatmatrix.aes.mixcolumn`).

2. `find('pattern')` and `bigfatmatrix['pattern']` support `*` and `?` wildcards (case-insensitive) and always return a `dict`. For an exact lookup, `bigfatmatrix['KEY']` behaves identically to attribute access.

3. The loader is lazy. Importing `bigfatmatrix` does not parse any YAML file immediately; the data files are read on first access, and a band published as several parts is merged there.

4. Attribute access hands out tuples, never lists, so an entry cannot be mutated by accident. The `yaml` proxy returns the raw parsed dictionary, where a sequence is still a list.