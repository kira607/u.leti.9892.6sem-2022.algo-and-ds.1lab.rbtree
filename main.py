from rbtree import RBTree, RBTreeNode


# Implementing Red-Black Tree in Python


import sys


def run_test(sure):
    if not sure: return
    d = {'1': 2, 3: '4', (5,): [6, '7']}
    print(d)
    # print(d[8])
    exit(0)


def get_tree():
    t = RBTree()
    if not t:
        for i in range(10):
            t.insert(i, str(hash(i)))
    return t


def main():
    run_test(False)
    t = get_tree()
    print(t)
    print(len(t))
    print(tuple(t.keys()))
    t[0] = 100
    print(t)
    t.print_tree()


if __name__ == '__main__':
    main()

