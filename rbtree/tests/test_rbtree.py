from .. import RBTree


def test_init():
    t = RBTree(a=1, b=2, c=3)
    assert sorted(t.keys()) == sorted(('a', 'b', 'c'))
    assert sorted(t.values()) == sorted((1, 2, 3))
    assert len(t) == 3
