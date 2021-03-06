from algorithms.utils import positive_mod, sum_mod2
from typing import List


def reconstruct_deletion(vector: List[int], c: int, d: int, u: int, P: int) -> List[int]:
    """Reconstruct the vector after a deletion has occured.
    does not change the original vector (does not work in place).

        Parameters:
                vector (List[int]): the vector after the deletion has occured.
                c (int): the weighted sum of the (original) vector is congruent to c (mod P).
                d (int): the sum of the (original) vector is congruent to d (mod 2).
                u (int): the first index where a deletion may have occured.
                P (int): the max distance of the deletion from u.

        Returns:
                reconstructed_vector (List[int]): the vector after reconstructing the original vector.
    """
    vector_copy = vector.copy()  # working on a copy, so we won't change the passed vector
    del_val = 0 if sum_mod2(vector_copy) == d else 1
    end = min(len(vector_copy) - 1, u + P - 2)  # this is u + P - 2 from the paper
    errd = vector_copy.copy()
    errd = errd[u:end + 1]

    c_tag = (sum([i * e for i, e in enumerate(vector_copy[:end + 1])]) + sum([((end + 1) + i + 1) * e for i, e in enumerate(vector_copy[end + 1:])])) % P

    delta = c - c_tag
    delta = positive_mod(delta, P)

    deleted_index = end + 1

    if del_val == 0:
        count_ones = sum(errd)
        for i in range(len(errd)):
            if count_ones == delta:
                deleted_index = i + u
                break
            if errd[i] == 1:
                count_ones -= 1
    else:
        delta_tag = (delta - u - sum(errd)) % P
        delta_tag = positive_mod(delta_tag, P)

        count_zeros = 0
        for i in range(len(errd)):
            if count_zeros == delta_tag:
                deleted_index = i + u
                break
            if errd[i] == 0:
                count_zeros += 1

    vector_copy.insert(deleted_index, del_val)
    return vector_copy
