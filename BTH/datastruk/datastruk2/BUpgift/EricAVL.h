#ifndef AVL_H
#define AVL_H

#include <vector>
#include <string>

template <class T>
class AVL
{
private:
	class Node
	{
	public:
		T element;
		Node *leftChild;
		Node *rightChild;
		Node *parent;
		int height;
		Node(T element);
		Node(T element, Node* parent);
		~Node() {};
		
	};
	Node *root = nullptr;
	void ToGraphvizHelper(std::string& listOfNodes, std::string& listOfConnections, Node* toWorkWith, size_t& uniqueID);
public:
	AVL();
	~AVL();
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
	int maxVal(int x, int y);
	void rotateRight(Node* x);
	void rotateLeft(Node* x);
	void balanceTree(Node* start);
	std::string ToGraphviz();
};
template <class T>
std::string AVL<T>::ToGraphviz() // Member function of the AVLTree class
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
void AVL<T>::ToGraphvizHelper(std::string& listOfNodes, std::string& listOfConnections, Node* toWorkWith, size_t& uniqueID) // Member function of the AVLTree class
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
inline AVL<T>::AVL()
{
	root = nullptr;
}
template<class T>
inline AVL<T>::Node::Node(T element)
{
	this->element = element;
	leftChild = nullptr;
	rightChild = nullptr;
	parent = nullptr;
	height = 0;
}
template<class T>
inline AVL<T>::Node::Node(T element, Node* parent){
	this->element = element;
	leftChild = nullptr;
	rightChild = nullptr;
	this->parent = parent;
	height = 0;
}
template<class T>
inline AVL<T>::~AVL()
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
inline void AVL<T>::insert(T element)
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
				parent->leftChild = new Node(element, parent);
			}
			else {
				parent->rightChild = new Node(element, parent);
			}
		}
		Node* temparent = parent;
		while (temparent != nullptr) {
			temparent->height = 1 + maxVal(getThatHeightBoi(temparent->leftChild), getThatHeightBoi(temparent->rightChild));
			temparent = temparent->parent;
		}
		balanceTree(parent);
	}
}

template<class T>
inline void AVL<T>::childTracker(std::vector<Node *>& vec, Node* subtree){
	if (subtree != nullptr) {
		childTracker(vec, subtree->leftChild);
		vec.push_back(subtree);
		childTracker(vec, subtree->rightChild);
	}
}

template<class T>
void AVL<T>::recurseInorder(std::vector<T>& vec, Node* subtree){
	if (subtree != nullptr) {
		recurseInorder(vec, subtree->leftChild);
		vec.push_back(subtree->element);
		recurseInorder(vec, subtree->rightChild);
	}
}

template<class T>
void AVL<T>::recursePreorder(std::vector<T>& vec, Node* subtree){
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
void AVL<T>::recursePostorder(std::vector<T>& vec, Node* subtree){
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
inline auto AVL<T>::getMinNode(Node* current) {
	while (current->leftChild != nullptr) {
		current = current->leftChild;
	}
	return current;
}

template<class T>
inline void AVL<T>::remove(T element)
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
			balanceTree(parent);
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
			balanceTree(parent);
		}
	}
}
template<class T>
inline bool AVL<T>::find(T element)
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
inline std::vector<T> AVL<T>::inOrderWalk()
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
inline std::vector<T> AVL<T>::preOrderWalk()
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
inline std::vector<T> AVL<T>::postOrderWalk()
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
inline int AVL<T>::getThatHeightBoi(Node* subtree)
{
	if (subtree == nullptr){
		return -1;
	}
	else {
		return subtree->height;
	}
}
template<class T>
inline int AVL<T>::getTreeHeight()
{
	Node* heightptr = root;
	return getThatHeightBoi(heightptr);
}
template<class T>
inline T AVL<T>::getMin()
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
inline T AVL<T>::getMax()
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
template<class T>
int AVL<T>::maxVal(int x, int y) {
    return (x > y)? x : y;
}
template<class T>
void AVL<T>::rotateRight(Node* x) {
	Node* y = x->leftChild;
	Node* parent = x->parent;
	Node* swap = x->leftChild->rightChild;
	if (x == root) {
		root = y;
		y->parent = nullptr;
	}
	else if (parent->rightChild == x) {
		parent->rightChild = y;
		y->parent = parent;
	}
	else {
		parent->leftChild = y;
		y->parent = parent;
	}
	swap = y->rightChild;
	y->rightChild = x;
	if (swap != nullptr) {
		swap->parent = x;
	}
	x->parent = y;
	x->leftChild = swap;

    x->height = maxVal(getThatHeightBoi(x->leftChild), getThatHeightBoi(x->rightChild)) + 1;
	y->height = maxVal(getThatHeightBoi(y->leftChild), getThatHeightBoi(y->rightChild)) + 1;
}
template<class T>
void AVL<T>::rotateLeft(Node* x) {
	Node* y = x->rightChild;
	Node* parent = x->parent;
	Node* swap = x->rightChild->leftChild;
	if (x == root) {
		root = y;
		y->parent = nullptr;
	}
	else if (parent->leftChild == x) {
		parent->leftChild = y;
		y->parent = parent;
	}
	else {
		parent->rightChild = y;
		y->parent = parent;
	}
	swap = y->leftChild;
	y->leftChild = x;
	if (swap != nullptr) {
		swap->parent = x;
	}
	x->parent = y;
	x->rightChild = swap;

	x->height = maxVal(getThatHeightBoi(x->leftChild), getThatHeightBoi(x->rightChild)) + 1;
	y->height = maxVal(getThatHeightBoi(y->leftChild), getThatHeightBoi(y->rightChild)) + 1;
}
template<class T>
void AVL<T>::balanceTree(Node* start) {
	if (start != nullptr) {
		start->height = maxVal(getThatHeightBoi(start->leftChild), getThatHeightBoi(start->rightChild)) + 1;
		if (start->leftChild != nullptr or start->rightChild != nullptr) {
			if (getThatHeightBoi(start->leftChild) - getThatHeightBoi(start->rightChild) >= 2) { //left child is LARGE
				if (getThatHeightBoi(start->leftChild->leftChild) < getThatHeightBoi(start->leftChild->rightChild)) { //inner right is greater than inner left
					rotateLeft(start->leftChild);
				}
				rotateRight(start);
			}
			else if(getThatHeightBoi(start->rightChild) - getThatHeightBoi(start->leftChild) >= 2) { //right child is LARGE
				if (getThatHeightBoi(start->rightChild->rightChild) < getThatHeightBoi(start->rightChild->leftChild)) { //inner left is greater than inner right
					rotateRight(start->rightChild);
				}
				rotateLeft(start);
			}
		}
		balanceTree(start->parent);
	}
}

#endif //AVL_H
