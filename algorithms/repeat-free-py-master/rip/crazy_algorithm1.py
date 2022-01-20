from math import log, ceil
from typing import Optional, List, NewType, Tuple, Dict
from rip.autoinc_queue import AutoIncQueue
from rip.avl_rank import AvlRankTree as DeltaTree
from rip.hashtable import ChainedHashtable as Hashtable, LinkedList, Link

# Using a dictionary to parse input, because all relevant complexity times are O(1):
# https://www.ics.uci.edu/~brgallar/week8_2.html

""" Data Classes from Python 3.7 are AMAZING
from dataclasses import dataclass, field

@dataclass
class Window:
    values: List[int] = field(default_factory=list)
    index: int = field(default=0, compare=False)
"""


# TODO: Sphinx

# User-defined types
bit = NewType('bit', int)
window = NewType('window', Tuple[bit, ...])


# will probably be used with n := log_n
def cr(n, w) -> List[bit]:
    out = w
    while len(out) < n:
        out += w
    return out[:n]


def b(n, width: int = 0) -> List[bit]:
    return list(format(n, 'b').zfill(width))


def q_ary(n, q, width) -> List[bit]:
    if n == 0:
        return [bit(0)] * width
    nums = []
    while n:
        n, r = divmod(n, q)
        nums.append(r)
    return list(reversed(''.join(nums).zfill(width)))


class Algorithm1:
    # region Parameters
    # FIELD     TYPE                    SKETCH NAME     DOMAIN          RANGE           DESCRIPTION
    input:      List[bit]               # s             [n]             bit             .
    w:          Dict[int, bit]          # w             [len]           bit             .
    n:          int                     # n             -               -               .
    len:        int                     # n_tag         -               Max Ext. Index  .
    q:          int                     # q             -               -               .
    log_n:      int                     # log_n         -               -               .
    k:          int                     # k             -               -               .
    index_in:   Optional[DeltaTree]     # M             Ext. Index      Link@index_ex   .
    index_ex:   Optional[LinkedList]    # L             Int. Index      Link@index_in   .
    windows:    Optional[Hashtable]     # W             window          Link@index_ex   .
    queue:      Optional[AutoIncQueue]  # Q             -               Link@w          .
    # endregion

    def __init__(self, s, q: int = 2):
        if not isinstance(s, list):
            raise Exception("Input must be a list.")
        if q != 2:
            raise NotImplementedError()
        self.input = s
        self.w = dict()
        self.n = len(s) + 1
        self.len = 0
        self.q = q
        self.log_n = ceil(log(self.n, self.q))
        self.k = 2 * self.log_n + 2
        self.index_in = None
        self.index_ex = None
        self.windows = None
        self.queue = None

    def encode(self, _debug_no_append=False):
        w_list = self.input + [bit(1)] + ([bit(0)] * (self.log_n + 1)) if not _debug_no_append else self.input
        self.w = dict(zip(range(len(w_list)), w_list))
        self.len = len(self.w)

        # Initialize data structures (see README for details)

        # index_{ex,in} are INTERTWINED
        self.index_ex = LinkedList.from_iterable(range(self.len))
        self.index_in, node_list = DeltaTree.from_sorted(list(self.index_ex))
        node_iter = iter(node_list)
        for link in self.index_ex:
            link.value = next(node_iter)

        self.windows = Hashtable(self.len)
        self.queue = AutoIncQueue(range(self.len), increment_until=self.len)

        # Run algorithm
        self.eliminate()
        self.expand()

    def eliminate(self):
        while True:
            if not self.queue.empty():
                # There are more input bits to check
                j_ex = self.queue.popleft()
                if j_ex + self.k >= self.len:
                    # TODO: When no more windows, check (log_n + 1)-RLL
                    # raise NotImplementedError()
                    break
                win_j: Optional[window] = window(tuple([self.w[key] for key in range(j_ex, j_ex + self.k)]))
                link_index_ex_j: Link = self.index_in.get(j_ex)
                j_in = link_index_ex_j.key
                assert (j_ex == link_index_ex_j.value.value)

                link_index_ex_i: Optional[Link] = self.windows.get(win_j)
                if link_index_ex_i is not None:
                    i_in, i_ex = link_index_ex_i.key, link_index_ex_i.value.value
                    self.index_in.delta_add(i_ex + self.k - 1, len(self.index_in), 1)
                    self.index_in.delta_add(0, i_ex + self.k - 2, -(self.k - 1))
                    self.queue.extendleft(range(0, self.k - 1))
                    for i in range(i_ex, i_ex + self.k):
                        del self.w[i]
                    prepended = [0] + b(i_ex, self.log_n) + b(j_ex, self.log_n)
                    self.w += dict(zip(range(len(prepended)), prepended))

                    # self.
                    # TODO: Remove link@windows and THEN this link
                    self.windows_id.remove(i_in)

                link_window = self.windows.put(win_j, link_index_ex_j)

                # TODO: This is needed to remove the <=(2k-1) windows that are invalidated after window removal
                self.windows_id.insert(j_in, link_window)

            else:  # Queue is empty: either RLL, case 2 or done (not sure which)
                # pass
                break

    def expand(self):
        while len(self.w) < self.n:
            # raise NotImplementedError()
            break
        self.w = self.w[:self.n]

    def output(self):
        return self.w
