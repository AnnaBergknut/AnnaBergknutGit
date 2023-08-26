""" AVL tree, Anna Bergknut """
class AVL:
    """ Class for AVL """
    class Node:
        """ Class for Node"""
        def __init__(self, data):
            self.left = None
            self.right = None
            self.data = data
            self.height = 1

    def __init__(self):
        self._root = None
        self.node_id = 0

    def insert(self, element):
        new_node = self.Node(element)
        if self._root is None:
            self._root = new_node
            return 

        self._root = self._insert_recursive(self._root, new_node)

    def _insert_recursive(self, current, new_node):
        if current is None:
            return new_node

        if new_node.data == current.data:
            return current
        elif new_node.data < current.data:
            current.left = self._insert_recursive(current.left, new_node)
        else:
            current.right = self._insert_recursive(current.right, new_node)

        current.height = 1 + max(self._get_tree_height(current.left), self._get_tree_height(current.right))
        balance = self.get_balance(current)

        if balance > 1 and new_node.data < current.left.data:
            return self.rotate_right(current)

        if balance < -1 and new_node.data > current.right.data:
            return self.rotate_left(current)

        if balance > 1 and new_node.data > current.left.data:
            current.left = self.rotate_left(current.left)
            return self.rotate_right(current)

        if balance < -1 and new_node.data < current.right.data:
            current.right = self.rotate_right(current.right)
            return self.rotate_left(current)

        return current

    def get_balance(self, current):
        if current is None:
            return 0
        return self._get_tree_height(current.left) - self._get_tree_height(current.right)

    def rotate_left(self, parent):
        child = parent.right
        grandchild = child.left

        child.left = parent
        parent.right = grandchild

        parent.height = 1 + max(self._get_tree_height(parent.left), self._get_tree_height(parent.right))
        child.height = 1 + max(self._get_tree_height(child.left), self._get_tree_height(child.right))

        return child

    def rotate_right(self, parent):
        child = parent.left
        grandchild = child.right

        child.right = parent
        parent.left = grandchild

        parent.height = 1 + max(self._get_tree_height(parent.left), self._get_tree_height(parent.right))
        child.height = 1 + max(self._get_tree_height(child.left), self._get_tree_height(child.right))

        return child

    def remove(self, element):
        """ I had a miss match with the inputs, needed to know what node to start on """
        self._root = self._remove(self._root, element)
        return self._root

    def _remove(self, current, element):
        """ """
        if current is None:
            return current
        
        if element < current.data:
            current.left = self._remove(current.left, element)  # Look in the left subtree
        elif element > current.data:
            current.right = self._remove(current.right, element)  # Look in the right subtree
        else:
            if current.left is None and current.right is None: # No child
                return None
            elif current.right is None and current.left is not None: # Only left
                return current.left
            elif current.left is None: # Only right
                return current.right
            else: # Has both
                successor = self._get_min(current.right)
                current.data = successor
                current.right = self._remove(current.right, successor)

        current.height = 1 + max(self._get_tree_height(current.left), self._get_tree_height(current.right))
        balance = self.get_balance(current)

        if balance > 1 and self.get_balance(current.left) >= 0:
            return self.rotate_right(current)

        if balance < -1 and self.get_balance(current.right) <= 0:
            return self.rotate_left(current)

        if balance > 1 and self.get_balance(current.left) < 0:
            current.left = self.rotate_left(current.left)
            return self.rotate_right(current)

        if balance < -1 and self.get_balance(current.right) > 0:
            current.right = self.rotate_right(current.right)
            return self.rotate_left(current)

        return current

    def find(self, element):
        """ Finds the node """
        current = self._root
        while current:
            if current.data == element:
                return True
            elif element < current.data:
                current = current.left  # Move to the left subtree
            else:
                current = current.right  # Move to the right subtree
        return False

    def pre_order_walk(self):
        """ I had a miss match with the inputs, needed to know what node to start on """
        my_list = []
        self._pre_order_walk(my_list, self._root)
        return my_list

    def _pre_order_walk(self, my_list, current):
        """ Pre order reclusive """
        if current:
            my_list.append(current.data)
            self._pre_order_walk(my_list, current.left)
            self._pre_order_walk(my_list, current.right)

    def in_order_walk(self):
        """ I had a miss match with the inputs, needed to know what node to start on """
        my_list = []
        self._in_order_walk(my_list, self._root)
        return my_list

    def _in_order_walk(self,my_list,  current):
        """ In order reclusive """
        if current:
            self._in_order_walk(my_list, current.left)
            my_list.append(current.data)
            self._in_order_walk(my_list, current.right)

    def post_order_walk(self):
        """ I had a miss match with the inputs, needed to know what node to start on """
        my_list = []
        self._post_order_walk(my_list, self._root)
        return my_list

    def _post_order_walk(self, my_list, current):
        """" Post order reclusive """
        if current:
            self._post_order_walk(my_list, current.left)
            self._post_order_walk(my_list, current.right)
            my_list.append(current.data)

    def get_tree_height(self):
        return self._get_tree_height(self._root)
        
    def _get_tree_height(self, current):
        """ Used BFS to count the deepest branch """
        if current is None:
            return -1

        queue = [(current, 1)]
        max_height = 0

        while queue:
            current, height = queue.pop(0)
            max_height = max(max_height, height)

            if current.left:
                queue.append((current.left, height + 1))

            if current.right:
                queue.append((current.right, height + 1))

        return max_height-1

    def get_min(self):
        """ I had a miss match with the inputs, needed to know what node to start on """
        return self._get_min(self._root)

    def _get_min(self, current):
        """ Find smalest node from startpoint """
        while current.left is not None:
            current = current.left
        return current.data

    def get_max(self):
        """" I had a miss match with the inputs, needed to know what node to start on """
        return self._get_max(self._root)

    def _get_max(self, current):
        """ Find biggest nod from startpoint """
        while current.right is not None:
            current = current.right
        return current.data

    def to_graphviz_rec(self, data, current):
        """ Not my funktion """
        my_node_id = self.node_id
        data += "\t" + str(my_node_id) + \
            " [label=\"" + str(current.data) + "\"];\n"
        self.node_id += 1
        if current.left is not None:
            data += "\t" + str(my_node_id) + " -> " + \
                str(self.node_id) + " [color=blue];\n"
            data = self.to_graphviz_rec(data, current.left)
        else:
            data += "\t" + str(self.node_id) + " [label=nill,style=invis];\n"
            data += "\t" + str(my_node_id) + " -> " + \
                str(self.node_id) + " [style=invis];\n"

        self.node_id += 1
        if current.right is not None:
            data += "\t" + str(my_node_id) + " -> " + \
                str(self.node_id) + " [color=red];\n"
            data = self.to_graphviz_rec(data, current.right)
        else:
            data += "\t" + str(self.node_id) + " [label=nill,style=invis];\n"
            data += "\t" + str(my_node_id) + " -> " + \
                str(self.node_id) + " [style=invis];\n"

        return data

    def to_graphviz(self):
        """ Not my funktion """
        data = ""
        if self._root is not None:
            self.node_id = 0
            data += "digraph {\n"
            data += "\tRoot [shape=plaintext];\n"
            data += "\t\"Root\" -> 0 [color=black];\n"
            data = self.to_graphviz_rec(data, self._root)
            data += "}\n"
        return data
        
def main():
    """ Main """
    a_list = [ 1,2,3,4,5,6,7,8,9 ]
    b_list = [ 1,9,2,8,3,4,7,5,6 ]
    c_list = [ 7,3,5,6,8,2,1,4,9 ]
    d_list = [2,1,3]
    e_list = [3, 2, 1, 4, 5, 6, 7, 16, 15, 14, 13, 12, 11, 10, 8, 9]
    f_list = []
    g_list = [3, 2, 1, 4, 5, 6, 7]
    element_to_find = 5
    element_to_delete = 12
    avl = AVL()
    for element in e_list:
        avl.insert(element)
    print(":::: AVL ::::")
    print(f"-- Before removal of {element_to_delete} --")
    print(avl.to_graphviz())
    avl.remove(element_to_delete)
    print(f"-- After removal of {element_to_delete} --")
    print(avl.to_graphviz())
    print(f"Does {element_to_find} exist in the tree?", avl.find(element_to_find))
    # print(f"-- Pre order --")
    # avl.pre_order_walk()
    # print(f"-- In order --")
    # avl.in_order_walk()
    # print(f"-- Post order --")
    # avl.post_order_walk()
    print("Height =", avl.get_tree_height())
    print("Min =", avl.get_min())
    print("Max =", avl.get_max())

if __name__ == '__main__':
    main()