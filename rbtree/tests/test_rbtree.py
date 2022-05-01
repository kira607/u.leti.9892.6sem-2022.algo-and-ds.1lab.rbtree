from math import log
from string import ascii_lowercase

import pytest

from .. import RBTree


_default_data = dict((char, num) for num, char in enumerate(ascii_lowercase, start=1))


def check_tree(tree: RBTree, data: dict) -> None:
    assert sorted(tree.keys()) == sorted(tuple(data.keys()))
    assert sorted(tree.values()) == sorted(tuple(data.values()))
    assert len(tree) == len(data)
    assert tree.height < 2 * log(len(tree) + 1)


@pytest.mark.parametrize(
    'data',
    (
        _default_data.copy(),
        dict((str(i), i) for i in range(100)),
        dict((str(i), i) for i in range(1000)),
    ),
)
def test_init(data):
    t = RBTree(**data)
    check_tree(t, data)


@pytest.mark.parametrize(
    'data, new_key, existing_key, new_value',
    (
        (_default_data.copy(), 'A', 'a', 1000),
        (dict((str(i), i) for i in range(100)), '101', '1', 1000),
        (dict((str(i), i) for i in range(1000)), '9999', '1', 1000),
    ),
)
def test_insert(data, new_key, existing_key, new_value):
    t = RBTree(**data)
    old_len = len(t)
    t[new_key] = new_value
    data[new_key] = new_value
    assert len(t) == old_len + 1
    t[existing_key] = new_value
    data[existing_key] = new_value
    assert len(t) == old_len + 1
    assert t[existing_key] == new_value
    check_tree(t, data)


@pytest.mark.parametrize(
    'data',
    (
        _default_data.copy(),
        dict((str(i), i) for i in range(100)),
        dict((str(i), i) for i in range(1000)),
    ),
)
def test_get(data):
    t = RBTree(**data)
    for k, v in t.items():
        assert t[k] == v
    check_tree(t, data)


def test_get_error():
    t = RBTree(**_default_data)
    with pytest.raises(KeyError):
        t.find('A')


@pytest.mark.parametrize(
    'data, existing_key',
    (
        (_default_data.copy(), 'a'),
        (dict((str(i), i) for i in range(100)), '1'),
        (dict((str(i), i) for i in range(1000)), '1'),
    ),
)
def test_delete(data, existing_key):
    t = RBTree(**data)
    old_len = len(t)
    del t[existing_key]
    del data[existing_key]
    assert len(t) == old_len - 1
    with pytest.raises(KeyError):
        t.find(existing_key)
    check_tree(t, data)


@pytest.mark.parametrize(
    'data, missing_key, error',
    (
            (_default_data.copy(), 'A', KeyError),
            (dict((str(i), i) for i in range(100)), '101', KeyError),
            (dict((str(i), i) for i in range(1000)), '9999', KeyError),
    ),
)
def test_delete_error(data, missing_key, error):
    t = RBTree(**data)
    with pytest.raises(KeyError):
        del t[missing_key]


# @pytest.mark.skip
def test_clear():
    t = RBTree(**_default_data)
    t.clear()
    assert not t
    assert len(t) == 0
