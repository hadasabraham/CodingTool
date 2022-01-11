import argparse
import sys
from encoder import *
from decoder import *


# Straight-forward check that there are no two identical windows of length k in the sequence, for testing purposes
def validate_no_identical_windows(w, k):
    seen_windows = set()
    for i in range(len(w) - k + 1):
        hash_w = str(w[i:i + k])
        if hash_w in seen_windows:
            return False
        else:
            seen_windows.add(hash_w)
    return True


def run_action(w: List, q, action, redundancy, complexity_mode, verbose_mode, test_mode, comma_mode):
    n = len(w) + redundancy if action == "encode" else len(w)
    orig_w = w.copy()
    log_n = ceil(log(n, q))
    k = 2 * log_n + 2
    if verbose_mode:
        print('n      =', n)
        print('q      =', q)
        print('log_n  =', log_n)
        print('k      =', k)
        print('w      =', w)

    res_word = Encoder(complexity_mode, redundancy, verbose_mode, q).input(w).encode().output() if \
        action == "encode" else Decoder(redundancy, verbose_mode, q).input(w).decode().output()

    if verbose_mode:
        print("output = ", end="")
    if comma_mode:
        print(str(res_word)[1:-1].replace(" ", ""))
    else:
        print("".join(map(str, res_word)))

    if test_mode:
        if action == "encode":
            if validate_no_identical_windows(res_word, k):
                if orig_w == Decoder(redundancy, verbose_mode, q).input(res_word).decode().output():
                    print('TEST SUCCESS')
                    return True
                else:
                    print('TEST FAILED!')
                    print('Decode(Encode(w)) != w')
                    return False
            else:
                print('TEST FAILED!')
                print('Result is not repeat-free')
                return False
        elif action == "decode":
            if orig_w == Encoder(complexity_mode, redundancy, verbose_mode, q).input(res_word).encode().output():
                print('TEST SUCCESS')
                return True
            else:
                print('TEST FAILED!')
                print('Encode(Decode(w)) != w')
                return False
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser("./main")
    parser.add_argument("action", help="{encode, decode}")
    parser.add_argument("sequence", nargs="?", help="a q-ary word")
    parser.add_argument("-i", "--input", help="get word from standard input", action="store_true")
    parser.add_argument("-r", "--redundancy", type=int, choices=[1, 2],
                        help="how many redundancy bits to use", default=1)
    parser.add_argument("-q", type=int, help="alphabet's size", default=2)
    parser.add_argument("-c", "--complexity", choices=["time", "space"],
                        help="save time or space complexity", default="time")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-t", "--test", help="test for output correctness", action="store_true")
    args = parser.parse_args()

    if args.sequence is None:
        if args.input:  # get word from standard input
            args.sequence = input()
        else:
            print("You must enter a word either from the command line or via standard input", file=sys.stderr)
            exit(1)

    if args.q != 2:
        if "," not in args.sequence:
            print(args.q)
            print("You must use ',' as a delimiter when using q != 2 flag", file=sys.stderr)
            exit(1)

    is_comma = False
    if "," in args.sequence:
        is_comma = True
        args.sequence = args.sequence.replace(" ", "").split(",")
    args.sequence = [int(x) for x in list(args.sequence)]

    run_action(args.sequence, args.q, args.action, args.redundancy, args.complexity, args.verbose, args.test, is_comma)

# region Anecdotes

# Before inlining 'identical', profiling shows:
# When n=256, number_of_tests=512, the method 'identical' is called 142M times (~ 2^27), and the program takes 109sec.
# So for one test, on average, it is called 2^(27-9)=2^18 times. Since n=2^8, we expected a lot more times...
# After inlining 'identical', profiling shows:
# Now it takes 78sec (diff=31sec). This means that one test on average takes around 150msec.
# According to Competitive Programming, 100M operations happen in 1 sec, so here, we have 15M operations.
# Since n=2^8, we expected 2^(8*3+2*2)=2^28 which is roughly 256M operations...

# endregion
