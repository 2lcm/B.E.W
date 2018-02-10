class NODE(object):
    def __init__(self, temp_object):
        self.head = None
        self.tail = None
        self.value = temp_object


class LL(object):
    def __init__(self):
        self.head_node = NODE(None)
        self.tail_node = NODE(None)
        self.head_node.tail = self.tail_node
        self.tail_node.head = self.head_node

    def insert_value(self, val):
        ret = NODE(val)
        self.insert_node(ret)
        return ret

    def insert_node(self, new_node):
        end_node = self.tail_node.head # end_node means the node that is right front of tail_node
        end_node.tail = new_node
        new_node.head = end_node
        new_node.tail = self.tail_node
        self.tail_node.head = new_node

    def delete(self, del_node):
        current_node = self.head_node.tail
        while True:
            if current_node == self.tail_node:
                print('Incomplete Delete')
                break
            if current_node == del_node:
                front_node = current_node.head
                back_node = current_node.tail
                front_node.tail = back_node
                back_node.head = front_node
                del current_node.value
                del current_node
                # print('Perfect Delete')
                break
            current_node = current_node.tail

    # return [value_list, node_list]
    def to_list(self):
        current_node = self.head_node.tail
        ret1 = []
        ret2 = []
        ret = [ret1, ret2]
        while True:
            if current_node == self.tail_node:
                return ret
            ret1.append(current_node.value)
            ret2.append(current_node)
            current_node = current_node.tail

    def test(self):

        current_node = self.head_node
        while True:
            if current_node == self.tail_node:
                print('its done')
                break
            else:
                print(current_node.value)
                current_node = current_node.tail


if __name__ == '__main__':
    A = NODE('changyeop')
    B = NODE('chulmin')
    C = NODE('horse')
    Link = LL()
    Link.insert_node(A)
    Link.insert_node(B)
    Link.insert_node(C)
    Link.delete(B)
    # Link.delete(A)
    Link.test()
