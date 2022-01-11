from rip.fenwick import FenwickTree
from rip.avl_rank import AvlRankTree
# from crazy_algorithm1 import *

# region Unit Tests

test_silent = 2


def test_print(i, b, name):
    if test_silent == 0:
        print("TEST", "PASSED" if b else "FAILED", "-", name, i)
    elif test_silent == 2 and not b:
        print("TEST FAILED -", name, i)
    return b


def test_fenwick():
    test_name = 'fenwick'
    tests_passed = 0
    arr = [1, 2, 3, 4, 5]
    tree = FenwickTree(arr=arr)
    tests_passed += test_print(1, tree == [1, 2, 3, 4, 5], test_name)
    tree.add_range(1, 3, -2)
    tests_passed += test_print(2, tree == [1, 0, 1, 2, 5], test_name)
    tests_passed += test_print(3, tree[1] == 0, test_name)
    if tests_passed == 3:
        print("Congrats! All tests for fenwick passed.")
    else:
        print("Sorry...")


# region Need Refactoring
def test_avl_rank():
    test_name = 'avl_rank'
    tests_passed = 0
    inputs = [5, 3, 6, 1, 4]
    tree = AvlRankTree()
    for i in inputs:
        tree.insert(i)
    tests_passed += test_print(1, tree.list(1, 6)[0] == [1, 3, 4, 5, 6], test_name)
    # print(tree.list(1, 6))
    tree.delta_add(1, 4, delta=5)  # add D=5 to [1, 4]
    # print(tree.list(1, 6))
    # input()
    for times in range(3):
        existent, existent_key, _, rank, deltas = tree.find(5)
        tests_passed += test_print(times + 2 + 1100, deltas == 0, test_name)
        tests_passed += test_print(times + 2 + 1200, rank == 4 + times, test_name)
        tests_passed += test_print(times + 2 + 1300, existent_key == 5, test_name)
        tests_passed += test_print(times + 2 + 1400, existent is True, test_name)
        existent, existent_key, _, rank, deltas = tree.find(3)
        tests_passed += test_print(times + 2 + 2100, deltas == 5, test_name)
        tests_passed += test_print(times + 2 + 2200, rank == 2 + times, test_name)
        tests_passed += test_print(times + 2 + 2300, existent_key == 3, test_name)
        tests_passed += test_print(times + 2 + 2400, existent is True, test_name)
        existent, existent_key, _, rank, deltas = tree.find(4)
        tests_passed += test_print(times + 2 + 3100, deltas == 5, test_name)
        tests_passed += test_print(times + 2 + 3200, rank == 3 + times, test_name)
        tests_passed += test_print(times + 2 + 3300, existent_key == 4, test_name)
        tests_passed += test_print(times + 2 + 3400, existent is True, test_name)
        existent, existent_key, _, rank, deltas = tree.find(0)
        tests_passed += test_print(times + 2 + 4100, deltas == 0, test_name)
        tests_passed += test_print(times + 2 + 4200, rank == (times > 0), test_name)
        tests_passed += test_print(times + 2 + 4300, (existent_key is None) == (times == 0), test_name)
        tests_passed += test_print(times + 2 + 4400, (existent is False) == (times == 0), test_name)
        if times == 0:
            tree.insert(0)
        elif times == 1:
            tree.insert(2)
    if tests_passed == 1 + 3 * 4 * 4:
        print("Congrats! All tests for avl_rank passed.")
    else:
        print("Sorry... Only", tests_passed, "passed for avl_rank.")
# endregion


def test_all():
    test_fenwick()
    test_avl_rank()
    test_lambda_as_arg()


def test_more():
    print("MORE tests!")
    seq = [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0]
    fenwick = FenwickTree(arr=seq)
    print(fenwick.values)
    print(seq[-4:])


def _lambda_as_arg(func):
    ret = func()
    return ret


def test_lambda_as_arg():
    test_name = 'lambda_as_arg'
    ret = _lambda_as_arg(lambda: {'A': 0})
    tests_passed = 0
    tests_passed += test_print(1, ret is not None, test_name)
    tests_passed += test_print(2, ret['A'] == 0, test_name)
    if tests_passed == 2:
        print("Congrats! All tests for lambda_as_arg passed.")
    else:
        print("Sorry...")


def test_first(run=0):
    if run == 0:
        return
    pass
# endregion
