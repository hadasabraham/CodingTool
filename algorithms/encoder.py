from math import log, ceil
from typing import NewType, Tuple, List, Optional



# will probably be used with n := log_n
def cr(n, w):
    out = w
    while len(out) < n:
        out += w
    return out[:n]


# Time complexity: O(log(n, base=q))
# Place complexity: O(log_q) * O(log(n, base=q))
def q_ary(n, q, width):
    if n == 0:
        return [0] * width
    if q == 2:  # short-circuit for binary
        return [int(p) for p in format(n, 'b').zfill(width)]
    nums = []
    while n:
        n, r = divmod(n, q)
        nums.append(r)
    nums.extend([0] * (width - len(nums)))
    return list(reversed(nums))


def q_ary_rev(n_list: List, q):
    result = 0
    if q == 2:
        for digits in n_list:
            result = (result << 1) | digits
        return result
    for digits in n_list:
        result = (result * q) + digits
    return result


"""

n * log_n       iterations
n   OR   log_n  new windows need to be compared per iteration
n               comparisons for each window
log_n           operations for each comparison

TOTAL:

TIME                       SPACE
-----                      -----
  n^3 * (log_n)^2    |       log_n          # when saving space
  n^2 * log_n        |       n * log_n      # when saving time

"""


class Encoder:
    # region Parameters
    w: List[int]
    n: int
    q: int
    log_n: int
    k: int
    zero_rll: int
    type: int
    redundancy: int
    # endregion

    def __init__(self, alg_type: str, redundancy, verbose_mode: bool, q: int = 2):
        assert 1 <= redundancy <= 2
        assert 2 <= q
        assert alg_type in ["time", "space"]
        self.type = 1 if alg_type == "space" else 2  # 1 saves space but costs more time
        self.redundancy = redundancy
        self.zero_rll = 3 - redundancy
        self.verbose = verbose_mode
        self.q = q
        self.text_to_print = ""

    def input(self, w: List):
        # Tested: `self.w = w` happens by reference (since `list` is mutable)
        self.w = w
        self.n = len(w) + self.redundancy
        self.log_n = ceil(log(self.n, self.q))
        self.k = 2 * self.log_n + 2
        self.zero_rll += self.log_n
        return self

    def encode(self, _debug_no_append=False):
        if self.redundancy == 2:
            self.w.insert(0, 0)
        if not _debug_no_append:
            self.w.append(1)
            for i in range(self.zero_rll):
                self.w.append(0)
        if self.verbose:
            self.text_to_print += f'w0      ={self.w}\n'
            #print('w0     =', self.w)

        # Run algorithm
        return self.eliminate().expand()

    def eliminate(self):
        found_identical_or_zero = True
        while found_identical_or_zero:
            found_identical_or_zero = False

            if self.type == 1:  # O(n^3 * log_n)
                for i in range(len(self.w) - self.k):
                    break_out = False
                    for j in range(i + 1, len(self.w) - self.k + 1):
                        if self.w[i:i + self.k] != self.w[j:j + self.k]:  # not self.identical(i, j):
                            continue
                        found_identical_or_zero = True
                        self.w[i:i + self.k] = []
                        self.w[:0] = [0] + q_ary(i, self.q, self.log_n) + q_ary(j, self.q, self.log_n)
                        if self.verbose:
                            self.text_to_print += f'w1      ={self.w}\n'
                            #print('w1     =', self.w)

                        break_out = True
                        break
                    if break_out:
                        break
            elif self.type == 2:  # O(n^2 * log^2_n)
                seen_windows = {}
                piw_i = -1  # piw: primal identical windows
                piw_j = -1
                for j in range(len(self.w) - self.k + 1):
                    hash_j = str(self.w[j:j + self.k])
                    # change i, j if found a better pair
                    # notice that < is necessary because if i < j < k are identical windows we want (i,j)
                    if hash_j in seen_windows.keys():
                        if piw_i == -1 or (seen_windows[hash_j] < piw_i):
                            piw_i = seen_windows[hash_j]  # already seen so this window is the first of the couple
                            piw_j = j
                    else:
                        seen_windows[hash_j] = j
                if piw_i >= 0:
                    i, j = piw_i, piw_j
                    found_identical_or_zero = True
                    self.w[i:i + self.k] = []
                    self.w[:0] = [0] + q_ary(i, self.q, self.log_n) + q_ary(j, self.q, self.log_n)
                    if self.verbose:
                        self.text_to_print += f'w1      ={self.w}\n'
                        #print('w1     =', self.w)

            if not found_identical_or_zero:
                zero_window_index = -1
                curr_length = 0
                for curr_index in range(len(self.w) - 1):
                    if self.w[curr_index] == 0:
                        curr_length += 1
                        if curr_length == self.zero_rll:
                            zero_window_index = curr_index - self.zero_rll + 1
                            break
                    else:  # elif self.w[curr_index] != 0:
                        curr_length = 0
                if zero_window_index >= 0:
                    self.w[zero_window_index:zero_window_index + self.zero_rll] = []

                    # One-by-one appending in O(len(appended))
                    prepended = [1] + q_ary(zero_window_index, self.q, self.log_n)
                    for p in reversed(prepended):
                        self.w.insert(0, int(p))
                    found_identical_or_zero = True
                    if self.verbose:
                        self.text_to_print += f'w2      ={self.w}\n'
                        #print('w2     =', self.w)
        return self

    def expand(self):
        while len(self.w) < self.n:
            # Go over all words of length log_n in O(n) time, and for each word,
            # check that it does not exist in w in O(n * log_n) time,
            # and that it is not equal to some Cr_log_n(w[-i]) in O(log^2_n * log_log_n) time.
            # Total: O(n * (n * log_n + log^2_n * log_log_n)) = O(n^2 * log_n) time.
            # Space: O(log_n) additional space.

            # u is a q_ary word of length log_n
            good_u: Optional[List] = None
            for u in range(self.n):
                next_u = False
                list_u = q_ary(u, self.q, self.log_n)
                for curr in range(len(self.w) - self.log_n + 1):
                    if list_u == self.w[curr:curr + self.log_n]:
                        next_u = True
                        break
                    # print('Truly,', self.w[curr:curr + self.log_n], 'does not equal', list_u)
                if next_u:
                    continue
                for i in range(1, self.log_n):
                    cr_i = cr(self.log_n, self.w[-i:])
                    if list_u == cr_i:
                        next_u = True
                        break
                    # print('Truly,', cr_i, 'does not equal', list_u)
                if next_u:
                    continue
                good_u = list_u
                # print("good_u =", good_u)
                break
            if good_u is None:
                raise Exception("B contains all words of length log_n.")
            self.w.extend(good_u)
            if self.verbose:
                self.text_to_print += f'w      ={self.w}\n'
                #print('w+     =', self.w)
        return self

    def output(self):
        self.w = self.w[:self.n]
        return self.w, self.text_to_print
        # Comment out the above and uncomment below to have O(n) place for the output only
        # return self.w[:self.n]
