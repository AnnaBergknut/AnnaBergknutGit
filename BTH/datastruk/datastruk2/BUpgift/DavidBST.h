#ifndef BST_H
#define BST_H

#include <vector>
#include <string>
#include <iostream>

template <class T>
class BST
{
private:
	class Node
	{
	public:
		T element;
		Node *leftChild;
		Node *rightChild;
		Node *parent = nullptr;
		Node(T element);
		~Node();
	};

	Node *root = nullptr;
	void ToGraphvizHelper(std::string& listOfNodes, std::string& listOfConnections, Node* toWorkWith, size_t& uniqueID);
public:
	BST();
	~BST();

	void insert(T element);

	void rec_find_preorder(std::vector<T>& vec, Node* below);
	void remove(T element);

	bool find(T element);

	void rec_find_inorder(std::vector<T>& vec, Node* sub_tree);
	std::vector<T> inOrderWalk();
	std::vector<T> preOrderWalk();
	void rec_find_postorder(std::vector<T>& vec, Node* sub_tree);
	std::vector<T> postOrderWalk();

	int rec_treeheight(Node* current);
	int getTreeHeight();

	T getMin();
	T getMax();

	std::string ToGraphviz();
};


template <typename T>
BST<T>::Node::Node(T element) : element(element), leftChild(nullptr), rightChild(nullptr)
{
}

template <typename T>
BST<T>::BST()
{}



template <typename T>
BST<T>::~BST()
{}


template <typename T>
void BST<T>::insert(T element)
{
	if (root == nullptr)
	{
		root = new Node(element);
	}
	else
	{
		Node* current = root;
		Node* parent = nullptr;
		while (current != nullptr)
		{
			parent = current;
			if (element == current->element)
			{
				break;
			}
			else if (element < current->element)
			{
				current = current->leftChild;
			}
			else
			{
				current = current->rightChild;
			}

		}
		if (element < parent->element)
		{
			parent->leftChild = new Node(element);
			parent->leftChild->parent = parent;
		}
		else if (element > parent->element)
		{
			parent->rightChild = new Node(element);
			parent->rightChild->parent = parent;
		}
	}
}




template <typename T>
void BST<T>::rec_find_preorder(std::vector<T>& vec, Node* sub_tree)
{
	if (sub_tree->leftChild != nullptr)
	{
		vec.push_back(sub_tree->leftChild->element);
		rec_find_preorder(vec, sub_tree->leftChild);
	}
	if (sub_tree->rightChild != nullptr)
	{
		vec.push_back(sub_tree->rightChild->element);
		rec_find_preorder(vec, sub_tree->rightChild);

	}
}

template <typename T>
void BST<T>::remove(T element)
{
	if(find(element))
	{
		Node* remove_branch = root;
		while (remove_branch->element != element)
		{
			if (element < remove_branch->element)
			{
				remove_branch = remove_branch->leftChild;
			}
			else
			{
				remove_branch = remove_branch->rightChild;
			}
		}
		
		if (remove_branch->leftChild != nullptr)
		{
			
			Node* current = remove_branch->leftChild;
			while (current->rightChild != nullptr)
			{
				current = current->rightChild;
			}
			
			
			if (remove_branch->parent != nullptr)
			{
				current->parent = remove_branch->parent;
				if (remove_branch->parent->rightChild == remove_branch)
				{
					remove_branch->parent->rightChild = current;
				}
				else
				{
					remove_branch->parent->leftChild = current;
				}

				if (current->leftChild != nullptr)
				{
					if (remove_branch->leftChild == current)
					{

						current->parent = remove_branch->parent;
						
					}
					else
					{
						current->leftChild->parent = current->parent;
						if (current->parent->rightChild == current)
						{
							current->parent->rightChild = current;
						}
						else if (current->parent->leftChild == current)
						{
							current->parent->leftChild = current;
						}
						current->leftChild = remove_branch->leftChild;
						if (remove_branch->rightChild != nullptr)
						{
							current->rightChild = remove_branch->rightChild;
						}
					}
					
				}

			}
			else
			{
				current->parent = nullptr;
				root = current;
				if (remove_branch->rightChild != nullptr)
					{
						current->rightChild = remove_branch->rightChild;
						remove_branch->rightChild->parent = current;
					}
			}

			

		}
		else if(remove_branch->rightChild != nullptr)
		{
			
			Node* current = remove_branch->rightChild;
			while (current->leftChild != nullptr)
			{
				current = current->leftChild;
			}
			
			
			if (remove_branch->parent != nullptr)
			{
				current->parent = remove_branch->parent;
				if (remove_branch->parent->leftChild == remove_branch)
				{
					remove_branch->parent->leftChild = current;
				}
				else
				{
					remove_branch->parent->rightChild = current;
				}


				if (current->rightChild != nullptr)
				{
					if (remove_branch->rightChild == current)
					{
						current->parent = remove_branch->parent;
					}
					else
					{
						current->rightChild->parent = current->parent;
						if (current->parent->leftChild == current)
						{
							current->parent->leftChild = current;
						}
						else if (current->parent->rightChild == current)
						{
							current->parent->rightChild = current;
						}
						current->rightChild = remove_branch->rightChild;
						if (remove_branch->leftChild != nullptr)
						{
							current->leftChild = remove_branch->leftChild;
						}
					}
					
				}

			}
			else
			{
				current->parent = nullptr;
				root = current;
				if (remove_branch->leftChild != nullptr)
					{
						current->leftChild = remove_branch->leftChild;
						remove_branch->leftChild->parent = current;
					}
			}

			
			

		}
		else
		{
			
			if (remove_branch->parent != nullptr)
			{
				if (remove_branch->parent->leftChild != nullptr)
				{
					remove_branch->parent->leftChild = nullptr;
				}
				else
				{
					remove_branch->parent->rightChild = nullptr;
				}
				remove_branch->parent = nullptr;
			}
			else
			{
				root = nullptr;
			}
			
			
		}
	}
	
}



template <typename T>
bool BST<T>::find(T element)
{
	Node* current = root;
	while (current->element != element)
	{
		if (current->element == element)
		{
			return true;
		}

		else if (element < current->element and current->leftChild != nullptr)
		{
			current = current->leftChild;
		}

		else if (element > current->element and current->rightChild != nullptr)
		{
			current = current->rightChild;
		}

		else 
		{
			return false;
		}
	}
	return true;
}

template <typename T>
void BST<T>::rec_find_inorder(std::vector<T>& vec, Node* sub_tree)
{
	if (sub_tree->leftChild == nullptr and sub_tree->rightChild == nullptr)
	{
		vec.push_back(sub_tree->element);
	}
	else
	{
		if (sub_tree->leftChild != nullptr)
		{
			rec_find_inorder(vec, sub_tree->leftChild);
		}
		
		vec.push_back(sub_tree->element);
		
		if (sub_tree->rightChild != nullptr)
		{
			rec_find_inorder(vec, sub_tree->rightChild);
		}



	}
}

template <typename T>
std::vector<T> BST<T>::inOrderWalk()
{
    std::vector<T> vec;
	if (root != nullptr)
	{
		rec_find_inorder(vec, root);

		return vec;
	}
	else
	{
		return vec;
	}
}


template <typename T>
std::vector<T> BST<T>::preOrderWalk()
{
	std::vector<T> vec;
	if (root != nullptr)
	{
		vec.push_back(root->element);
		rec_find_preorder(vec, root);
		return vec;
	}
	else
	{
		return vec;
	}
}


template <typename T>
void BST<T>::rec_find_postorder(std::vector<T>& vec, Node* sub_tree)
{
	if (sub_tree->leftChild != nullptr)
	{
		rec_find_postorder(vec, sub_tree->leftChild);
	}

	if (sub_tree->rightChild != nullptr)
	{
		rec_find_postorder(vec, sub_tree->rightChild);
	}

	vec.push_back(sub_tree->element);


	
}

template <typename T>
std::vector<T> BST<T>::postOrderWalk()
{
    std::vector<T> vec;
	if (root != nullptr)
	{
		rec_find_postorder(vec, root);
		return vec;
	}
	else
	{
		return vec;
	}
}

template <typename T>
int BST<T>::rec_treeheight(Node* current)
{
	if (current == nullptr)
	{
		return 0;
	}
	else
	{
		int value1 = rec_treeheight(current->leftChild);
		int value2 = rec_treeheight(current->rightChild);
		if (value1 > value2)
		{
			return 1 + value1;
		}
		else 
		{
			return 1 + value2;
		}
	}
}

template <typename T>
int BST<T>::getTreeHeight()
{
	if (root == nullptr)
	{
		return -1;
	}
	else if (root != nullptr and root->leftChild == nullptr and root->rightChild == nullptr)
	{
		return 0;
	}
	else 
	{
		return rec_treeheight(root) -1;
	}
}


template <typename T>
T BST<T>::getMin()
{
    Node* current = root;
	while (current->leftChild != nullptr)
	{
		current = current->leftChild;
	}
    return current->element;
}


template <typename T>
T BST<T>::getMax()
{
	Node* current = root;
	while (current->rightChild != nullptr)
	{
		current = current->rightChild;
	}
    return current->element;
}

template <typename T>
std::string BST<T>::ToGraphviz() // Member function of the AVLTree class
{
	std::string toReturn = "";
	if(this->root) // root is a pointer to the root node of the tree
	{
		std::string listOfNodes;
		std::string listOfConnections = std::string("\t\"Root\" -> ") + std::to_string(0) + std::string(";\n");
		toReturn += std::string("digraph {\n");
		size_t id = 0;
		ToGraphvizHelper(listOfNodes, listOfConnections, root, id);
		toReturn += listOfNodes;
		toReturn += listOfConnections;
		toReturn += std::string("}");
	}
	return toReturn;
}

template <class T>
void BST<T>::ToGraphvizHelper(std::string& listOfNodes, std::string& listOfConnections, Node* toWorkWith, size_t& uniqueID) // Member function of the AVLTree class
{
	size_t myID = uniqueID;
	listOfNodes += std::string("\t") + std::to_string(myID) + std::string(" [label=\"") + std::to_string(toWorkWith->element) + std::string("\"];\n");
	if(toWorkWith->left)
	{
		listOfConnections += std::string("\t") + std::to_string(myID) + std::string(" -> ") + std::to_string(uniqueID + 1) + std::string(" [color=blue];\n");
		ToGraphvizHelper(listOfNodes, listOfConnections, toWorkWith->left, ++uniqueID);
	}
	else
	{
		listOfNodes += std::string("\t") + std::to_string(++uniqueID) + std::string(" [label=") + std::string("nill, style = invis];\n");
		listOfConnections += std::string("\t") + std::to_string(myID) + std::string(" -> ") + std::to_string(uniqueID) + std::string(" [ style = invis];\n");
	}
			
	if(toWorkWith->right)
	{
		listOfConnections += std::string("\t") + std::to_string(myID) + std::string(" -> ") + std::to_string(uniqueID + 1) + std::string(" [color=red];\n");
		ToGraphvizHelper(listOfNodes, listOfConnections, toWorkWith->right, ++uniqueID);
	}
	else
	{
		listOfNodes += std::string("\t") + std::to_string(++uniqueID) + std::string(" [label=") + std::string("nill, style = invis];\n");
		listOfConnections += std::string("\t") + std::to_string(myID) + std::string(" -> ") + std::to_string(uniqueID) + std::string(" [ style = invis];\n");
	}
}
#endif //BST_H
