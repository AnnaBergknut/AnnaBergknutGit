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

    def insert(self, data):
        new_node = self.Node()
        new_node.data = data

        if not self._root:
            self._root = new_node
            return

        current = self._root
        parent = None
        while current:
            parent = current
            if data < current.data:
                current = current.left
            else:
                current = current.right

        if data < parent.data:
            parent.left = new_node
        else:
            parent.right = new_node

        self.rebalance_tree(new_node)

    def remove(self, data):
        if not self._root:
            return

        parent = None
        current = self._root
        while current and current.data != data:
            parent = current
            if data < current.data:
                current = current.left
            else:
                current = current.right

        if not current:
            return

        if current.left and current.right:
            successor_parent = current
            successor = current.right
            while successor.left:
                successor_parent = successor
                successor = successor.left
            current.data = successor.data
            parent = successor_parent
            current = successor

        child = None
        if current.left:
            child = current.left
        elif current.right:
            child = current.right

        if not parent:
            self._root = child
        elif parent.left == current:
            parent.left = child
        else:
            parent.right = child

        self.rebalance_tree(parent)

    def rebalance_tree(self, start_node):
        current = start_node
        while current:
            current.height = 1 + max(self.get_tree_height(current.left), self.get_tree_height(current.right))
            balance = self.get_balance(current)

            if balance > 1 and self.get_balance(current.left) >= 0:
                current = self.rotate_right(current)
            elif balance < -1 and self.get_balance(current.right) <= 0:
                current = self.rotate_left(current)
            elif balance > 1 and self.get_balance(current.left) < 0:
                current.left = self.rotate_left(current.left)
                current = self.rotate_right(current)
            elif balance < -1 and self.get_balance(current.right) > 0:
                current.right = self.rotate_right(current.right)
                current = self.rotate_left(current)

            if current == self._root:
                break

            parent = self.find_parent(self._root, current)
            if parent:
                if current.data < parent.data:
                    parent.left = current
                else:
                    parent.right = current
            current = parent
    
    def find_parent(self, root, node):
        parent = None
        current = root
        while current:
            if node.data == current.data:
                return parent
            parent = current
            if node.data < current.data:
                current = current.left
            else:
                current = current.right

        return None
    
    def get_balance(self, current):
        if current is None:
            return 0
        return self.get_tree_height(current.left) - self.get_tree_height(current.right)

    def rotate_left(self, parent):
        child = parent.right
        grandchild = child.left

        child.left = parent
        parent.right = grandchild

        parent.height = 1 + max(self.get_tree_height(parent.left), self.get_tree_height(parent.right))
        child.height = 1 + max(self.get_tree_height(child.left), self.get_tree_height(child.right))

        return child

    def rotate_right(self, parent):
        child = parent.left
        grandchild = child.right

        child.right = parent
        parent.left = grandchild

        parent.height = 1 + max(self.get_tree_height(parent.left), self.get_tree_height(parent.right))
        child.height = 1 + max(self.get_tree_height(child.left), self.get_tree_height(child.right))

        return child

    def find(self, current, element):
        if current is None:
            return False

        if current.data == element:  # Compare the data of the current node
            return True
        elif element < current.data:
            return self.find(current.left, element)  # Looking in the left subtree
        else:
            return self.find(current.right, element)  # Looing in the right subtree

    def pre_order_walk(self, current):
        if current:
            print(current.data)
            self.pre_order_walk(current.left)
            self.pre_order_walk(current.right)

    def in_order_walk(self, current):
        if current:
            self.in_order_walk(current.left)
            print(current.data)
            self.in_order_walk(current.right)

    def post_order_walk(self, current):
        if current:
            self.post_order_walk(current.left)
            self.post_order_walk(current.right)
            print(current.data)

    def get_tree_height(self, current):
        if current is None:
            return 0
        else:
            leftHeight = self.get_tree_height(current.left)
            rightHeight = self.get_tree_height(current.right)
            return max(leftHeight, rightHeight) + 1

    def get_min(self , current):
        while (current.left is not None):
            current = current.left
        return current.data

    def get_max(self, current):
        while (current.right is not None):
            current = current.right
        return current.data

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
        
def main():
    a_list = [ 1,2,3,4,5,6,7,8,9 ]
    b_list = [ 1,9,2,8,3,4,7,5,6 ]
    c_list = [ 7,3,5,6,8,2,1,4,9 ]
    element_to_find = 5
    element_to_remove = 3
    avl = AVL()
    for element in b_list:
        avl.insert(element)
    print("::::::::::::::::::::::::::AVL::::::::::::::::::::::::::")
    print(f"--------------------------Before removal of {element_to_remove}--------------------------")
    print(avl.to_graphviz())
    avl.remove(avl._root, element_to_remove)
    print(f"--------------------------After removal of {element_to_remove}--------------------------")
    print(f"Does {element_to_find} exist in the tree?", avl.find(avl._root, element_to_find))
    print(f"--------------------------Pre order--------------------------")
    avl.pre_order_walk(avl._root)
    print(f"--------------------------In order--------------------------")
    avl.in_order_walk(avl._root)
    print(f"--------------------------Post order--------------------------")
    avl.post_order_walk(avl._root)
    
    print("Height inclouding the root =", avl.get_tree_height(avl._root))
    print("Height not inclouding the root =", avl.get_tree_height(avl._root) -1)
    print("Min =", avl.get_min(avl._root))
    print("Max =", avl.get_max(avl._root))
    
    print(avl.to_graphviz())

if __name__ == '__main__':
    main()
