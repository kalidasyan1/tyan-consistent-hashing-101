import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = dict()           # hash value -> (node_name, replica_index)
        self.sorted_keys = []        # sorted hash values (ints)
        self.node_set = set()        # set of physical node names for deduplication
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % (2**16)
    
    def add_node(self, node):
        if node in self.node_set:
            print(f"Node '{node}' already exists. Skipping.")
            return
        for i in range(self.replicas):
            node_id = f"{node}-{i}"
            key = self._hash(node_id)
            self.ring[key] = (node, i)
            bisect.insort(self.sorted_keys, key)
        self.node_set.add(node)
        print(f"Node '{node}' added with {self.replicas} replicas.")
    
    def remove_node(self, node):
        if node not in self.node_set:
            print(f"Node '{node}' does not exist. Cannot remove.")
            return
        remove_keys = [k for k in self.sorted_keys if self.ring[k][0] == node]
        for key in remove_keys:
            del self.ring[key]
            self.sorted_keys.remove(key)
        self.node_set.remove(node)
        print(f"Node '{node}' and its replicas removed.")
    
    def get_node(self, key):
        if not self.ring:
            return None
        hash_val = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, hash_val) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]][0]  # return just the node name

    def get_nodes_for_replication(self, key, num_replicas=3):
        if not self.ring:
            return []
        hash_val = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, hash_val)
        nodes = []
        visited = set()
        for i in range(len(self.sorted_keys)):
            node_idx = (idx + i) % len(self.sorted_keys)
            node = self.ring[self.sorted_keys[node_idx]][0]
            if node not in visited:
                nodes.append(node)
                visited.add(node)
            if len(nodes) >= num_replicas:
                break
        return nodes

    def print_ring_diagram(self):
        print("Consistent Hash Ring Diagram:")
        print("-" * 54)
        print("{:<8} | {:<7} | {:<10}".format("Node", "Replica", "Hash"))
        print("-" * 54)
        for key in self.sorted_keys:
            node, replica = self.ring[key]
            print("{:<8} | {:<7} | {:<10}".format(node, replica, key))
        print("-" * 54)
        print("Ring Visualization (sorted by hash):")
        visualization = ["[{:>5}]{}-{}".format(k, self.ring[k][0], self.ring[k][1]) for k in self.sorted_keys]
        print(" -> ".join(visualization))
        print("-" * 54)

# ----------------------- DEMO -----------------------

nodes = ['NodeA', 'NodeB', 'NodeC', 'NodeD', 'NodeE']
ring = ConsistentHashRing(nodes, replicas=3)

print("Initial ring with 5 nodes:")
ring.print_ring_diagram()

print("\nKey Placement Example:")
for key in ['apple', 'banana', 'carrot', 'date']:
    print(f"Key '{key}' is stored on: {ring.get_node(key)}")

print("\nReplication Example:")
for key in ['apple', 'banana']:
    print(f"Key '{key}' is replicated to: {ring.get_nodes_for_replication(key, 3)}")

print("\nAdding NodeF:")
ring.add_node('NodeF')
ring.print_ring_diagram()
print("Key 'apple' is now stored on:", ring.get_node('apple'))

print("\nAdding NodeF again:")
ring.add_node('NodeF')

print("\nRemoving NodeB:")
ring.remove_node('NodeB')
ring.print_ring_diagram()
print("Key 'apple' is now stored on:", ring.get_node('apple'))

print("\nRemoving NodeB again:")
ring.remove_node('NodeB')

print("\nRe-adding NodeB:")
ring.add_node('NodeB')
ring.print_ring_diagram()
print("Key 'apple' is now stored on:", ring.get_node('apple'))

print("\nKey placement after ring changes:")
for key in ['apple', 'banana', 'carrot', 'date']:
    print(f"Key '{key}' is stored on: {ring.get_node(key)}")