from HashTable import ChainHashMap
from FPTree import FP_Tree, Fp_node


def _ht_get(ht, key):
	v = ht.get(key)
	return v if v is not None else 0


def build_fp_tree(transactions, min_support):
	
	# Count global frequencies using HashTable
	freq = ChainHashMap()
	for tr in transactions:
		for item in tr:
			try:
				c = freq[item]
				freq[item] = c + 1
			except KeyError:
				freq[item] = 1

	frequent = {}
	for bucket in freq._table:
		if bucket is None:
			continue
		cur = bucket.head
		while cur:
			if cur.value >= min_support:
				frequent[cur.key] = cur.value
			cur = cur.next

	if not frequent:
		return None

	def sort_key(item):
		return (-frequent[item], item)

	tree = FP_Tree()

	def add_transaction_with_count(tr, count=1):
		current = tree.root
		for item in tr:
			child = current.get_child(item)
			if child:
				child.count += count
			else:
				new_node = Fp_node(item, count=count, parent=current)
				current.add_child(new_node)
				entry = tree.header_table.get(item)
				if entry:
					entry[0] += new_node.count
					entry[1].append(new_node)
					tree.header_table.put(item, entry)
				else:
					tree.header_table.put(item, [new_node.count, [new_node]])
				child = new_node
			current = child

	for tr in transactions:
		filtered = [item for item in tr if item in frequent]
		if not filtered:
			continue
		filtered.sort(key=sort_key)
		add_transaction_with_count(filtered, count=1)

	return tree


def _conditional_pattern_base(item, tree):
	"""Return list of (prefix_path_list, count) for given item from tree."""
	try:
		entry = tree.header_table[item]
	except KeyError:
		return []
	nodes = entry[1]
	patterns = []
	for node in nodes:
		count = node.count
		path = []
		parent = node.parent
		while parent and parent.value != "Root":
			path.append(parent.value)
			parent = parent.parent
		if path:
			path.reverse()
			patterns.append((path, count))
	return patterns


def build_conditional_tree(patterns, min_support):
	"""patterns: list of (path_list, count)
	returns FP_Tree or None
	"""
	freq = ChainHashMap()
	for path, cnt in patterns:
		for item in path:
			try:
				c = freq[item]
				freq[item] = c + cnt
			except KeyError:
				freq[item] = cnt

	frequent = {}
	for bucket in freq._table:
		if bucket is None:
			continue
		cur = bucket.head
		while cur:
			if cur.value >= min_support:
				frequent[cur.key] = cur.value
			cur = cur.next
	if not frequent:
		return None

	def sort_key(item):
		return (-frequent[item], item)

	tree = FP_Tree()

	for path, cnt in patterns:
		filtered = [it for it in path if it in frequent]
		if not filtered:
			continue
		filtered.sort(key=sort_key)
		current = tree.root
		for item in filtered:
			child = current.get_child(item)
			if child:
				child.count += cnt
			else:
				new_node = Fp_node(item, count=cnt, parent=current)
				current.add_child(new_node)
				entry = tree.header_table.get(item)
				if entry:
					entry[0] += new_node.count
					entry[1].append(new_node)
					tree.header_table.put(item, entry)
				else:
					tree.header_table.put(item, [new_node.count, [new_node]])
				child = new_node
			current = child

	return tree


def mine_tree(tree, min_support, prefix=None, frequent_itemsets=None):
	if prefix is None:
		prefix = []
	if frequent_itemsets is None:
		frequent_itemsets = []

	items = []
	for bucket in tree.header_table._table:
		if bucket is None:
			continue
		cur = bucket.head
		while cur:
			k = cur.key
			v = cur.value
			support = v[0] if v is not None else 0
			items.append((k, support))
			cur = cur.next

	items.sort(key=lambda x: (x[1], x[0]))

	for item, support in items:
		new_freq_set = prefix + [item]
		frequent_itemsets.append((new_freq_set, support))

		patterns = _conditional_pattern_base(item, tree)
		conditional_tree = build_conditional_tree(patterns, min_support)
		if conditional_tree:
			mine_tree(conditional_tree, min_support, new_freq_set, frequent_itemsets)

	return frequent_itemsets


def fpgrowth(transactions, min_support):
	tree = build_fp_tree(transactions, min_support)
	if not tree:
		return []
	return mine_tree(tree, min_support)




