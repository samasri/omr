# Algorithm to create the `Hierarchy` vector 
Input: _child class name_, _parent class name_ (such that the child passed extends the parent passed)

Output: none (edits the `Hierarchy` list with the appropriate additions)

Search for child and parent in the address map
1. If child is found:
			Create new node
			Link the new node to the found child (child->newNode)
			Add newNode to the address map
2. If parent is found:
* Create new node
* Link the new node to the found parent (newNode->parent)
* Do a search on all Hierarchies and change the base of the right Hierarchy to the new one (which we just added)
* Add child to the address map
3. If neither child nor parent are found:
* Create 2 new nodes (the child and the parent)
* Link them together
* Add them to the address map
* Add them to a new hierarchy
* Add the new hierarchy to the hierarchy list
4. If both child and parent are found:
* Link child to parent
* Check if parent was a base of a hierarchy, delete that hierarchy