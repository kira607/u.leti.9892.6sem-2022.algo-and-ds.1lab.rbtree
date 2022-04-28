from typing import Any, Hashable, Optional, Union

from ._errors import LeftRotateError, RightRotateError
from ._rbtree_node import RBTreeNode, RBTreeColor


class RBTree:
    def __init__(self):
        self._len = 0
        self._root = RBTreeNode()

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

        self._len += 1

        if not new_node.parent:
            new_node.color_black()
            return
        if not new_node.gparent:
            return

        self._fix_insert(new_node)

    def __delitem__(self, key):
        node_to_delete = self._get_node(key, raise_error=True)
        node_to_delete_2 = node_to_delete
        node_to_delete_original_color = node_to_delete_2.color
        if not node_to_delete.left:
            x = node_to_delete.right
            self._swap(node_to_delete, node_to_delete.right)
        elif not node_to_delete.right:
            x = node_to_delete.left
            self._swap(node_to_delete, node_to_delete.left)
        else:
            node_to_delete_2 = self.get_min(node_to_delete.right)
            node_to_delete_original_color = node_to_delete_2.color
            x = node_to_delete_2.right
            if node_to_delete_2.parent == node_to_delete:
                x.parent = node_to_delete_2
            else:
                self._swap(node_to_delete_2, node_to_delete_2.right)
                node_to_delete_2.right = node_to_delete.right
                node_to_delete_2.right.parent = node_to_delete_2

            self._swap(node_to_delete, node_to_delete_2)
            node_to_delete_2.left = node_to_delete.left
            node_to_delete_2.left.parent = node_to_delete_2
            node_to_delete_2.color = node_to_delete.color
        if node_to_delete_original_color == RBTreeColor.BLACK:
            self._fix_delete(x)
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

    def get(self, key: Hashable, default: Any = None) -> Union[RBTreeNode, Any]:
        try:
            return self[key]
        except KeyError:
            return default

    def items(self):
        for k in self.keys():
            yield k, self[k]

    def insert(self, key: Hashable, value: Any):
        self[key] = value

    def remove(self, key: Hashable):
        del self[key]

    def find(self, key: Hashable):
        return self[key]

    def clear(self):
        pass

    def keys(self):
        return tuple(node.key for node in self._traverse_inorder(self._root))

    def values(self):
        return tuple(node.value for node in self._traverse_inorder(self._root))

    def print(self):
        print(self)

    def print_tree(self, hash_key: bool = False):
        self._print_tree(self._root, '', right=False, root=True, hash_key=hash_key)

    def get_max(self, node: RBTreeNode = None) -> RBTreeNode:
        node = node or self._root
        while node.right:
            node = node.right
        return node

    def get_min(self, node: RBTreeNode = None) -> RBTreeNode:
        node = node or self._root
        while node.left:
            node = node.left
        return node

    def _fix_insert(self, new_node: RBTreeNode):
        current_node = new_node
        while current_node.parent.color == RBTreeColor.RED:
            if current_node.parent == current_node.gparent.left:
                if current_node.gparent.right.color == RBTreeColor.RED:
                    current_node.gparent.right.color_black()
                    current_node.parent.color_black()
                    current_node.gparent.color_red()
                    current_node = current_node.gparent
                else:
                    if current_node == current_node.parent.right:
                        current_node = current_node.parent
                        self._left_rotate(current_node)
                    current_node.parent.color_black()
                    current_node.gparent.color_red()
                    self._right_rotate(current_node.gparent)
            elif current_node.parent == current_node.gparent.right:
                if current_node.gparent.left.color == RBTreeColor.RED:
                    current_node.gparent.left.color_black()
                    current_node.parent.color_black()
                    current_node.gparent.color_red()
                    current_node = current_node.gparent
                else:
                    if current_node == current_node.parent.left:
                        current_node = current_node.parent
                        self._right_rotate(current_node)
                    current_node.parent.color_black()
                    current_node.gparent.color_red()
                    self._left_rotate(current_node.gparent)
            if current_node == self._root:
                break
        self._root.color_black()

    def _fix_delete(self, node: RBTreeNode):
        # TODO: rewrite this
        while node != self._root and node.color == RBTreeColor.BLACK:
            if node.is_left_child():
                s = node.parent.right
                if s.color == RBTreeColor.RED:
                    s.color_black()
                    node.parent.color_red()
                    self._left_rotate(node.parent)
                    s = node.parent.right
                if s.left.color == RBTreeColor.BLACK and s.right.color == RBTreeColor.BLACK:
                    s.color_red()
                    node = node.parent
                else:
                    if s.right.color == RBTreeColor.BLACK:
                        s.left.color_black()
                        s.color_red()
                        self._right_rotate(s)
                        s = node.parent.right
                    s.color = node.parent.color
                    node.parent.color_black()
                    s.right.color_black()
                    self._left_rotate(node.parent)
                    node = self._root
            else:
                s = node.parent.left
                if s.color == RBTreeColor.RED:
                    s.color_black()
                    node.parent.color_red()
                    self._right_rotate(node.parent)
                    s = node.parent.left
                if s.right.color == RBTreeColor.BLACK and s.left.color == RBTreeColor.BLACK:
                    s.color_red
                    node = node.parent
                else:
                    if s.left.color == RBTreeColor.BLACK:
                        s.right.color_black()
                        s.color_red()
                        self._left_rotate(s)
                        s = node.parent.left
                    s.color = node.parent.color
                    node.parent.color_black()
                    s.left.color_black()
                    self._right_rotate(node.parent)
                    node = self._root
        node.color_black()

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

    def _left_rotate(self, node):
        right_node = node.right
        node.right = right_node.left

        if not right_node:
            raise LeftRotateError('Cannot left rotate a node without a right child')

        if right_node.left:
            right_node.left.parent = node

        right_node.parent = node.parent
        if not node.parent:
            self._root = right_node
        elif node == node.parent.left:
            node.parent.left = right_node
        elif node == node.parent.right:
            node.parent.right = right_node

        right_node.left = node
        node.parent = right_node

    def _right_rotate(self, node):
        left_node = node.left
        node.left = left_node.right

        if not left_node:
            raise RightRotateError('Cannot right rotate a node without a left child')

        if left_node.right:
            left_node.right.parent = node

        left_node.parent = node.parent
        if not node.parent:
            self._root = left_node
        elif node == node.parent.right:
            node.parent.right = left_node
        elif node == node.parent.left:
            node.parent.left = left_node

        left_node.right = node
        node.parent = left_node

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

    def _swap(self, node_a: RBTreeNode, node_b: RBTreeNode) -> None:
        if not node_a.parent:
            self.root = node_b
        elif node_a.is_left_child():
            node_a.parent.left = node_b
        else:
            node_a.parent.right = node_b
        node_b.parent = node_a.parent
