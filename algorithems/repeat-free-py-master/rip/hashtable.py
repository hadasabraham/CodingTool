# Source: https://github.com/Darthfett/Hashtable/blob/master/Hashtable.py

import abc
import math
from typing import List, Callable
from rip.linked_list import *


class Hash:
    @staticmethod
    def division_hash(key, size) -> int:
        return key % size

    @staticmethod
    def auxiliary_hash_quad(key, size) -> int:
        a = 0.618
        return int(math.floor(size * ((key * a) % 1)))

    @staticmethod
    def linear_hash(key, i, size) -> int:
        return (Hash.auxiliary_hash_quad(key, size) + i) % size

    @staticmethod
    def auxiliary_hash_double(key, size) -> int:
        return 1 + (key % (size - 1))

    @staticmethod
    def quadratic_hash(key, i, size) -> int:
        c_1 = 0.5
        c_2 = 0.5
        return int((Hash.auxiliary_hash_quad(key, size) + c_1 * i + c_2 * i * i) % size)

    @staticmethod
    def double_hash(key, i, size) -> int:
        return int((Hash.division_hash(key, size) + i * Hash.auxiliary_hash_double(key, size)) % size)


class ChainedHashtable:
    """ Chained Hashtable
        A linked list of Keys and Values are stored in the links array, which holds a linked list of all mapped values
    """

    def __init__(self, size=32, pre_hash: Optional[Callable] = None):
        self.size: int = size
        self.links: List[Optional[LinkedList]] = [None] * self.size
        self.pre_hash = pre_hash if pre_hash else lambda x: x.__hash__()

    def get(self, key):
        llist = self.links[self.hash(key)]
        if llist is None:
            return None
        cur_node = llist.head
        while cur_node is not None:
            if cur_node.key == key:
                return cur_node.value
            else:
                cur_node = cur_node.next
        return None

    def __getitem__(self, item):
        return self.get(item)

    def search(self, key):
        llist = self.links[self.hash(key)]
        if llist is None:
            return str(self.hash(key))
        search_result = ""
        cur_node = llist.head
        search_result += str(self.hash(key)) + " "
        while cur_node is not None:
            search_result += str(cur_node.value) + " "
            if cur_node.key == key:
                return search_result
            else:
                cur_node = cur_node.next
        return search_result

    def put(self, key, value):
        llist = self.links[self.hash(key)]
        if llist is None:
            node = Link(key=key, value=value)
            llist = LinkedList(head=node)
            self.links[self.hash(key)] = llist
            return
        cur_node = llist.head
        while cur_node is not None:
            if cur_node.key == key:
                cur_node.value = value
                return cur_node
            else:
                cur_node = cur_node.next
        link = Link(key=key, value=value)
        llist.push(link)
        return link

    def __setitem__(self, key, value):
        self.put(key, value)

    def insert(self, value):
        self.put(value, value)

    def hash(self, key):
        return Hash.division_hash(self.pre_hash(key) if self.pre_hash else key, self.size)

    def __str__(self):
        lines = []
        for i in range(len(self.links)):
            if self.links[i] is None:
                lines.append("" + str(i) + "\t")
            else:
                lines.append("" + str(i) + "\t" + str(self.links[i]))
        return "\n".join(lines)


# region Associative Hashtables
class Entry:
    """ Entry
        Used in every hashtable but the ChainedHashtable, an Entry is a (key, value) pair
    """

    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value

    def __str__(self):
        return str(self.value)


class AssociativeHashtable:
    """ Associative Hashtable
        Keys and Values are stored in an associative array, probed for values by some associative hash function
    """

    def __init__(self, size=32):
        self.size: int = size
        self.entries: List[Optional[Entry]] = [None] * self.size

    def get(self, key):
        i = 0
        entry = self.entries[self.hash(key, i)]
        while entry is None or entry.key != key:
            i += 1
            if i == self.size:
                return None
            entry = self.entries[self.hash(key, i)]
        return entry.value

    def __getitem__(self, item):
        return self.get(item)

    def search(self, key):
        i = 0
        entry = self.entries[self.hash(key, i)]
        search_result = str(self.hash(key, i)) + " "
        while entry is None or entry.key != key:
            i += 1
            if i == self.size:
                return search_result + "-1"
            entry = self.entries[self.hash(key, i)]
            search_result += str(self.hash(key, i)) + " "
        return search_result

    def put(self, key, value):
        i = 0
        entry = self.entries[self.hash(key, i)]
        while entry is not None and entry.key != key:
            i += 1
            if i == self.size:
                raise Exception("Table is full!")
            entry = self.entries[self.hash(key, i)]
        if entry is None:
            entry = Entry(key=key, value=value)
            self.entries[self.hash(key, i)] = entry
        else:
            entry.value = value

    def __setitem__(self, key, value):
        self.put(key, value)

    def insert(self, value):
        self.put(value, value)

    @abc.abstractmethod
    def hash(self, key, i):
        pass

    def __str__(self):
        lines = []
        for i in range(len(self.entries)):
            if self.entries[i] is None:
                lines.append("" + str(i) + "\t" + "-1")
            else:
                lines.append("" + str(i) + "\t" + str(self.entries[i].value))
        return "\n".join(lines)


class LinearHashtable(AssociativeHashtable):
    """ Linear Hashtable
        Keys and Values are stored in an associative array, probed for values by searching linearly through the table
    """
    def hash(self, key, i):
        return Hash.linear_hash(key, i, self.size)


class QuadraticHashtable(AssociativeHashtable):
    """ Quadratic Hashtable
        Keys and Values are stored in an associative array, probed for values by searching quadratically through table
    """
    def hash(self, key, i):
        return Hash.quadratic_hash(key, i, self.size)


class DoubleHashtable(AssociativeHashtable):
    """ Double Hashtable
        Keys and Values are stored in an associative array, probed for values by searching with double hashing
    """
    def hash(self, key, i):
        return Hash.double_hash(key, i, self.size)

# endregion
