from random import choice


def generate_test():
    file = open('test_file_updated.txt', 'w')
    for i in range(0, 100):
        strand = ''.join(choice('01') for _ in range(100))
        file.write(strand)
        file.write('\n')

generate_test()


