from typing import Optional

# Fenwick Tree:
# Internally one-based indexing, externally zero-based indexing
# Source in C++: https://cp-algorithms.com/data_structures/fenwick.html
# Independently moved to Python


class FenwickTree(object):
    def __init__(self, n=0, arr=None):
        if arr is not None:
            n = len(arr)
        if n == 0:
            raise Exception("Data structure size must be positive.")
        self._n = n + 1
        self._bit = [0] * self._n
        if arr is not None:
            for i in range(n):
                self.add_range(i, i, arr[i])

    # from start=1 to end=idx
    def sum(self, idx):
        ret = 0
        idx += 1
        while idx > 0:
            ret += self._bit[idx]
            idx -= idx & -idx
        return ret

    def sum_range(self, left, right):
        return self.sum(right) - self.sum(left - 1)

    def add(self, idx, delta):
        idx += 1
        while idx < self._n:
            self._bit[idx] += delta
            idx += idx & -idx

    def add_range(self, left, right, delta):
        self.add(left, delta)
        self.add(right + 1, -delta)

    def __getitem__(self, idx):
        ret = 0
        idx += 1
        while idx > 0:
            ret += self._bit[idx]
            idx -= idx & -idx
        return ret

    def __len__(self):
        return self._n - 1

    def __iter__(self):
        # generator expression
        return (self[idx] for idx in range(self._n - 1))

    def __eq__(self, other):
        return [i for i in self] == other

    @property
    def values(self):
        return [i for i in self]
