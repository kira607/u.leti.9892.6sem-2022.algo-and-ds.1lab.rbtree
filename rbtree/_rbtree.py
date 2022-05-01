import graphviz
from typing import Any, Hashable, Optional, Union

from ._rbtree_node import RBTreeNode, RBTreeColor


class RBTree:
    def __init__(self, **kwargs: Any) -> None:
        self._len = 0
        self._root = RBTreeNode()
        for k, v in kwargs.items():
            self[k] = v

    def __getitem__(self, key: Hashable):
        node = self._get_node(key, True)
        return node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        '''insert a new node.'''
        node = self._get_node(key)

        if node:
            node.value = value
            return

        new_node = RBTreeNode(key, value, RBTreeColor.RED)
        leaf = self._get_leaf(key)
        new_node.parent = leaf
        if not leaf:
            self._root = new_node
        elif new_node > leaf:
            leaf.right = new_node
        else:
            leaf.left = new_node

        self._fix_insert(new_node)
        self._len += 1

    def __delitem__(self, key: Hashable):
        node_to_delete = self._get_node(key, raise_error=True)
        print(node_to_delete)

        if node_to_delete.left and node_to_delete.right:
            fix_node = (
                self.get_min_node(node_to_delete.right)
                or self.get_max_node(node_to_delete.left)
            )
            self._swap_kv(node_to_delete, fix_node)
            node_to_delete = fix_node

        self._delete(node_to_delete)
        self._len -= 1

    def __len__(self):
        return self._len

    def __str__(self):
        string = f'{self.__class__.__name__}({{'
        for k, v in self.items():
            string += f'{repr(k)}: {repr(v)}, '
        string = string[:-2]
        string += '})'
        return string

    def __iter__(self):
        return iter(self.keys())

    def __bool__(self):
        return len(self) != 0

    @property
    def height(self):
        return self.get_height()

    def get(self, key: Hashable, default: Any = None) -> Union[RBTreeNode, Any]:
        try:
            return self[key]
        except KeyError:
            return default

    def items(self):
        for k in self.keys():
            yield k, self[k]

    def keys(self):
        return tuple(node.key for node in self._traverse_inorder(self._root))

    def values(self):
        return tuple(node.value for node in self._traverse_inorder(self._root))

    # Task methods (start)

    def insert(self, key: Hashable, value: Any):
        self[key] = value

    def remove(self, key: Hashable):
        del self[key]

    def find(self, key: Hashable):
        return self[key]

    def clear(self):
        while self:
            del self[self._root.key]

    def get_keys(self):
        return self.keys()

    def get_values(self):
        return self.values()

    def print(self):
        print(self)

    # Task methods (end)

    def print_tree(self, hash_key: bool = False):
        self._print_tree(self._root, '', right=False, root=True, hash_key=hash_key)

    def get_max_node(self, node: RBTreeNode = None) -> RBTreeNode:
        node = node or self._root
        while node.right:
            node = node.right
        return node

    def get_min_node(self, node: RBTreeNode = None) -> RBTreeNode:
        node = node or self._root
        while node.left:
            node = node.left
        return node

    def get_height(self, node: RBTreeNode = None, h: int = 0) -> int:
        if not self._root:
            return 0
        if not isinstance(node, RBTreeNode):
            node = self._root

        if not node:
            return h
        else:
            h += 1

        return max(self.get_height(node.left, h), self.get_height(node.right, h))

    def get_graphviz(self) -> graphviz.Source:
        graphviz_string = 'graph {\n'
        for k in self.keys():
            node = self._get_node(k, True)
            graphviz_string += node.get_graphviz()
        graphviz_string += '}'
        return graphviz.Source(graphviz_string)

    def _fix_insert(self, node: RBTreeNode):
        self._insert_case_1(node)

    def _insert_case_1(self, node: RBTreeNode) -> None:
        if not node.parent:
            node.color_black()
        else:
            self._insert_case_2(node)

    def _insert_case_2(self, node: RBTreeNode) -> None:
        if node.parent.is_black():
            return
        else:
            self._insert_case_3(node)

    def _insert_case_3(self, node: RBTreeNode) -> None:
        u = node.uncle
        if u and u.is_red():
            node.parent.color_black()
            u.color_black()
            g = node.gparent
            g.color_red()
            self._insert_case_1(g)
        else:
            self._insert_case_4(node)

    def _insert_case_4(self, node: RBTreeNode) -> None:
        if node.is_right_child() and node.parent.is_left_child():
            self._left_rotate(node.parent)
            node = node.left
        elif node.is_left_child() and node.parent.is_right_child():
            self._right_rotate(node.parent)
            node = node.right
        self._insert_case_5(node)

    def _insert_case_5(self, node: RBTreeNode) -> None:
        g = node.gparent
        node.parent.color_black()
        g.color_red()
        if node.is_left_child() and node.parent.is_left_child():
            self._right_rotate(g)
        else:
            self._left_rotate(g)

    def _replace(self, node: RBTreeNode, child: RBTreeNode) -> None:
        if not node.parent:
            self.root = child
        elif node.is_left_child():
            node.parent.left = child
        else:
            node.parent.right = child
        child.parent = node.parent

    def _delete(self, node: RBTreeNode) -> None:
        if node.left and node.right:
            raise RuntimeError('Attempting to delete a node with both children existing (expected <= 1)')

        child = node.left if node.left else node.right
        print(f'replacing {node} with {child}')
        self._replace(node, child)
        if node.is_black():
            if child.is_red():
                child.color_black()
            else:
                self._fix_delete(child)
        del node
  
    def _fix_delete(self, node: RBTreeNode):
        self._del_case_1(node)

    def _del_case_1(self, node: RBTreeNode) -> None:
        if not node.parent:
            return
        self._del_case_2(node)

    def _del_case_2(self, node: RBTreeNode) -> None:
        bro = node.bro
        if bro.is_red():
            node.parent.color_red()
            bro.color_black()
            if node.is_left_child():
                self._left_rotate(node.parent)
            else:
                self._right_rotate(node.parent)
        self._del_case_3(node)

    def _del_case_3(self, node: RBTreeNode) -> None:
        bro = node.bro
        if (
            node.parent.is_black()
            and bro.is_black()
            and bro.left.is_black()
            and bro.right.is_black()
        ):
            bro.color_red()
            self._del_case_1(node.parent)
        else:
            self._del_case_4(node)

    def _del_case_4(self, node: RBTreeNode) -> None:
        bro = node.bro
        if (
            node.parent.is_red()
            and bro.is_black()
            and bro.left.is_black()
            and bro.right.is_black()
        ):
            bro.color_red()
            node.parent.color_black()
        else:
            self._del_case_5(node)

    def _del_case_5(self, node: RBTreeNode) -> None:
        bro = node.bro

        if bro.is_black():
            if (
                node.is_left_child()
                and bro.right.is_black()
                and bro.left.is_red()
            ):
                bro.color_red()
                bro.left.color_black()
                self._right_rotate(bro)
            elif (
                node.is_right_child()
                and bro.right.is_red()
                and bro.left.is_black()
            ):
                bro.color_red()
                bro.right.color_black()
                self._left_rotate(bro)
        self._del_case_6(node)

    def _del_case_6(self, node: RBTreeNode) -> None:
        bro = node.bro

        bro.color = node.parent.color
        node.parent.color_black()

        if node.is_left_child():
            bro.right.color_black()
            self._left_rotate(node.parent)
        else:
            bro.left.color_black()
            self._right_rotate(node.parent)

    def _traverse_preorder(self, node):
        if node:
            yield node
            yield from self._traverse_preorder(node.left)
            yield from self._traverse_preorder(node.right)

    def _traverse_inorder(self, node):
        if node:
            yield from self._traverse_inorder(node.left)
            yield node
            yield from self._traverse_inorder(node.right)

    def _traverse_postorder(self, node):
        if node:
            yield from self._traverse_postorder(node.left)
            yield from self._traverse_postorder(node.right)
            yield node

    def _left_rotate(self, x: RBTreeNode):
        y = x.right
        x.right = y.left

        if y.left:
            y.left.parent = x

        y.parent = x.parent

        if not x.parent:
            self._root = y
        elif x.is_left_child():
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, x: RBTreeNode):
        y = x.left
        x.left = y.right

        if y.right:
            y.right.parent = x

        y.parent = x.parent

        if not x.parent:
            self._root = y
        elif x.is_left_child():
            x.parent.left = y
        else:
            x.parent.right = y

        y.right = x
        x.parent = y

    def _print_tree(
        self, 
        node: RBTreeNode, 
        indent: str, 
        right: bool, 
        root: bool = False, 
        hash_key: bool = False,
    ) -> None:
        if not node:
            return
        
        line = indent
        if root:
            line += '--> '
            indent += '    '
        elif right:
            line += '└─R '
            indent += '    '
        else:
            line += '├─L '
            indent += '│   '
        
        k = repr(hash(node.key)) if hash_key else repr(node.key)
        line += f'{k}:{repr(node.value)} ({node.color.name})'
        print(line)

        self._print_tree(node.left, indent, False, hash_key=hash_key)
        self._print_tree(node.right, indent, True, hash_key=hash_key)

    def _get_node(self, key: Hashable, raise_error: bool = False) -> Optional[RBTreeNode]:
        '''
        Get a node in a tree.
        
        :param key: The key of the node.
        :param raise_error: If true, raise a KeyError if node with given key was not found.
        :raises KeyError: If node with given key was not found.
        :return: A node in the tree if exists, else None.
        '''
        current = self._root
        while current:
            if key > current:
                current = current.right
            elif key < current:
                current = current.left
            else:
                return current
        if raise_error:
            raise KeyError(key)
        return None

    def _get_leaf(self, key: Hashable):
        leaf = None
        current = self._root
        while current:
            leaf = current
            if key > current:
                current = current.right
            elif key < current:
                current = current.left
            else:
                return None
        return leaf

    def _swap_kv(self, a: RBTreeNode, b: RBTreeNode) -> None:
        k, v = a.key, a.value
        a.key, a.value = b.key, b.value
        b.key, b.value = k, v
