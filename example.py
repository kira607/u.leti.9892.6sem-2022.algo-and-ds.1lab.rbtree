from rbtree import RBTree


def get_tree():
    t = RBTree()
    for i in range(10):
        t.insert(i, i)
    return t


examples = []


def example(name):
    def decorator(f):
        def wrapper(t):
            print(f'Example {name}:')
            print(f'Original tree: {t}')

            f(t)

            print('Tree:')
            t.print_tree()
        examples.append(wrapper)
        return wrapper
    return decorator


@example('find')
def example_find(t):
    for k in t:
        print(f'{k}: {t.find(k)}')


@example('insert')
def example_insert(t):
    t.insert(1, 'new_value')
    print('Replaced value at key 1 with "new_value":')
    print(t)

    t.insert('new_key', 'another_value')
    print('Inserted value "new_value" with key "new_key":')
    print(t)


@example('remove')
def example_remove(t):
    print('Removed key 7:')
    t.remove(7)
    print(t)


@example('keys and values')
def example_keys_and_values(t):
    print('Keys:')
    print(t.get_keys())

    print('Values:')
    print(t.get_values())


def main():
    t = get_tree()
    for example in examples:
        example(t)
        print()


if __name__ == '__main__':
    main()

