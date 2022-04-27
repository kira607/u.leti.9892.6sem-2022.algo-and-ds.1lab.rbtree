from typing import Any, Hashable, Optional

from ._rbtree_color import RBTreeColor


class RBTreeNode:
    def __init__(
        self,
        key: Optional[Hashable] = None,
        value: Any = None,
        color: RBTreeColor = RBTreeColor.BLACK,
        parent: Optional['RBTreeNode'] = None,
        left: Optional['RBTreeNode'] = None,
        right: Optional['RBTreeNode'] = None,
    ) -> None:
        self.key = key
        self.value = value
        self.parent = parent
        self._color = color
        self.left = left or RBTreeNode(None, parent=self) if key is not None else None
        self.right = right or RBTreeNode(None, parent=self) if key is not None else None

    def __eq__(self, other: 'RBTreeNode'):
        return self.key == other.key

    def __bool__(self):
        return not (self.key is None)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        info = f'{self.color.name} {self.key}:{repr(self.value)}' if bool(self) else 'NULL'
        return f'<{self.__class__.__name__} {info}>'

    def is_left_child(self):
        if not self.parent:
            return False
        return self == self.parent.left

    def is_right_child(self):
        if not self.parent:
            return False
        return self == self.parent.right

    @property
    def gparent(self):
        if self.parent:
            return self.parent.parent
        return None

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: RBTreeColor):
        if not isinstance(color, RBTreeColor):
            raise TypeError('color must be a RBTreeColor instance')
        self._color = color

    def color_black(self):
        self.color = RBTreeColor.BLACK

    def color_red(self):
        self.color = RBTreeColor.RED
