from collections import deque
from typing import Iterable, Optional, Callable


class AutoIncQueue(deque):
    def __init__(self, iterable: Optional[Iterable] = None,
                 maxlen: Optional[int] = None,
                 autoincrement: bool = False,
                 increment_until: Optional = None,
                 increment_func: Optional[Callable] = None):
        if iterable is None:
            iterable = ()
        deque.__init__(self, iterable=iterable, maxlen=maxlen)
        self._autoincrement = autoincrement
        self._increment_until = increment_until
        self._prev = iterable[0] if iterable else None
        self._increment_func = increment_func if increment_func else lambda n: n + 1

    @property
    def autoincrement(self):
        return self._autoincrement

    @autoincrement.setter
    def autoincrement(self, flag: bool):
        self._autoincrement = flag

    @property
    def increment_until(self):
        return self._increment_until

    @increment_until.setter
    def increment_until(self, val: int):
        self._increment_until = val

    @property
    def prev(self):
        return self._prev

    def pop(self, i: int = ...):
        if len(self) == 1 and (i is None or i == 0) and self._autoincrement and self[-1] < self._increment_until:
            self.appendleft(self._increment_func(self[-1]))
        self._prev = self[-1]
        return deque.pop(self)

    def popleft(self):
        if len(self) == 1 and self._autoincrement and self[0] < self._increment_until:
            self.append(self._increment_func(self[0]))
        self._prev = self[0]
        return deque.popleft(self)

    # Assumes value is found; otherwise, prev is wrong
    def remove(self, value) -> None:
        if len(self) == 1 and value == self[0] and self._autoincrement and self[0] < self._increment_until:
            self.append(self._increment_func(self[0]))
        self._prev = value
        return deque.remove(self, value)

    # Supported base methods:

    def insert(self, i: int, x) -> None:
        deque.insert(self, i, x)

    def append(self, x) -> None:
        deque.append(self, x)

    def appendleft(self, x) -> None:
        deque.appendleft(self, x)

    def clear(self) -> None:
        deque.clear(self)

    def extend(self, iterable: Iterable) -> None:
        deque.extend(self, iterable)

    def extendleft(self, iterable: Iterable) -> None:
        deque.extendleft(self, iterable)

    def empty(self) -> bool:
        return len(self) == 0
