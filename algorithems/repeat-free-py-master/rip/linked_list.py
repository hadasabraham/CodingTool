# Source: https://github.com/Darthfett/Hashtable/blob/master/LinkedList.py
from typing import Optional, Iterable, Reversible


class Link:
    """ Link
        Used in the ChainedHashtable, a Link is a (key, value) pair for use in a linked list.
    """
    key:   int = 0
    value: Optional = None
    next:  Optional['Link'] = None
    prev:  Optional['Link'] = None

    def __init__(self, key: int, value, next: Optional['Link'] = None, prev: Optional['Link'] = None):
        self.key = key
        self.value = value
        self.next = next
        self.prev = prev

    def __str__(self):
        if self.next is None:
            return str(self.value) + " "
        else:
            return str(self.value) + " " + str(self.next)

    def __add__(self, add_to_value):
        return self.value + add_to_value

    def __sub__(self, sub_from_value):
        return self.value - sub_from_value

    def advance(self, index: int):
        link = self
        up = index > 0
        for i in range(abs(index)):
            link = link.next if up else link.prev
        return link


class LinkedList:
    head: Optional[Link]
    tail: Optional[Link]
    len:  int

    def __init__(self, head: Optional[Link] = None):
        self.head = head
        self.tail = head
        self.len = 1 if head else 0

    def push(self, new, prev: Optional[Link] = None):
        new.prev = prev
        if prev is None:
            new.next = self.head
            if new.next:
                new.next.prev = new
            self.head = new
        else:
            new.next = prev.next
            if new.next:
                new.next.prev = new
            prev.next = new
        if new.next is None:
            self.tail = new
        self.len += 1

    def pop(self, index: int = 0):
        cur = index
        prev_node = None
        cur_node = self.head
        while cur > 0:
            prev_node = cur_node
            cur_node = cur_node.next
            cur -= 1
        if cur_node.next is None:
            self.tail = prev_node

        cur_node.next.prev = prev_node
        if prev_node is None:
            popped = self.head
            self.head = cur_node.next
            self.len -= 1
            return popped
        else:
            prev_node.next = cur_node.next
            self.len -= 1
            return cur_node

    def insert(self, node: Link, index: int = 0):
        if node is None:
            raise Exception("node is None Type")
        cur = index
        prev_node = None
        next_node = self.head
        while cur > 0:
            if next_node is None:
                raise Exception("Index out of bounds")
            prev_node = next_node
            next_node = next_node.next
            cur -= 1

        node.prev = prev_node
        if prev_node is None:
            self.head = node
        else:
            prev_node.next = node

        node.next = next_node
        if next_node is None:
            self.tail = node
        self.len += 1

    def __str__(self):
        return str(self.head) if self.head is not None else ""

    def __len__(self):
        return self.len

    # Note: Iterator value is a Link, not its value (needed for Algorithm1's "index_in = AvlRankTree.from_sorted(iter)")
    def __iter__(self):
        curr = self.head
        while curr:
            yield curr
            curr = curr.next

    def remove_window_before(self, next_node: Optional[Link], k: int):
        self.remove_window_at(prev_node=(next_node.prev if next_node else self.tail).advance(-k), k=k)

    def remove_window_at(self, prev_node: Optional[Link], k: int):
        kth_node = prev_node.next if prev_node else self.head
        kth_node = kth_node.advance(k)
        if kth_node is None:
            self.tail = prev_node
        else:
            kth_node.prev = prev_node
        if prev_node is None:
            self.head = kth_node
        else:
            prev_node.next = kth_node
        self.len -= k

    def get_window_before(self, next_node: Optional[Link], k: int):
        self.get_window_at(prev_node=(next_node.prev if next_node else self.tail).advance(-k), k=k)

    def get_window_at(self, prev_node: Optional[Link], k: int):
        window = []
        if not prev_node:
            prev_node = self.head
            k -= 1
            window += [prev_node.value]
        for i in range(k):
            prev_node = prev_node.next
            window += [prev_node.value]
        return window

    def extend(self, other: 'LinkedList'):
        for node in other:
            self.push(node, self.tail)

    def extendleft(self, other: 'LinkedList'):
        prev = None
        for node in other:
            self.push(node, prev)
            prev = node

    @classmethod
    def from_iterable(cls, iterable: Iterable[int]) -> 'LinkedList':
        llist = cls()
        for i, val in enumerate(iterable):
            llist.push(Link(i, val), llist.tail)
        return llist
