""" BST tree, Anna Bergknut """
class BST:
    """ Class for the bst tree """
    class Node:
        """ Class for the nodes """
        def __init__(self):
            self.left = None
            self.right = None
            self.data = None

    def __init__(self):
        self._root = None
        self.node_id = 0

    def insert(self, element):
        """ The funktion used to create the tree """
        new_node = self.Node()
        new_node.data = element
        if self._root is None: # First node
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
            parent.left = new_node # Smaller
        else:
            parent.right = new_node # Bigger

    def remove(self, element):
        """ I had a miss match with the inputs, needed to know what node to start on """
        self._root = self.temp_remove(self._root, element)
        return self._root

    def temp_remove(self, current, element):
        """ Find, remove and then fixing the tree """
        if current is None: # No tree
            return current

        if element < current.data:
            current.left = self.temp_remove(current.left, element)  # Look in the left subtree
        elif element > current.data:
            current.right = self.temp_remove(current.right, element)  # Look in the right subtree
        else:
            if current.left is None and current.right is None: # No child
                if current == self._root:# Remove the root if it's the only node
                    return None
                else:
                    current = None
            elif current.right is None and current.left is not None: # Only left
                return current.left
            else: # Has right or both
                successor = self.temp_get_min(current.right)
                current.data = successor
                current.right = self.temp_remove(current.right, successor)
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
        self.temp_pre_order_walk(my_list, self._root)
        return my_list

    def temp_pre_order_walk(self, my_list, current):
        """ Pre order reclusive """
        if current:
            my_list.append(current.data)
            self.temp_pre_order_walk(my_list, current.left)
            self.temp_pre_order_walk(my_list, current.right)

    def in_order_walk(self):
        """ I had a miss match with the inputs, needed to know what node to start on """
        my_list = []
        self.temp_in_order_walk(my_list, self._root)
        return my_list

    def temp_in_order_walk(self,my_list,  current):
        """ In order reclusive """
        if current:
            self.temp_in_order_walk(my_list, current.left)
            my_list.append(current.data)
            self.temp_in_order_walk(my_list, current.right)

    def post_order_walk(self):
        """ I had a miss match with the inputs, needed to know what node to start on """
        my_list = []
        self.temp_post_order_walk(my_list, self._root)
        return my_list

    def temp_post_order_walk(self, my_list, current):
        """" Post order reclusive """
        if current:
            self.temp_post_order_walk(my_list, current.left)
            self.temp_post_order_walk(my_list, current.right)
            my_list.append(current.data)

    def get_tree_height(self):
        """ Used BFS to count the deepest breanch """
        current = self._root
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
        return self.temp_get_min(self._root)

    def temp_get_min(self , current):
        """ Find smalest node from startpoint """
        while current.left is not None:
            current = current.left
        return current.data

    def get_max(self):
        """" I had a miss match with the inputs, needed to know what node to start on """
        return self.temp_get_max(self._root)

    def temp_get_max(self, current):
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
    element_to_find = 5
    element_to_delete = 3
    bst = BST()
    for element in d_list:
        bst.insert(element)
    print("::::BST::::")
    print(f"-- Before removal of {element_to_delete} --")
    print(bst.to_graphviz())
    bst.remove(element_to_delete)
    print(f"-- After removal of {element_to_delete} --")
    print(bst.to_graphviz())
    print(f"Does {element_to_find} exist in the tree?", bst.find(element_to_find))
    print(f"-- Pre order --")
    bst.pre_order_walk()
    print(f"-- In order --")
    bst.in_order_walk()
    print(f"-- Post order --")
    bst.post_order_walk()
    print("Height =", bst.get_tree_height())
    print("Min =", bst.get_min())
    print("Max =", bst.get_max())

if __name__ == '__main__':
    main()
