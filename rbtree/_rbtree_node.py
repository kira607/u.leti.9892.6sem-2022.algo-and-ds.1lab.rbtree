from typing import Any, Hashable, Optional, Union

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
        hash(key)
        self.key = key
        self.value = value
        self.parent = parent
        self._color = color
        self.left = left or RBTreeNode(None, parent=self) if key is not None else None
        self.right = right or RBTreeNode(None, parent=self) if key is not None else None

    def __eq__(self, other: Union['RBTreeNode', Hashable]):
        return hash(self.key) == hash(other)

    def __gt__(self, other: Union['RBTreeNode', Hashable]):
        return hash(self.key) > hash(other)

    def __lt__(self, other: Union['RBTreeNode', Hashable]):
        return hash(self.key) < hash(other)

    def __le__(self, other: Union['RBTreeNode', Hashable]):
        return (self < other) or (self == other)

    def __ge__(self, other: Union['RBTreeNode', Hashable]):
        return (self > other) or (self == other)

    def __hash__(self):
        return hash(self.key)

    def __bool__(self):
        return not (self.key is None)

    def __str__(self):
        if self:
            return f'{repr(self.key)}:{repr(self.value)}'
        return 'NULL'

    def __repr__(self):
        return f'<{self.__class__.__name__} {str(self)} {self.color.name}>'

    @property
    def bro(self) -> Optional['RBTreeNode']:
        '''Get node brother.'''
        if not self.parent:
            return None 
        if self.is_left():
            return self.parent.right
        if self.is_right():
            return self.parent.left

    @property
    def gparent(self) -> Optional['RBTreeNode']:
        '''Get node grandparent.'''
        if self.parent:
            return self.parent.parent
        return None

    @property
    def uncle(self) -> Optional['RBTreeNode']:
        '''Get node uncle.'''
        if not self.gparent:
            return None
        if self.parent.is_left():
            return self.gparent.right
        elif self.parent.is_right():
            return self.gparent.left
        return None

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: RBTreeColor):
        if not isinstance(color, RBTreeColor):
            raise TypeError('color must be a RBTreeColor instance')
        self._color = color

    def is_red(self):
        return self.color == RBTreeColor.RED

    def is_black(self):
        return self.color == RBTreeColor.BLACK

    def color_black(self):
        self.color = RBTreeColor.BLACK

    def color_red(self):
        self.color = RBTreeColor.RED

    def is_left(self):
        if not self.parent:
            return False
        return self == self.parent.left

    def is_right(self):
        if not self.parent:
            return False
        return self == self.parent.right

    def get_graphviz(self):
        color = f'[fontcolor="{"red" if self.is_red() else "black"}"]'
        s = f'{{"{str(self)}"{color}}}'
        return (
            f'{s} -- "{str(self.left)}"\n'
            f'{s} -- "{str(self.right)}"\n'
        )
