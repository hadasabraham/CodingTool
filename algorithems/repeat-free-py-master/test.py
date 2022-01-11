import numpy as np
import contextlib
import io

from main import run_action


def run_tests(number_of_tests, n, digit_distribution, redundancy, complexity, verbose, test_mode, print_output):
    len_source = number_of_tests + n - 1 - redundancy
    q = len(digit_distribution)

    # If some digit has "-1" then it takes the remainder of the distribution
    # Only one digit can use this
    for i in range(q):
        if digit_distribution[i] == -1:
            digit_distribution[i] = round(1 - sum(digit_distribution[:i] + digit_distribution[i + 1:]), 2)
            break

    if sum([d if d < 0 else 0 for d in digit_distribution]) != 0:
        raise Exception("Digit distribution must have non-negative values for all digits, "
                        "with the possibility of one usage of '-1' (meaning 'the rest')")

    if sum(digit_distribution) != 1:
        raise Exception("Sum of digit distribution must be 1. Hint: "
                        "Use '-1' for one of the digits to mean 'the rest'.")

    raw_arr = []
    for i in range(1, q):
        raw_arr += [i] * int(len_source * digit_distribution[i])
    raw_arr += [0] * (len_source - len(raw_arr))
    arr = np.array(raw_arr)
    np.random.shuffle(arr)
    source = list(arr)
    number_of_successes = 0
    for i in range(number_of_tests):
        w = source[i:i + (n - redundancy)]
        if print_output and not verbose:
            print('input  =', "".join([str(x) for x in w]))
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            res = run_action(w, q, 'encode', redundancy, complexity, verbose, test_mode)
        out = f.getvalue()
        if print_output and i & 0b1111111 == 0:  # Print every 128-th output
            print(out)
        number_of_successes += res
    print("With n={}, q={}, r={}, digit_dist={}, c={}, test_mode={}".format(n, q, redundancy, digit_distribution,
                                                                            complexity, test_mode))
    print("Succeeded {} times out of {} ({}%)".format(number_of_successes, number_of_tests,
                                                      100. * number_of_successes / number_of_tests))
    print()


if __name__ == '__main__':
    run_tests(
        number_of_tests=2 ** 8,
        n=2 ** 7,
        digit_distribution=[-1, 0.35, 0.1],
        # q=len(digit_distribution),
        redundancy=2,
        complexity='space',
        verbose=False,
        test_mode=True,
        print_output=True
    )
    run_tests(
        number_of_tests=2 ** 8,
        n=2 ** 7,
        digit_distribution=[-1, 0.35, 0.1, 0.2, 0.3],
        # q=len(digit_distribution),
        redundancy=1,
        complexity='time',
        verbose=False,
        test_mode=True,
        print_output=True
    )
