from ._errors import LeftRotateError, RightRotateError
from ._rbtree_node import RBTreeNode, RBTreeColor


class RBTree:
    def __init__(self):
        self._len = 0
        self._root = RBTreeNode()

    def __getitem__(self, key):
        node = self._get_node(key)
        if not node:
            raise KeyError(key)
        return node.value

    def __setitem__(self, key, value) -> None:
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
        elif new_node.key > leaf.key:
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
        # TODO: fix this
        node_to_delete = self._get_node(key, raise_error=True)
        y = node_to_delete
        y_original_color = y.color
        if not node_to_delete.left:
            x = node_to_delete.right
            self.__rb_transplant(node_to_delete, node_to_delete.right)
        elif (node_to_delete.right == self.TNULL):
            x = node_to_delete.left
            self.__rb_transplant(node_to_delete, node_to_delete.left)
        else:
            y = self.minimum(node_to_delete.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node_to_delete:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = node_to_delete.right
                y.right.parent = y

            self.__rb_transplant(node_to_delete, y)
            y.left = node_to_delete.left
            y.left.parent = y
            y.color = node_to_delete.color
        if y_original_color == 0:
            self._fix_delete(x)

    def __len__(self):
        return self._len

    def __str__(self):
        string = f'{self.__class__.__name__}('
        for k, v in self.items():
            string += f'{k}: {repr(v)},'
        string = string[:-1]
        string += ')'
        return string

    def __iter__(self):
        pass

    def __bool__(self):
        return len(self) != 0

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def items(self):
        for k in self.keys():
            yield k, self[k]

    def insert(self, key, value):
        self[key] = value

    def remove(self, key):
        del self[key]

    def find(self, key):
        return self[key]

    def clear(self):
        pass

    def keys(self):
        return tuple(node.key for node in self._traverse_inorder(self._root))

    def values(self):
        pass

    def print(self):
        print(self)

    def print_tree(self):
        self._print_tree(self._root, '', right=False, root=True)

    def _fix_insert(self, new_node):
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

    def _fix_delete(self, x):
        # TODO: rewrite this
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self._left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self._right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self._right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.left.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self._left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = 0

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

    def _print_tree(self, node, indent, right, root=False):
        if node:
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
            line += f'{repr(node.key)}:{repr(node.value)} ({node.color.name})'
            print(line)

            self._print_tree(node.left, indent, False)
            self._print_tree(node.right, indent, True)

    def _get_node(self, key, raise_error=False):
        current = self._root
        while current:
            if key > current.key:
                current = current.right
            elif key < current.key:
                current = current.left
            else:
                return current
        if raise_error:
            raise KeyError(key)
        return None

    def _get_leaf(self, key):
        leaf = None
        current = self._root
        while current:
            leaf = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return None
        return leaf

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
