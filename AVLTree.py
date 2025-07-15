#name1: itay mutzafi

#username1: itaymutzafi@mail.tau.ac.il

#name2: aya rotbart

#username2: ayarotbart@mail.tau.ac.il

"""A class represnting a node in an AVL tree"""
import math

class AVLNode(object):

	"""Constructor, you are allowed to add more fields.

	@type key: int

	@param key: key of your node

	@type value: string

	@param value: data of your node

	"""

	def __init__(self, key=None, value=None, is_real = True):

		self.key = key

		self.value = value

		self.left = None

		self.right= None

		self.parent = None

		self.height = -1

		self.is_real = is_real

		if is_real:
			self.left = AVLNode(is_real=False)
			self.left.parent = self
			self.right = AVLNode(is_real=False)
			self.right.parent = self

	"""returns whether self is not a virtual node 

	@rtype: bool

	@returns: False if self is a virtual node, True otherwise.

	"""

	def is_real_node(self):
		return self.is_real

"""

A class implementing an AVL tree.

"""

class AVLTree(object):



	"""

	Constructor, you are allowed to add more fields.

	"""

	def __init__(self):
		self.root = None
		self.size = 0
		self.max_node = AVLNode(key = -math.inf, is_real= False)


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        

	@type key: int

	@param key: a key to be searched

	@rtype: (AVLNode,int)

	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),

	and e is the number of edges on the path between the starting node and ending node+1.

	"""

	def search(self, key):  #Complexity - O(logn)

		e = 1 #count the length of search route.

		node = self.root

		while node.is_real_node() :

			if node.key == key:

				return node, e

			elif node.key < key:

				node = node.right

				e +=1

			elif node.key > key:

				node = node.left

				e +=1

		return None,e

	"""
	"searches for a node in the dictionary corresponding to the key, starting at the max

	@type key: int

	@param key: a key to be searched

	@rtype: (AVLNode,int)

	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),

	and e is the number of edges on the path between the starting node and ending node+1.

	"""

	def finger_search(self, key):

		if self.root is None:
			return None, 1

		if key <= self.root.key: #if node is in left subtree - do regular search
			return self.search(key)

		#else - search for key in the right subtree

		node = self.max_node

		e = 1

		while node.key > key and node.parent is not None: #search for the first key that is smaller than key

			node = node.parent

			e+=1

		#search the key, beginning the node we found

		while node.key != key and node.is_real_node():

			if node.key < key:

				node = node.right

				e +=1

			if node.key > key:

				node = node.left

				e +=1

		return node, e 


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)



	@type key: int

	@pre: key currently does not appear in the dictionary

	@param key: key of item that is to be inserted to self

	@type val: string

	@param val: the value of the item

	@rtype: (AVLNode,int,int)

	@returns: a 3-tuple (x,e,h) where x is the new node,

	e is the number of edges on the path between the starting node and new node before rebalancing,

	and h is the number of PROMOTE cases during the AVL rebalancing

	"""

	def insert(self, key, val):  #Complexity - O(logn)

		if self.root is None:
			self.root = AVLNode(key,val)
			self.root.height += 1
			self.max_node = self.root
			self.size +=1
			return self.root,0,0

		new_node = AVLNode(key, val)
		e=0
		h=0
		node = self.root
		parent = None

		while node.is_real_node(): #find the place of the new node
			parent = node
			if node.key > key:
				node = node.left
			else:
				node = node.right
			e+=1

		if not parent:
			self.root = AVLNode(key, val)
			self.root.height += 1
			self.max_node = self.root
			self.size += 1
			return self.root, 0, 0


		if parent and parent.key < key:
			parent.right = new_node
			new_node.parent = parent
		else:
			parent.left = new_node
			new_node.parent = parent  # initilized new node's parent

		new_node.height += 1
		h = self.rebalance(new_node,h)

		self.size +=1

		search_max = self.root
		while search_max.right.is_real_node():
			search_max = search_max.right

		self.max_node = search_max

		return new_node,e,h

	def rebalance(self, node, h): #O(logn)
		while node.parent is not None:  # node inserted
			bf = node.parent.left.height - node.parent.right.height

			tmp_h = node.parent.height

			node.parent.height = 1 + max(node.parent.left.height,node.parent.right.height)  # update node.parent height if needed

			if tmp_h == node.parent.height:

				break  # terminate

			if abs(bf) < 2:  # my height changed and bf is legal

				node = node.parent

				h += 1

				continue

			# node.parent height has changed and BF is ilegal
			if bf > 1:  # left child height is greater than right child
				node = node.parent.left
				node_bf = node.left.height - node.right.height
				if node_bf >= 0:  # single_rotate
					self.rotate_left(node, node.parent)
				else:  # double_rotate
					x = self.rotate_right(node.right, node)
					self.rotate_left(x, x.parent)

			if bf < -1:
				node = node.parent.right
				node_bf = node.left.height - node.right.height
				if node_bf <= 0:  # single_rotate
					self.rotate_right(node, node.parent)

				else:  # double_rotate
					x = self.rotate_left(node.left, node)
					self.rotate_right(x, x.parent)

		return h

	def rotate_left(self,bottom,top):
		bottom_right = bottom.right
		newparent_bottom = top.parent
		bottom.right = top
		top.left = bottom_right
		bottom_right.parent = top
		top.parent = bottom
		bottom.parent = newparent_bottom

		if bottom.parent is None:
			self.root = bottom
			top.height = 1 + max(top.left.height, top.right.height)
			bottom.height = 1 + max(bottom.left.height, bottom.right.height)
			return bottom

		else:
			if bottom.key < bottom.parent.key:
				bottom.parent.left = bottom
			else:
				bottom.parent.right = bottom

		top.height = 1 + max(top.left.height, top.right.height)
		bottom.height = 1 + max(bottom.left.height, bottom.right.height)
		bottom.parent.height = 1 + max(bottom.parent.left.height, bottom.parent.right.height)
		return bottom

	def rotate_right(self,bottom,top):
		bottom_left = bottom.left
		newparent_bottom = top.parent
		bottom.left = top
		top.right = bottom_left
		top.parent = bottom

		bottom_left.parent = top

		bottom.parent = newparent_bottom

		if bottom.parent is None:
			self.root = bottom
			top.height = 1 + max(top.left.height, top.right.height)
			bottom.height = 1 + max(bottom.left.height, bottom.right.height)
			return bottom
		else:
			if bottom.key < bottom.parent.key:
				bottom.parent.left = bottom
			else:
				bottom.parent.right = bottom

		top.height = 1 + max(top.left.height, top.right.height)
		bottom.height = 1 + max(bottom.left.height, bottom.right.height)
		bottom.parent.height = 1 + max(bottom.parent.left.height, bottom.parent.right.height)

		return bottom



	

	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int

	@pre: key currently does not appear in the dictionary

	@param key: key of item that is to be inserted to self

	@type val: string

	@param val: the value of the item

	@rtype: (AVLNode,int,int)

	@returns: a 3-tuple (x,e,h) where x is the new node,

	e is the number of edges on the path between the starting node and new node before rebalancing,

	and h is the number of PROMOTE cases during the AVL rebalancing

	"""

	def finger_insert(self, key, val):

		new_node = AVLNode(key, val)
		new_node.height += 1
		if self.root is None:
			self.root =  new_node
			self.max_node = new_node
			self.size+=1
			return self.root,0,0

		if key <= self.root.key:
			return self.insert(key,val)

		parent = None
		e = 0
		h = 0
		node = self.max_node
		if new_node.key > node.key: #new node is the new max
			node.right = new_node
			new_node.parent = node
			self.max_node = new_node
			h = self.rebalance(new_node, h)
			return new_node, 0,h

		while node.key > key and node.parent is not None: #search for the first key that is smaller than key
			node = node.parent
			e+=1

		#search the key, beginning the node we found
		while node.is_real_node():
			parent = node
			if node.key < key:
				node = node.right
				e +=1
			else:
				node = node.left
				e +=1



		if parent and parent.key < key:
			parent.right = new_node
			new_node.parent = parent  # initilized new node's parent
			h = self.rebalance(parent.right, h)

		else:
			parent.left = new_node
			new_node.parent = parent  # initilized new node's parent
			h = self.rebalance(parent.left, h)

		search_max = self.root
		while search_max.right.is_real_node():
			search_max = search_max.right
		self.max_node = search_max
		self.size += 1


		return new_node, e, h




	"""deletes node from the dictionary

	@type node: AVLNode

	@pre: node is a real pointer to a node in self

	"""

	# Complexity - O(logn)
	def delete(self, node):
		parent = node.parent
		if node.height == 0:
			self.delete_leaf(node)
		elif not (node.left.is_real_node()) and (node.right.is_real_node()):  # node has only right child -bypass it
			self.delete_right_unary_node(node)
		elif not (node.right.is_real_node()) and (node.left.is_real_node()):  # node has only left child -bypass it
			self.delete_left_unary_node(node)
		else:
			suc = self.successor(node)
			parent = suc.parent
			self.delete_binary_node(node)

		while parent is not None:  # rotate or demote
			bf = parent.left.height - parent.right.height
			prev_height = parent.height
			parent.height = 1 + max(parent.left.height, parent.right.height)
			if abs(bf) < 2 and prev_height == parent.height:
				parent = parent.parent
				continue
			else:
				if abs(bf) < 2 and prev_height != parent.height:
					parent = parent.parent
					continue
				else:
					if bf > 1:  # left child's height is greather then right child
						if parent.left.is_real_node():
							node_bf = parent.left.left.height - parent.left.right.height
							if node_bf == -1:  # single_rotate
								self.rotate_right(parent.left.right, parent.left)
								self.rotate_left(parent.left, parent)
							else:  # double_rotate
								self.rotate_left(parent.left, parent)
						else:
							self.rotate_left(parent.left, parent)
						parent.height = 1 + max(parent.left.height, parent.right.height)

					if bf < -1:
						if parent.right.is_real_node():
							node_bf = parent.right.left.height - parent.right.right.height
							if node_bf == 1:  # double_rotate
								self.rotate_left(parent.right.left, parent.right)
								self.rotate_right(parent.right, parent)

							else:  # single_rotate
								self.rotate_right(parent.right, parent)
						else:
							self.rotate_right(parent.right, parent)
						parent.height = 1 + max(parent.left.height, parent.right.height)


		search_max = self.root
		while search_max is not None and search_max.right.is_real_node():
			search_max = search_max.right
		self.max_node = search_max


	def delete_binary_node(self,node):
		suc = self.successor(node)
		node.value = suc.value  # replace node with its successor
		node.key = suc.key  # keep a pointer to the parent of the physical deleted node
		if suc.height == 0:
			self.delete_leaf(suc)
		else:
			self.delete_right_unary_node(suc)
		return self

	def delete_right_unary_node(self,node):
		if node is self.root:
			self.root = node.right
			node.right.parent = None
			node.right = AVLNode()
			self.max_node = self.root
			node.height = 1 + max(node.left.height, node.right.height)
			self.size -=1
			return self
		if not (node.left.is_real_node()) and (node.right.is_real_node()):  # node has only right child -bypass it
			if node.parent is None:
				self.root = node.right
				node.right.parent = None
				node.height = 1 + max(node.left.height, node.right.height)
			else:
				parent = node.parent
				if parent.left is node:   # node is the left child
					parent.left = node.right
					parent.left.parent = parent
				elif parent.right is node:  # node is the right child
					parent.right = node.right
					parent.right.parent = parent
				p2 = parent.parent
				while p2 is not None:
					p2.height = 1 + max(p2.left.height, p2.right.height)
					p2 = p2.parent
				parent.height = 1 + max(parent.left.height, parent.right.height)
		self.size -=1
		return self

	#O(logn)
	def delete_left_unary_node(self,node): #node has only left child, bypass it
		if node is self.root:
			self.root = node.left
			node.left.parent = None
			node.left = AVLNode()
			#self.max_node = self.root
			self.size -= 1
			node.height = 1 + max(node.left.height, node.right.height)
			return self
		else:
			parent = node.parent
			if parent.left is node:  # node is the left child
				parent.left = node.left
				parent.left.parent = parent
			elif parent.right is node:  # node is the right child
				parent.right = node.left
				parent.right.parent = parent
			parent.height = 1 + max(parent.left.height,parent.right.height)
			p2 = parent.parent
			while p2 is not None:
				p2.height = 1 + max(p2.left.height, p2.right.height)
				p2 = p2.parent
		self.size -= 1
		return self

	#O(logn)
	def delete_leaf(self,node):
		if node is self.root:
			self.root = None
			self.size = 0
			self.max_node = AVLNode(is_real=False, key = -math.inf)
			return self
		else:
			parent = node.parent
			if parent.left is node:  # node is the left child
				parent.left = AVLNode(None, None, is_real=False)  # delete node and terminate
				parent.left.parent = parent

			elif parent.right is node:
				parent.right = AVLNode(None, None, is_real=False)  # delete node and terminate
				parent.right.parent = parent
			parent.height = 1 + max(parent.left.height, parent.right.height)

		p2 = parent.parent
		while p2 is not None:
			p2.height = 1 + max(p2.left.height, p2.right.height)
			p2 = p2.parent

		self.size -=1
		return self

	#O(logn)
	def successor(self, node):
		if node.right.is_real_node():
			node = node.right
			while node.left.is_real_node():
				node = node.left
			return node
		else:
			while node.parent != None:
				if node.key < node.parent.key:
					return node.parent
				node = node.parent
			return node

	"""joins self with item and another AVLTree

	@type tree2: AVLTree 

	@param tree2: a dictionary to be joined with self

	@type key: int 

	@param key: the key separting self and tree2

	@type val: string

	@param val: the value corresponding to key

	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,

	or the opposite way

	"""
	#Comlexity O(height(t1)-height(t2)+1)
	def join(self, tree2, key, val):
		if tree2.root is None and self.root is None:
			self.insert(key,val)
			return self
		if self.root is None:
			self.root = tree2.root
			self.size = tree2.size
			self.insert(key,val)
			return self
		if tree2.root is None:
			self.insert(key, val)
			return self
		new_node = AVLNode(key, val)
		new_node.height+=1
		h_og = self.root.height
		h_add = tree2.root.height
		node1 = self.root
		node2 = tree2.get_root()
		node1_pointer = self.root #keep a pointer to the root to later update
		node2_pointer = tree2.get_root()  # keep a pointer to the root to later update
		self.size += 1 + tree2.size

		if node1.key < node2.key: #tree2 is greater then self
			self.max_node = tree2.max_node
			if h_add > h_og: #tree2 height is greater then self
				while node2.is_real_node() and node2.height > h_og:
					node2 = node2.left
				parent = node2.parent #change to pointers to connect the trees
				new_node.right = node2
				node2.parent = new_node
				new_node.left = node1
				node1.parent = new_node
				new_node.parent = parent
				if parent is not None:
					parent.left = new_node
				self.root = node2_pointer
				new_node.height = 1 + max(new_node.right.height,new_node.left.height)
				while parent is not None:
					bf = parent.left.height - parent.right.height
					parent.height = 1 + max(parent.left.height,parent.right.height)  # update node.parent height if needed
					if bf > 1:  # left child height is greater then right child
						node_bf = parent.left.left.height - parent.left.right.height
						if node_bf == 0:  # single_rotate
							self.rotate_left(parent.left,parent)
							parent = parent.parent
						elif node_bf == 1:
							self.rotate_left(parent.left,parent)
						else:  # double_rotate
							x = self.rotate_right(parent.left.right, parent.left)
							self.rotate_left(x, x.parent)
					elif bf < -1:
						node_bf = parent.right.left.height - parent.right.right.height
						if node_bf == 0:  # single_rotate
							self.rotate_right(parent.right, parent)
							parent = parent.parent
						elif node_bf == -1:
							self.rotate_right(parent.right, parent)
						else:  # double_rotate
							x = self.rotate_left(parent.right.left,parent.right)
							self.rotate_right(x, x.parent)
					else:
						parent = parent.parent



			elif h_add < h_og:
				while node1.is_real_node() and node1.height > h_add: #find the root of the subtree in the same height
					node1 = node1.right
				parent = node1.parent #preforme the pointers change to conecct the trees
				new_node.left = node1
				node1.parent = new_node
				new_node.right = node2
				node2.parent = new_node
				new_node.parent = parent
				if parent is not None:
					parent.right = new_node
				self.root = node1_pointer
				new_node.height = 1 + max(new_node.right.height,new_node.left.height)
				while parent is not None:
					bf = parent.left.height - parent.right.height
					parent.height = 1 + max(parent.left.height,parent.right.height)  # update node.parent height if needed
					if bf > 1:  # left child height is greather then right child
						node_bf = parent.left.left.height - parent.left.right.height
						if node_bf == 0:  # single_rotate
							self.rotate_left(parent.left,parent)
							parent = parent.parent
						elif node_bf == 1:
							self.rotate_left(parent.left,parent)
						else:  # double_rotate
							x = self.rotate_right(parent.left.right, parent.left)
							self.rotate_left(x, x.parent)
					elif bf < -1:
						node_bf = parent.right.left.height - parent.right.right.height
						if node_bf == 0:  # single_rotate
							self.rotate_right(parent.right, parent)
							parent = parent.parent
						elif node_bf == -1:
							self.rotate_right(parent.right, parent)
						else:  # double_rotate
							x = self.rotate_left(parent.right.left,parent.right)
							self.rotate_right(x, x.parent)
					else:
						parent = parent.parent #the problem is solved or moved up




			elif h_add == h_og: #case when only need to connect the two trees
				new_node.right = node2
				node2.parent = new_node
				new_node.left = node1
				node1.parent = new_node
				self.root = new_node
				new_node.height = 1 + max(new_node.right.height, new_node.left.height)
				#tree2.root = None


		else:
			if h_add > h_og: #tree2 height is greater then self
				while node2.is_real_node() and node2.height > h_og:
					node2 = node2.right
				parent = node2.parent
				new_node.left = node2
				node2.parent = new_node
				new_node.right = node1
				node1.parent = new_node
				new_node.parent = parent
				if parent:
					parent.right = new_node
				self.root = node2_pointer
				new_node.height = 1 + max(new_node.right.height,new_node.left.height)
				while parent is not None:
					bf = parent.left.height - parent.right.height
					parent.height = 1 + max(parent.left.height,parent.right.height)  # update node.parent height if needed
					if bf > 1:  # left child height is greather then right child
						node_bf = parent.left.left.height - parent.left.right.height
						if node_bf == 0:  # single_rotate
							self.rotate_left(parent.left,parent)
							parent = parent.parent
						elif node_bf == 1:
							self.rotate_left(parent.left,parent)
						else:  # double_rotate
							x = self.rotate_right(parent.left.right, parent.left) #לא בטוחה
							self.rotate_left(x, x.parent)
					elif bf < -1:
						node_bf = parent.right.left.height - parent.right.right.height
						if node_bf == 0:  # single_rotate
							self.rotate_right(parent.right, parent)
							parent = parent.parent
						elif node_bf == -1:
							self.rotate_right(parent.right, parent)
						else:  # double_rotate
							x = self.rotate_left(parent.right.left,parent.right)
							self.rotate_right(x, x.parent)
					else:
						parent = parent.parent


			elif h_add < h_og:
				while node1.is_real_node() and node1.height > h_add: #find the root of the subtree in the same height
					node1 = node1.left
				parent = node1.parent #preforme the pointers change to conecct the trees
				new_node.right = node1
				node1.parent = new_node
				new_node.left = node2
				node2.parent = new_node
				new_node.parent = parent
				if parent is not None:
					parent.left = new_node
				self.root = node1_pointer
				new_node.height = 1 + max(new_node.right.height,new_node.left.height)
				while parent is not None:
					bf = parent.left.height - parent.right.height
					parent.height = 1 + max(parent.left.height,parent.right.height)  # update node.parent height if needed
					if bf > 1:  # left child height is greather then right child
						node_bf = parent.left.left.height - parent.left.right.height
						if node_bf == 0:  # single_rotate
							self.rotate_left(parent.left,parent)
							parent = parent.parent
						elif node_bf == 1:
							self.rotate_left(parent.left,parent)
						else:  # double_rotate
							x = self.rotate_right(parent.left.right, parent.left)
							self.rotate_left(x, x.parent)
					elif bf < -1:
						node_bf = parent.right.left.height - parent.right.right.height
						if node_bf == 0:  # single_rotate
							self.rotate_right(parent.right, parent)
							parent = parent.parent
						elif node_bf == -1:
							self.rotate_right(parent.right, parent)
						else:  # double_rotate
							x = self.rotate_left(parent.right.left,parent.right)
							self.rotate_right(x, x.parent)
					else:
						parent = parent.parent #the problem is solved or moved up



			elif h_add == h_og: #case when only need to connect the two trees
				new_node.right = node1
				node1.parent = new_node
				new_node.left = node2
				node2.parent = new_node
				self.root = new_node
				new_node.height = 1 + max(new_node.right.height, new_node.left.height)
				tree2.root = None


		search_max = self.root
		while search_max is not None and search_max.right.is_real_node():
			search_max = search_max.right
		self.max_node = search_max
		return self


	"""splits the dictionary at a given node

	@type node: AVLNode

	@pre: node is in self 

	@param node: the node in the dictionary to be used for the split

	@rtype: (AVLTree, AVLTree)

	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 

	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 

	dictionary larger than node.key.

	"""
	#O(logn)
	def split(self, node):

		l_tree = AVLTree()
		r_tree = AVLTree()
		new_tree = AVLTree()

		if self.root.height == 0 and node is self.root: #the tree is empty
			self.root = None
			return l_tree, r_tree

		if node.left.is_real_node(): #node has left child
			l_tree.root = node.left
			l_tree.root.parent = None
			l_tree.max_node = l_tree.root

		if node.right.is_real_node(): #node has right child
			r_tree.root = node.right
			r_tree.root.parent = None
			r_tree.max_node = r_tree.root

		while node.parent is not None:

			if node.parent.right is node:
				if node.parent.left.is_real_node():
					new_tree.root = node.parent.left
					new_tree.root.parent = None
				l_tree.join(new_tree,node.parent.key,node.parent.value)
			else:
				if  node.parent.right.is_real_node():
					new_tree.root = node.parent.right
					new_tree.root.parent = None
				r_tree.join(new_tree,node.parent.key,node.parent.value)

			node = node.parent

		l_max = l_tree.root
		while l_max and l_max.right.is_real_node():
			l_max = l_max.right
		l_tree.max_node = l_max

		r_max = r_tree.root
		while r_max and r_max.right.is_real_node():
			r_max = r_max.right
		r_tree.max_node = r_max

		return l_tree, r_tree


	"""returns an array representing dictionary 

	@rtype: list

	@returns: a sorted list according to key of touples (key, value) representing the data structure

	"""

	# O(n)
	def avl_to_array(self):
		if self.root is None:
			return []
		arr = []
		return self.in_order(self.root,arr)

	#O(n)
	def in_order(self,node, L):
		if node.is_real_node():
			self.in_order(node.left,L)
			L.append((node.key, node.value))
			self.in_order(node.right,L)
		return L

	"""in order scans all Treenode, O(n)""" 



	"""returns the node with the maximal key in the dictionary



	@rtype: AVLNode

	@returns: the maximal node, None if the dictionary is empty

	"""
	#O(1)
	def max_node(self):
		return self.max_node

	"""returns the number of items in dictionary 

	@rtype: int

	@returns: the number of items in dictionary 

	"""

	# O(1)
	def size(self):
		return self.size

	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode

	@returns: the root, None if the dictionary is empty

	"""

	def get_root(self):
		return self.root
