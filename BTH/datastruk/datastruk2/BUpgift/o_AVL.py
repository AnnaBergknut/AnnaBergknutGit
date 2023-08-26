class AVL:
    class Node:
        def __init__(self):
            self.left = None
            self.right = None
            self.data = None
            self.height = None

    def __init__(self):
        self._root = None
        self.node_id = 0  # ONLY USED WITHIN to_graphviz()!
        pass

    def insert(self, element):
        pass
        def insert(self, element):
            """ The funktion used to create the tree """
            current = self._root
            if current is None:
                return self.Node(element)
            elif element == current.data:
                return  # Already exists, do nothing
            elif element < current.data:
                current.left = self.insert(current.left, element)
            else:
                current.right = self.insert(current.right, element)

            current.height = 1 + max(self.get_tree_height(current.left), self.get_tree_height(current.right))

            balance = self.get_balance(current)

            if balance > 1 and element < current.left.data:
                return self.rotate_right(current)

            if balance < -1 and element > current.right.data:
                return self.rotate_left(current)

            if balance > 1 and element > current.left.data:
                current.left = self.rotate_left(current.left)
                return self.rotate_right(current)

            if balance < -1 and element < current.right.data:
                current.right = self.rotate_right(current.right)
                return self.rotate_left(current)

            return current
        def insert(self, element):
        """ The funktion used to create the tree """
        new_node = self.Node(element)
        if self._root is None:
            self._root = new_node
            return 

        current = self._root
        parent = None

        while current:
            parent = current
            if element == current.data:
                return  # Already exists, do nothing
            elif element < current.data:
                current = current.left
            else:
                current = current.right

        if element < parent.data:
            parent.left = new_node
        else:
            parent.right = new_node

        current = new_node  # Update the current node to the new node

        current.height = 1 + max(self.temp_get_tree_height(current.left), self.temp_get_tree_height(current.right))

        balance = self.get_balance(current)

        if balance > 1 and element < current.left.data:
            return self.rotate_right(current)

        if balance < -1 and element > current.right.data:
            return self.rotate_left(current)

        if balance > 1 and element > current.left.data:
            current.left = self.rotate_left(current.left)
            return self.rotate_right(current)

        if balance < -1 and element < current.right.data:
            current.right = self.rotate_right(current.right)
            return self.rotate_left(current)

        return current

    def get_balance(self, current):
        """ """
        if current is None:
            return 0
        return self.temp_get_tree_height(current.left) - self.temp_get_tree_height(current.right)

    def rotate_left(self, parent):
        """ """
        child = parent.right
        grandchild = child.left

        child.left = parent
        parent.right = grandchild

        parent.height = 1 + max(self.temp_get_tree_height(parent.left), self.temp_get_tree_height(parent.right))
        child.height = 1 + max(self.temp_get_tree_height(child.left), self.temp_get_tree_height(child.right))

        return child

    def rotate_right(self, parent):
        """ """
        child = parent.left
        grandchild = child.right

        child.right = parent
        parent.left = grandchild

        parent.height = 1 + max(self.temp_get_tree_height(parent.left), self.temp_get_tree_height(parent.right))
        child.height = 1 + max(self.temp_get_tree_height(child.left), self.temp_get_tree_height(child.right))

        return child


    def remove(self, element):
        pass

    def find(self, element):
        pass

    def pre_order_walk(self):
        pass

    def in_order_walk(self):
        pass

    def post_order_walk(self):
        pass

    def get_tree_height(self):
        pass

    def get_min(self):
        pass

    def get_max(self):
        pass

    def to_graphviz_rec(self, data, current):
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
        data = ""
        if self._root is not None:
            self.node_id = 0
            data += "digraph {\n"
            data += "\tRoot [shape=plaintext];\n"
            data += "\t\"Root\" -> 0 [color=black];\n"
            data = self.to_graphviz_rec(data, self._root)
            data += "}\n"
        return data
