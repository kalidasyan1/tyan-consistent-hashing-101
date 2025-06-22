# Consistent Hashing Hash Ring

## Overview

This project demonstrates a Python implementation of **consistent hashing**, a foundational technique in distributed systems for partitioning data and achieving horizontal scalability with minimal key movement during membership changes.

Consistent hashing addresses the problem of distributing keys among a dynamic set of nodes (servers) in such a way that when nodes are added or removed, only a small subset of keys need to be remapped. This property makes it a popular choice for building scalable, fault-tolerant systems such as distributed caches and databases.

## How Consistent Hashing Works

- **Hash Ring**: Both physical nodes and data keys are mapped onto a fixed-size circular hash space (the "ring") using a hash function (e.g., MD5).
- **Virtual Nodes (Replicas)**: Each physical node is represented by multiple points ("replicas") on the ring to achieve better load balancing.
- **Key Placement**: To find the node responsible for a key, hash the key, then walk clockwise on the ring to the first node whose hash is greater than or equal to the key's hash (wrapping around if needed).
- **Replication**: For fault tolerance, data can be replicated to multiple unique successor nodes on the ring.

### Example

Suppose nodes are added to the ring as `NodeA`, `NodeB`, etc., each with several virtual nodes. When a node joins or leaves:
- Only keys falling between affected hash intervals need to be redistributed.
- The vast majority of key assignments remain unchanged, ensuring stability.

## Project Features

- Add and remove nodes (with safety checks for duplicates)
- Each node uses multiple replicas (virtual nodes) for smoother distribution
- Query the responsible node for any key
- Query a set of nodes for key replication (N-way replication)
- Print a diagram of the ring with hash positions for all nodes and their replicas
- Interactive demos of key placements before and after adding/removing nodes

## Usage & Example Output

- Initialize the ring with any set of nodes
- Dynamically add or remove nodes and observe how key placements are impacted
- Display a sorted diagram of the ring for debugging and visualization
- See which nodes are responsible for any given key and how N-way replication is handled

Example outputs show key assignments and ring structure as nodes are added or removed, demonstrating the minimal disruption property of consistent hashing.

## Why Use Consistent Hashing?

Consistent hashing is used by systems such as **Amazon DynamoDB, Apache Cassandra, Riak, and Memcached clients** to enable:
- Fault tolerance through efficient replication
- Scalable, elastic addition and removal of nodes
- Even distribution of load using virtual nodes

## References

- [Amazon Dynamo: A Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Consistent Hashing (Martin Fowler)](https://martinfowler.com/articles/consistent-hashing.html)
- [Wikipedia: Consistent Hashing](https://en.wikipedia.org/wiki/Consistent_hashing)