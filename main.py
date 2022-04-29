from operator import lt
from rbtree import RBTree, RBTreeNode


def get_tree():
    t = RBTree()
    if not t:
        for i in range(10):
            t.insert(i, str(hash(i)))
    t['123'] = 456
    return t


def main():
    t = get_tree()
    print(t)
    print(len(t))
    print(t.keys())
    t[0] = 100
    t[1] = 10
    print(t)
    t.print_tree(True)
    del t[5]
    t.print_tree()
    print(dict(t.items()))
    print(len(t))
    print('height:', t.get_height())
    t = RBTree()
    t.remove(1)


if __name__ == '__main__':
    main()

