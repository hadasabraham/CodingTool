# Antonio: Currently unused.

"""
AVL property - Binary Search Tree with a balance property
Idea: keep tree shallow so we don't get the O(n) worst case for search, insert, delete like in a BST
Forces max height of tree to be bounded by log n (AVL tree height is at most roughly 1.44 log(N + 2) − 1.328)
balance <= 1
    where balance is defined as |height_LeftSubtree - height_RightSubtree|
    update heights recursively starting at leaves
need to store:
    - heights
    - balance
To maintain AVL property, after changing tree structure (insert, delete)
    1. update heights
    2. update balances
    3. rebalance (via rotations)
___________
|Rotations|
-----------
    balance is calculated by left_height - right_height
    if the balance is > 1, then the left side is heavier (violates the AVL property)
    if balance < -1, then the right side is heavier (or larger)
    if positive we need to start with a left rotation
    if negative we need to start with a right rotation
    assuming that the node that violates the balance condition is *, thus * needs to be rebalanced
        - a node can only have at most 2 children
        - height imbalance requires *'s subtrees differ by 2
                           *
                        /     \
                  lChild       rChild
                 /    \        /      \
            lSubT    rSubT   lSubT   rSubT
             o         i       i       o
        so violation can occur in 4 places:
            1. insertion into left subtree of left child of *   | insertion occurs 'outside', left left
            2. insertion into right subtree of left child of *  | insertion occurs 'inside', right left
            3. insertion into left subtree of right child of *  | insertion occurs 'inside', left right
            4. insertion into right subtree of right child of * | insertion occurs 'outside', right right
        o = 'outside' can be fixed with a single rotation
        i = 'inside' needs more complex double rotation
    treat caps as twice height of lower case
    Single Rotations
                    k2                                      k1              drag z down, make k1 new root
                  /   \      left left case                 /  \             attach y to k2
                k1    z     => rotate right =>             X    k2
               /  \                                            / \
              X   y                                           y   z
            h b     k2 violates balance property           h b
        k2|4 2                                          k2|3 0
        k1|3 1                                          k1|2 0
        z |1 0                                          z |1 0
        X |2 0                                          X |2 0
        y |1 0                                          y |1 0
            A                               B
           /       left left case so       / \
          B     => right rotation =>       C   A      this keeps BST property and keeps tree shallower allowing O(log n ) operations
         /
        C
    Double Rotations
                k3                                                   k3                     k2
        l     /  \                                                  / \                     /  \
            k1    D   => left right case                     =>   k2  D      =>          k1    k3
           /  \  r       so rotate left to get rid of the r      /  \                   / \   /  \
          A    k2           then rotate right                  k1   C                  A  B   C  D
              /  \                                           /  |
            B     C                                         A   B
                k3 is violating the AVL property
        h b
    k3|3 2
    k1|2 1
    k2|1 0
    A |0 0
    D |0 0
    B |0 0
    C |0 0
- insert is same as BST with updating height after and rebalanced to enforce AVL property
- look up, get min, get max is same as BST
All operations O(log n)
O(n) space

Description source: https://github.com/darvid7/technical-interviews
"""

# Source: https://github.com/bfaure/Python3_Data_Structures


class AvlTree:
    class TreeNode:
        def __init__(self, value=None):
            self.value = value
            self.left_child = None
            self.right_child = None
            self.parent = None  # pointer to parent node in tree
            self.height = 1  # height of node in tree (max dist. to leaf)

        def get_child(self, i):
            if i == 0:
                return self.left_child
            if i == 1:
                return self.right_child
            return None

        def set_child(self, i, node):
            if i == 0:
                self.left_child = node
            elif i == 1:
                self.right_child = node

    def __init__(self):
        self.root = None

    def __repr__(self):
        if self.root is None:
            return ''
        content = '\n'  # to hold final string
        cur_nodes = [self.root]  # all nodes at current level
        cur_height = self.root.height  # height of nodes at current level
        sep = ' ' * (2 ** (cur_height - 1))  # variable sized separator between elements
        while True:
            cur_height += -1  # decrement current height
            if len(cur_nodes) == 0:
                break
            cur_row = ' '
            next_row = ''
            next_nodes = []

            if all(n is None for n in cur_nodes):
                break

            for n in cur_nodes:

                if n is None:
                    cur_row += '   ' + sep
                    next_row += '   ' + sep
                    next_nodes.extend([None, None])
                    continue

                if n.value is None:
                    buf = ' ' * int((5 - len(str(n.value))) / 2)
                    cur_row += '%s%s%s' % (buf, str(n.value), buf) + sep
                else:
                    cur_row += ' ' * 5 + sep

                if n.left_child is not None:
                    next_nodes.append(n.left_child)
                    next_row += ' /' + sep
                else:
                    next_row += '  ' + sep
                    next_nodes.append(None)

                if n.right_child is None:
                    next_nodes.append(n.right_child)
                    next_row += '\\ ' + sep
                else:
                    next_row += '  ' + sep
                    next_nodes.append(None)

            content += (cur_height * '   ' + cur_row + '\n' + cur_height * '   ' + next_row + '\n')
            cur_nodes = next_nodes
            sep = ' ' * int(len(sep) / 2)  # cut separator size in half
        return content

    def insert(self, value):
        if self.root is None:
            self.root = AvlTree.TreeNode(value)
        else:
            self._insert(value, self.root)

    def _insert(self, value, cur_node):
        if value < cur_node.value:
            if cur_node.left_child is None:
                cur_node.left_child = AvlTree.TreeNode(value)
                cur_node.left_child.parent = cur_node  # set parent
                self._inspect_insertion(cur_node.left_child)
            else:
                self._insert(value, cur_node.left_child)
        elif value > cur_node.value:
            if cur_node.right_child is None:
                cur_node.right_child = AvlTree.TreeNode(value)
                cur_node.right_child.parent = cur_node  # set parent
                self._inspect_insertion(cur_node.right_child)
            else:
                self._insert(value, cur_node.right_child)
        else:
            print("Value already in tree!")

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)

    def _print_tree(self, cur_node):
        if cur_node is not None:
            self._print_tree(cur_node.left_child)
            print('%s, h=%d' % (str(cur_node.value), cur_node.height))
            self._print_tree(cur_node.right_child)

    def height(self):
        if self.root is not None:
            return self._height(self.root, 0)
        else:
            return 0

    def _height(self, cur_node, cur_height):
        if cur_node is None:
            return cur_height
        left_height = self._height(cur_node.left_child, cur_height + 1)
        right_height = self._height(cur_node.right_child, cur_height + 1)
        return max(left_height, right_height)

    def find(self, value):
        if self.root is not None:
            return self._find(value, self.root)
        else:
            return None

    def _find(self, value, cur_node):
        if value == cur_node.value:
            return cur_node
        elif value < cur_node.value and cur_node.left_child is not None:
            return self._find(value, cur_node.left_child)
        elif value > cur_node.value and cur_node.right_child is not None:
            return self._find(value, cur_node.right_child)

    def delete_value(self, value):
        return self.delete_node(self.find(value))

    def delete_node(self, node):
        # Protect against deleting a node not found in the tree
        if node is None or self.find(node.value) is None:
            print("Node to be deleted not found in the tree!")
            return None

        # returns the node with min value in tree rooted at input node
        def min_value_node(n):
            current = n
            while current.left_child is not None:
                current = current.left_child
            return current

        # returns the number of children for the specified node
        def num_children(n):
            # both parentheses are necessary
            return (n.left_child is not None) + (n.right_child is not None)

        # get the parent of the node to be deleted
        node_parent = node.parent

        # get the number of children of the node to be deleted
        node_children = num_children(node)

        # break operation into different cases based on the
        # structure of the tree & node to be deleted

        # CASE 1 (node has no children)
        if node_children == 0:

            if node_parent is not None:
                # remove reference to the node from the parent
                if node_parent.left_child == node:
                    node_parent.left_child = None
                else:
                    node_parent.right_child = None
            else:
                self.root = None

        # CASE 2 (node has a single child)
        if node_children == 1:

            # get the single child node
            if node.left_child is not None:
                child = node.left_child
            else:
                child = node.right_child

            if node_parent is not None:
                # replace the node to be deleted with its child
                if node_parent.left_child == node:
                    node_parent.left_child = child
                else:
                    node_parent.right_child = child
            else:
                self.root = child

            # correct the parent pointer in node
            child.parent = node_parent

        # CASE 3 (node has two children)
        if node_children == 2:
            # get the inorder successor of the deleted node
            successor = min_value_node(node.right_child)

            # copy the inorder successor's value to the node formerly
            # holding the value we wished to delete
            node.value = successor.value

            # delete the inorder successor now that it's value was
            # copied into the other node
            self.delete_node(successor)

            # exit function so we don't call the _inspect_deletion twice
            return

        if node_parent is not None:
            # fix the height of the parent of current node
            node_parent.height = 1 + max(AvlTree.get_height(node_parent.left_child),
                                         AvlTree.get_height(node_parent.right_child))

            # begin to traverse back up the tree checking if there are
            # any sections which now invalidate the AVL balance rules
            self._inspect_deletion(node_parent)

    def search(self, value):
        if self.root is not None:
            return self._search(value, self.root)
        else:
            return False

    def _search(self, value, cur_node):
        if value == cur_node.value:
            return True
        elif value < cur_node.value and cur_node.left_child is not None:
            return self._search(value, cur_node.left_child)
        elif value > cur_node.value and cur_node.right_child is not None:
            return self._search(value, cur_node.right_child)
        return False

    # Functions added for AVL...

    def _inspect_insertion(self, cur_node, path=None):
        if path is None:
            path = []
        if cur_node.parent is None:
            return
        path = [cur_node] + path

        left_height = AvlTree.get_height(cur_node.parent.left_child)
        right_height = AvlTree.get_height(cur_node.parent.right_child)

        if abs(left_height - right_height) > 1:
            path = [cur_node.parent] + path
            self._rebalance_node(path[0], path[1], path[2])
            return

        new_height = 1 + cur_node.height
        if new_height > cur_node.parent.height:
            cur_node.parent.height = new_height

        self._inspect_insertion(cur_node.parent, path)

    def _inspect_deletion(self, cur_node):
        if cur_node is None:
            return

        left_height = AvlTree.get_height(cur_node.left_child)
        right_height = AvlTree.get_height(cur_node.right_child)

        if abs(left_height - right_height) > 1:
            y = self.taller_child(cur_node)
            x = self.taller_child(y)
            self._rebalance_node(cur_node, y, x)

        self._inspect_deletion(cur_node.parent)

    def _rebalance_node(self, z, y, x):
        if y == z.left_child and x == y.left_child:
            self._right_rotate(z)
        elif y == z.left_child and x == y.right_child:
            self._left_rotate(y)
            self._right_rotate(z)
        elif y == z.right_child and x == y.right_child:
            self._left_rotate(z)
        elif y == z.right_child and x == y.left_child:
            self._right_rotate(y)
            self._left_rotate(z)
        else:
            raise Exception('_rebalance_node: z,y,x node configuration not recognized!')

    def _left_rotate(self, z):
        self._rotate(z, side=0)

    def _right_rotate(self, z):
        self._rotate(z, side=1)

    def _rotate(self, z, side=None):
        if side is None:
            return
        sub_root = z.parent
        y = z.get_child(1 - side)
        t = y.get_child(side)
        y.set_child(side, z)
        z.parent = y
        z.set_child(1 - side, t)
        if t is not None:
            t.parent = z
        y.parent = sub_root
        if y.parent is None:
            self.root = y
        elif y.parent.left_child == z:
            y.parent.left_child = y
        else:
            y.parent.right_child = y
        z.height = 1 + max(AvlTree.get_height(z.left_child),
                           AvlTree.get_height(z.right_child))
        y.height = 1 + max(AvlTree.get_height(y.left_child),
                           AvlTree.get_height(y.right_child))

    @staticmethod
    def get_height(cur_node: TreeNode):
        return cur_node.height if cur_node is not None else 0

    @staticmethod
    def taller_child(cur_node: TreeNode):
        left = AvlTree.get_height(cur_node.left_child)
        right = AvlTree.get_height(cur_node.right_child)
        return cur_node.left_child if left >= right else cur_node.right_child
