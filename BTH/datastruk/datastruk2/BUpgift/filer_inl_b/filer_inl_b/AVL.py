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

    def remove(self, element):
        pass

    def find(self, node, element):
        if node is None:
            return False

        if node.data == element:  # Compare the data of the current node
            return True
        elif element < node.data:
            return self.find(node.left, element)  # Looking in the left subtree
        else:
            return self.find(node.right, element)  # Looing in the right subtree

    def pre_order_walk(self, node):
        current = node
        if current:
            print(current.data)
            self.pre_order_walk(current.left)
            self.pre_order_walk(current.right)

    def in_order_walk(self, node):
        current = node
        if current:
            self.in_order_walk(current.left)
            print(current.data)
            self.in_order_walk(current.right)

    def post_order_walk(self, node):
        current = node
        if current:
            self.post_order_walk(current.left)
            self.post_order_walk(current.right)
            print(current.data)

    def get_tree_height(self, node):
        if node is None:
            return 0
        else:
            leftHeight = self.get_tree_height(node.left)
            rightHeight = self.get_tree_height(node.right)
            return max(leftHeight, rightHeight) + 1

    def get_min(self , node):
        current = node
        while (current.left is not None):
            current = current.left
        return current.data

    def get_max(self, node):
        current = node
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
        for i in c_list:
            avl.insert(i)
        print(f"--------------------------before removal of {element_to_remove}--------------------------")
        print(avl.to_graphviz())
        avl.remove(avl._root, element_to_remove)
        print(f"--------------------------after removal of {element_to_remove}--------------------------")
        print(f"Does {element_to_find} exist in the tree?", avl.find(avl._root, element_to_find))
        print(f"--------------------------Pre order--------------------------")
        avl.pre_order_walk(avl._root)
        print(f"--------------------------In order--------------------------")
        avl.in_order_walk(avl._root)
        print(f"--------------------------Post order--------------------------")
        avl.post_order_walk(avl._root)
        
        print("height inclouding the root =", avl.get_tree_height(avl._root))
        print("height not inclouding the root =", avl.get_tree_height(avl._root) -1)
        print("min =", avl.get_min(avl._root))
        print("max =", avl.get_max(avl._root))
        
        print(avl.to_graphviz())

if __name__ == '__main__':
    main()
