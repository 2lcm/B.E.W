class Node(object):
    def __init__(self, val=None):
        self.prev = None
        self.next = None
        self.val = val


class LL(object):
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert(self, new):
        if type(new) != Node:
            new = Node(new)
        tmp = self.tail.prev
        tmp.next = new
        self.tail.prev = new
        new.prev = tmp
        new.next = self.tail

    def find(self, val):
        cur = self.head.next
        while cur != self.tail:
            if cur.val == val:
                return cur
            cur = cur.next

    def delete(self, target):
        if type(target) != Node:
            target = self.find(target)
        prev = target.prev
        next = target.next
        target.prev = None
        target.next = None
        prev.next = next
        next.prev = prev
        del target
        return next

    def print_all(self):
        cur = self.head.next
        while cur != self.tail:
            print(cur.val)
            cur = cur.next

    def to_list(self):
        cur = self.head.next
        res = []
        while cur != self.tail:
            res.append(cur.val)
            cur = cur.next
        return res
