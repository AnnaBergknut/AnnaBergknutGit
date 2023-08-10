#ifndef BST_H
#define BST_H

#include <vector>
#include <string>

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
		Node(T element);
		~Node() {};
	};

	Node *root = nullptr;
	void ToGraphvizHelper(std::string& listOfNodes, std::string& listOfConnections, Node* toWorkWith, size_t& uniqueID);
public:
	BST();
	~BST();
	void insert(T element);
	void childTracker(std::vector<Node *>& vec, Node* subtree);
	void recurseInorder(std::vector<T>& vec, Node* subtree);
	void recursePreorder(std::vector<T>& vec, Node* subtree);
	void recursePostorder(std::vector<T>& vec, Node* subtree);
	auto getMinNode(Node* current);
	void remove(T element);
	bool find(T element);
	std::vector<T> inOrderWalk();
	std::vector<T> preOrderWalk();
	std::vector<T> postOrderWalk();
	int getThatHeightBoi(Node* subtree);
	int getTreeHeight();
	T getMin();
	T getMax();
	std::string ToGraphviz();
};
template <class T>
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
	if(toWorkWith->leftChild)
	{
		listOfConnections += std::string("\t") + std::to_string(myID) + std::string(" -> ") + std::to_string(uniqueID + 1) + std::string(" [color=blue];\n");
		ToGraphvizHelper(listOfNodes, listOfConnections, toWorkWith->leftChild, ++uniqueID);
	}
	else
	{
		listOfNodes += std::string("\t") + std::to_string(++uniqueID) + std::string(" [label=") + std::string("nill, style = invis];\n");
		listOfConnections += std::string("\t") + std::to_string(myID) + std::string(" -> ") + std::to_string(uniqueID) + std::string(" [ style = invis];\n");
	}
			
	if(toWorkWith->rightChild)
	{
		listOfConnections += std::string("\t") + std::to_string(myID) + std::string(" -> ") + std::to_string(uniqueID + 1) + std::string(" [color=red];\n");
		ToGraphvizHelper(listOfNodes, listOfConnections, toWorkWith->rightChild, ++uniqueID);
	}
	else
	{
		listOfNodes += std::string("\t") + std::to_string(++uniqueID) + std::string(" [label=") + std::string("nill, style = invis];\n");
		listOfConnections += std::string("\t") + std::to_string(myID) + std::string(" -> ") + std::to_string(uniqueID) + std::string(" [ style = invis];\n");
	}
}
template<class T>
inline BST<T>::BST()
{
	root = nullptr;
}
template<class T>
inline BST<T>::Node::Node(T element)
{
	this->element = element;
	leftChild = nullptr;
	rightChild = nullptr;
}
template<class T>
inline BST<T>::~BST()
{
	Node* killer = root;
	std::vector<Node*> vec;
	childTracker(vec, killer);
	for (Node* i : vec){
		delete i;
	}
	root = nullptr;
}
template<class T>
inline void BST<T>::insert(T element)
{
	if (root == nullptr) {
		root = new Node(element);
	}
	else {
		Node* current = root;
		Node* parent = nullptr;
		while (current != nullptr and element != current->element) {
			parent = current;
			if (element < current->element) {
				current = current->leftChild;
			}
			else {
				current = current->rightChild;
			}
		}
		if (parent != nullptr and current == nullptr) {
			if (element < parent->element) {
				parent->leftChild = new Node(element);
			}
			else {
				parent->rightChild = new Node(element);
			}
		}
	}
}

template<class T>
inline void BST<T>::childTracker(std::vector<Node *>& vec, Node* subtree){
	if (subtree != nullptr) {
		childTracker(vec, subtree->leftChild);
		vec.push_back(subtree);
		childTracker(vec, subtree->rightChild);
	}
}

template<class T>
inline void BST<T>::recurseInorder(std::vector<T>& vec, Node* subtree){
	if (subtree != nullptr) {
		recurseInorder(vec, subtree->leftChild);
		vec.push_back(subtree->element);
		recurseInorder(vec, subtree->rightChild);
	}
}

template<class T>
inline void BST<T>::recursePreorder(std::vector<T>& vec, Node* subtree){
	if (subtree->leftChild != nullptr){
		vec.push_back(subtree->leftChild->element);
		recursePreorder(vec, subtree->leftChild);
	}
	if (subtree->rightChild != nullptr){
		vec.push_back(subtree->rightChild->element);
		recursePreorder(vec, subtree->rightChild);
	}
}

template<class T>
inline void BST<T>::recursePostorder(std::vector<T>& vec, Node* subtree){
	if (subtree->leftChild != nullptr){
		recursePostorder(vec, subtree->leftChild);
		vec.push_back(subtree->leftChild->element);
	}
	if (subtree->rightChild != nullptr){
		recursePostorder(vec, subtree->rightChild);
		vec.push_back(subtree->rightChild->element);
	}
}

template<class T>
inline auto BST<T>::getMinNode(Node* current) {
	while (current->leftChild != nullptr) {
		current = current->leftChild;
	}
	return current;
}

template<class T>
inline void BST<T>::remove(T element)
{
	if (root != nullptr) {	
		Node* parent = nullptr;
		Node* remove_branch = root;
		while (remove_branch->element != element and remove_branch != nullptr) {
			parent = remove_branch;
			if (element < remove_branch->element) {
				remove_branch = remove_branch->leftChild;
			}
			else {
				remove_branch = remove_branch->rightChild;
			}
		}

		if (remove_branch->leftChild == nullptr and remove_branch->rightChild == nullptr) {
			if (remove_branch != root) {
				if (parent->leftChild == remove_branch) {
					parent->leftChild = nullptr;
				}
				else {
					parent->rightChild = nullptr;
				}
			}
			else {
				root = nullptr;
			}
			delete remove_branch;
		}
		else if (remove_branch->leftChild and remove_branch->rightChild){
			Node* next = getMinNode(remove_branch->rightChild);
			int value = next->element;
			remove(next->element);
			remove_branch->element = value;
		}
		else {
			Node* next = (remove_branch->leftChild)? remove_branch->leftChild: remove_branch->rightChild;
			if (remove_branch != root) {
				if (remove_branch == parent->leftChild) {
					parent->leftChild = next;
				}
				else {
					parent->rightChild = next;
				}
			}
			else {
				root = next;
			}
			delete remove_branch;
		}
	}
}

template<class T>
inline bool BST<T>::find(T element)
{
	if (root == nullptr) {
		return false;
	}
	Node* finder = root;
	while (finder->element != element) {
		if (element < finder->element and finder->leftChild != nullptr) {
			finder = finder->leftChild;
		}
		else if (element > finder->element and finder->rightChild != nullptr) {
			finder = finder->rightChild;
		}
		else if (element == finder->element) {
			return true;
		}
		else return false;
	}
	return true;
}
template<class T>
inline std::vector<T> BST<T>::inOrderWalk()
{
	if (root == nullptr) {
		return std::vector<T>();
	}
	Node* order = root;
	std::vector<T> vec;
	recurseInorder(vec, order);
	return vec;
}
template<class T>
inline std::vector<T> BST<T>::preOrderWalk()
{
	if (root == nullptr) {
		return std::vector<T>();
	}
	Node* order = root;
	std::vector<T> vec;
	vec.push_back(order->element);
	recursePreorder(vec, order);
	return vec;
}
template<class T>
inline std::vector<T> BST<T>::postOrderWalk()
{	
	if (root == nullptr) {
		return std::vector<T>();
	}
	Node* order = root;
	std::vector<T> vec;
	recursePostorder(vec, order);
	vec.push_back(order->element);
	return vec;
}
template<class T>
inline int BST<T>::getThatHeightBoi(Node* subtree)
{
	if (subtree == nullptr){
		return 0;
	}
	else {
		int left;
		int right;
		left = getThatHeightBoi(subtree->leftChild);
		right = getThatHeightBoi(subtree->rightChild);
		if (left > right) {
			return left + 1;
		}
		else {
			return right + 1;
		}
	}
}
template<class T>
inline int BST<T>::getTreeHeight()
{
	Node* heightptr = root;
	return getThatHeightBoi(heightptr) - 1;
}
template<class T>
inline T BST<T>::getMin()
{
	Node* minptr = root;
	while (minptr != nullptr) {
		if (minptr->leftChild != nullptr) {
			minptr = minptr->leftChild;
		}
		else {
			return minptr->element;
		}
	}
	return -1;
}
template<class T>
inline T BST<T>::getMax()
{
	Node* maxptr = root;
	while (maxptr != nullptr) {
		if (maxptr->rightChild != nullptr) {
			maxptr = maxptr->rightChild;
		}
		else {
			return maxptr->element;
		}
	}
	return -1;
}
#endif //BST_H
