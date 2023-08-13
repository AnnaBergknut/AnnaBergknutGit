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

    def remove(self, current, element):
        if current is None:
            return current
        
        if element < current.data:
            current.left = self.remove(current.left, element)  # Look in the left subtree
        elif element > current.data:
            current.right = self.remove(current.right, element)  # Look in the right subtree
        else:
            # Node with one child or no child
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left

            # Node with two children: find in-order successor and copy its data
            successor = self.get_min(current.right)
            current.data = successor

            # Delete the in-order successor
            current.right = self.remove(current.right, successor)

        return current

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
    bst = BST()
    for i in c_list:
        bst.insert(i)
    print(f"--------------------------before removal of {element_to_remove}--------------------------")
    print(bst.to_graphviz())
    bst.remove(bst._root, element_to_remove)
    print(f"--------------------------after removal of {element_to_remove}--------------------------")
    print(f"Does {element_to_find} exist in the tree?", bst.find(bst._root, element_to_find))
    print(f"--------------------------Pre order--------------------------")
    bst.pre_order_walk(bst._root)
    print(f"--------------------------In order--------------------------")
    bst.in_order_walk(bst._root)
    print(f"--------------------------Post order--------------------------")
    bst.post_order_walk(bst._root)
    
    print("height inclouding the root =", bst.get_tree_height(bst._root))
    print("height not inclouding the root =", bst.get_tree_height(bst._root) -1)
    print("min =", bst.get_min(bst._root))
    print("max =", bst.get_max(bst._root))
    
    print(bst.to_graphviz())

if __name__ == '__main__':
    main()
