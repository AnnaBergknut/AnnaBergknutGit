''' '''
class BST:
    class Node:
        def __init__(self):
            self.left = None
            self.right = None
            self.data = None

    def __init__(self):
        self._root = None
        self.node_id = 0  # ONLY USED WITHIN to_graphviz()!

    def insert(self, element):
        new_node = self.Node()
        new_node.data = element
        if self._root is None:
            self._root = new_node
            return
        current = self._root
        while current != None:
            parent = current
            if element < current.data:
                current = current.left
            else:
                current = current.right
        if element < parent.data:
            parent.left = new_node
        else:
            parent.right = new_node

    def remove(self, element):
        if self._root is None:
            return self._root
        
        if self._root > element:
            self._root.left = self.remove(self._root.left, element)
            return self._root
        elif self._root < element:
            self._root.right = self.remove(self._root.right, element)
            return self._root

    def find(self, element):
        pass

    def pre_order_walk(self):
        pass

    def in_order_walk(self):
        pass

    def post_order_walk(self):
        pass

    def get_tree_height(self, node):
        if node is None:
            return 0
        leftHeight= self.get_tree_height(node.left)
        rightHeight= self.get_tree_height(node.right)
        max_height= leftHeight
        if rightHeight>max_height:
            max_height = rightHeight
        return max_height+1

    def get_min(self):
        current = self._root
        while(current.left is not None):
            current = current.left
        return current.data

    def get_max(self):
        current = self._root
        while(current.right is not None):
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
    bst = BST()
    for i in c_list:
        bst.insert(i)
    print("min =", bst.get_min())
    print("max =", bst.get_max())
    print("hight =", bst.get_tree_height(bst._root))
    print("remove node", bst.remove(3))
    print(bst.to_graphviz())

if __name__ == '__main__':
    main()
