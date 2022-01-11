# AVL Rank Tree:
# Skeleton source: https://gist.github.com/Jekton/d161ccf57bdcc9da5ee134c191f81af7
# Further added methods and all the delta-functionality, independently

from typing import Optional, Tuple, NamedTuple, List


# # Wrapper class for AvlRankTree
# # for consecutive double-edged integers with values
# class IndexMap(object):
#     def __init__(self, first: int):
#         self._avl = AvlRankTree()
#         self._min = first
#         self._max = first
#
#     def prepend(self, value_list: list):
#         for v in reversed(value_list):
#             self._min -= 1
#             self._avl.insert(self._min, v)
#
#     def append(self, value_list: list):
#         for v in value_list:
#             self._max += 1
#             self._avl.insert(self._max, v)
#
#     def __getitem__(self, item):
#         return self._avl[item]
#
#     def delta_add(self, i, j, delta):
#         return self._avl.delta_add(i, j, delta)
#
#     def remove_range(self, i, j):
#         # TODO
#         raise NotImplementedError()


class FindResult(NamedTuple):
    exists: bool
    key:    int
    value:  object
    rank:   int
    deltas: int


class AvlRankTree:
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.left: Optional[AvlRankTree.Node] = None
            self.right: Optional[AvlRankTree.Node] = None

            # Avl-specific
            self.height = 0

            # Extra data
            self.value:                Optional = value
            self.size:                      int = 1  # Used for rank
            self.deltas:                    int = 0
            self.right_deltas:              int = 0
            self.left_most:    AvlRankTree.Node = self
            self.right_most:   AvlRankTree.Node = self

        @staticmethod
        def safe_size(node):
            return node.size if node is not None else 0

        @staticmethod
        def safe_height(node):
            return node.height if node is not None else 0

        @staticmethod
        def safe_right_deltas(node):
            return node.right_deltas if node is not None else 0

    def __init__(self):
        # Initially empty range index.
        self.root = None

    def __len__(self):
        return self.root.size if self.root else 0

    def insert(self, key, value):
        # Inserts a key in the range index.
        if key is None:
            raise ValueError('Index must not be None')

        # Insertion to beginning or end of tree is O(1)
        if self.root and value <= self.root.left_most.key:
            self.root.left_most = AvlRankTree._insert(self.root.left_most, key, value)
        elif self.root and value >= self.root.right_most.key:
            self.root.right_most = AvlRankTree._insert(self.root.right_most, key, value)
        else:
            self.root = AvlRankTree._insert(self.root, key, value)

    @staticmethod
    def _insert(root, key, value):
        if root is None:
            return AvlRankTree.Node(key, value)
        if root.key < key:
            root.right = AvlRankTree._insert(root.right, key, value)
        else:
            root.left = AvlRankTree._insert(root.left, key, value)
        return AvlRankTree._balance(root)

    @staticmethod
    def _update_height(root):
        root.height = max(AvlRankTree.Node.safe_height(root.left), AvlRankTree.Node.safe_height(root.right)) + 1

    @staticmethod
    def _update_size(root):
        root.size = AvlRankTree.Node.safe_size(root.left) + AvlRankTree.Node.safe_size(root.right) + 1

    @staticmethod
    def _update_deltas_rr(root: Node, right: Node):
        orig_deltas = root.deltas
        root.deltas += right.deltas + right.right_deltas
        right.right_deltas -= orig_deltas
        right.deltas -= orig_deltas

    @staticmethod
    def _update_deltas_lr(root: Node, left: Node):
        root.right_deltas += left.right_deltas
        root.deltas += left.right_deltas

    @staticmethod
    def _update_left_most(root):
        root.left_most = root.left.left_most if root.left else root

    @staticmethod
    def _update_right_most(root):
        root.right_most = root.right.right_most if root.right else root

    @staticmethod
    def _balance(root):
        left_height = AvlRankTree.Node.safe_height(root.left)
        right_height = AvlRankTree.Node.safe_height(root.right)
        if left_height >= right_height + 2:
            if AvlRankTree.Node.safe_height(root.left.left) > AvlRankTree.Node.safe_height(root.left.right):
                root = AvlRankTree._right_rotate(root)
            else:
                root.left = AvlRankTree._left_rotate(root.left)
                root = AvlRankTree._right_rotate(root)
        elif right_height >= left_height + 2:
            if AvlRankTree.Node.safe_height(root.right.right) > AvlRankTree.Node.safe_height(root.right.left):
                root = AvlRankTree._left_rotate(root)
            else:
                root.right = AvlRankTree._right_rotate(root.right)
                root = AvlRankTree._left_rotate(root)
        else:
            AvlRankTree._local_update(root)
        return root

    @staticmethod
    def _local_update(node):
        for update in [AvlRankTree._update_height,
                       AvlRankTree._update_size,
                       AvlRankTree._update_left_most,
                       AvlRankTree._update_right_most]:
            update(node)

    @staticmethod
    def _left_rotate(root):
        right = root.right
        root.right = right.left
        right.left = root
        AvlRankTree._local_update(root)
        AvlRankTree._local_update(right)
        AvlRankTree._update_deltas_lr(right, root)
        return right

    @staticmethod
    def _right_rotate(root):
        left = root.left
        root.left = left.right
        left.right = root
        AvlRankTree._local_update(root)
        AvlRankTree._local_update(left)
        AvlRankTree._update_deltas_rr(left, root)
        return left

    def remove(self, key):
        # Removes a key from the range index.
        self.root = AvlRankTree._remove(self.root, key)

    @staticmethod
    def _remove(root, key):
        if root is None:
            return None

        if root.key < key:
            root.right = AvlRankTree._remove(root.right, key)
        elif root.key > key:
            root.left = AvlRankTree._remove(root.left, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            else:
                right_most_of_left = root.left.right_most
                root.left = AvlRankTree._remove(root.left, right_most_of_left)
                root.key = right_most_of_left
        return AvlRankTree._balance(root)

    def update(self, key, new_value):
        AvlRankTree._update(self.root, key, new_value)

    @staticmethod
    def _update(root, key, new_value):
        if root is None:
            return
        if root.key < key:
            AvlRankTree._update(root.right, key, new_value)
        elif root.key > key:
            AvlRankTree._update(root.left, key, new_value)
        else:
            root.value = new_value

    # @staticmethod
    # def _right_most(root):
    #     while root.right is not None:
    #         root = root.right
    #     return root.key

    def list(self, first_key, last_key, inorder=True):
        # List of values for the keys that fall within [first_key, last_key].
        lca = self._lca(first_key, last_key)
        result = []
        _deltas = []
        _right_deltas = []
        if inorder:
            AvlRankTree._node_list_inorder(lca, first_key, last_key, result, _deltas, _right_deltas)
        else:
            AvlRankTree._node_list_preorder(lca, first_key, last_key, result, _deltas, _right_deltas)
        return result, _deltas, _right_deltas

    @staticmethod
    def _node_list_preorder(node, lo, hi, result, _deltas, _right_deltas):
        if node is None:
            return
        if lo <= node.key <= hi:
            result.append(node.key)
            _deltas.append(node.deltas)
            _right_deltas.append(node.right_deltas)
        if node.key >= lo:
            AvlRankTree._node_list_preorder(node.left, lo, hi, result, _deltas, _right_deltas)
        if node.key <= hi:
            AvlRankTree._node_list_preorder(node.right, lo, hi, result, _deltas, _right_deltas)

    @staticmethod
    def _node_list_inorder(node, lo, hi, result, _deltas, _right_deltas):
        if node is None:
            return
        if node.key >= lo:
            AvlRankTree._node_list_inorder(node.left, lo, hi, result, _deltas, _right_deltas)
        if lo <= node.key <= hi:
            result.append(node.key)
            _deltas.append(node.deltas)
            _right_deltas.append(node.right_deltas)
        if node.key <= hi:
            AvlRankTree._node_list_inorder(node.right, lo, hi, result, _deltas, _right_deltas)

    def _lca(self, lo, hi):
        node = self.root
        while node is not None and not (lo <= node.key <= hi):
            node = node.left if lo < node.key else node.right
        return node

    def count(self, first_key, last_key):
        # Number of keys that fall within [first_key, last_key].
        first_exists, _, _, first_rank, _ = self._rank(first_key)
        _, _, _, last_rank, _ = self._rank(last_key)
        return last_rank - first_rank + int(first_exists)

    # # Same as _rank below, written more explicitly
    # def _rank_original(self, key):
    #     rank = 0
    #     deltas = 0
    #     root = self.root
    #     while root is not None and not (root.key == key):
    #         if key < root.key:
    #             root = root.left
    #         else:
    #             rank += AvlRankTree.Node.safe_size(root.left) + 1
    #             deltas += AvlRankTree.Node.safe_right_deltas(root)
    #             root = root.right
    #     if root is not None:
    #         rank += AvlRankTree.Node.safe_size(root.left) + 1
    #         deltas += AvlRankTree.Node.safe_right_deltas(root) + root.deltas
    #         return True, root.key, rank, deltas
    #     return False, None, rank, deltas

    def find(self, key):
        return self._rank(key)

    def _find_path(self, key, before, when_left, when_right, after):
        params = before()
        assert params is not None
        root = self.root
        while root is not None and not (root.key == key):
            if key < root.key:
                params = when_left(params, root)
                root = root.left
            else:
                params = when_right(params, root)
                root = root.right
        return after(params, root)

    # Returns a 5-tuple (FindResult):
    #   exists: bool
    #   key:    int
    #   value:  int if exists else None
    #   rank:   int
    #   deltas: int
    def _rank(self, key) -> Tuple[bool, int, Optional[int], int, int]:
        return self._find_path(
            key=key,
            before=lambda: {'rank': 0, 'deltas': 0},
            when_left=lambda params, root: params,
            when_right=lambda params, root: {'rank': params['rank'] + AvlRankTree.Node.safe_size(root.left) + 1,
                                             'deltas': params['deltas'] + AvlRankTree.Node.safe_right_deltas(root)},
            after=lambda params, root: FindResult(exists=True,
                                                  key=root.key,
                                                  value=root.value,
                                                  rank=params['rank'] + AvlRankTree.Node.safe_size(root.left) + 1,
                                                  deltas=params['deltas'] + root.deltas)
            if root else FindResult(exists=False,
                                    key=key,
                                    value=None,
                                    rank=params['rank'],
                                    deltas=params['deltas'])
        )

    @staticmethod
    def _delta_add_when_left(params, root):
        if not params['right_edge']:
            root.deltas += params['delta']
        root.right_deltas += params['delta']
        return params

    def delta_add(self, i, j, delta):
        self._find_path(
            key=i,
            before=lambda: {'delta': delta, 'right_edge': False},
            when_left=AvlRankTree._delta_add_when_left,
            when_right=lambda params, root: params,
            after=AvlRankTree._delta_add_when_left
        )
        self._find_path(
            key=j,
            before=lambda: {'delta': -delta, 'right_edge': False},
            when_left=AvlRankTree._delta_add_when_left,
            when_right=lambda params, root: params,
            after=lambda params, root: AvlRankTree._delta_add_when_left({'delta': params['delta'],
                                                                         'right_edge': True}, root)
        )

    def __getitem__(self, key):  # -> int
        existent, existent_key, value, _, deltas = self.find(key)
        return value + deltas if value is not None else None

    def get(self, key):
        existent, existent_key, value, _, _ = self.find(key)
        return value

    @classmethod
    def from_sorted(cls, sorted_list: List):
        tree = cls()
        node_list = [None] * len(sorted_list)
        tree.root = AvlRankTree._from_sorted(sorted_list, node_list)
        AvlRankTree._local_update(tree.root)
        return tree, node_list

    @staticmethod
    def _from_sorted(sorted_list: List, node_list: List = None) -> Optional['AvlRankTree.Node']:
        if len(sorted_list) == 0:
            return None

        mid = (len(sorted_list)) // 2
        root = AvlRankTree.Node(mid, sorted_list[mid])

        if node_list:
            node_list[mid] = root

        root.left = AvlRankTree._from_sorted(sorted_list[:mid], node_list)
        root.right = AvlRankTree._from_sorted(sorted_list[mid + 1:], node_list)
        AvlRankTree._local_update(root)
        return root
