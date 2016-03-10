# Conway's Game of Life

Featuring:

- an infinite field (dynamic resizing);
- efficient in CPU and memory; and
- a simple implementation in Python.

It only stores living cells (memory efficient) and only processes living cells
plus neighbors (CPU efficient).

Performance: 384ns per tick on a 90x51 field with a population of 16.

License: BSD (2-clause)

---

Operations read oldcells and set newcells. At the end of a tick, changes are
applied.

Possible performance improvement: queue operations instead of deep copying, and
perhaps garbage cleanup periodically instead of at every setCell.

