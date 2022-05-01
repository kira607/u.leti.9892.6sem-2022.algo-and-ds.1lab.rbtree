from rbtree import RBTree


def get_tree():
    t = RBTree()
    for i in range(10):
        t.insert(i, i)
    return t


def main():
    t = get_tree()
    t.print_tree()


if __name__ == '__main__':
    main()

