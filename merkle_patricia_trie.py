from Crypto.Hash import keccak
from typing import List, Union
import os
import pickle

def hash(value: bytes):
    k = keccak.new(digest_bits=256)
    k.update(value)
    return k.digest()

class MerklePatriciaTrieNode:
    def __init__(self, key_segment='', data=b'', is_leaf=False):
        self.children: List[Union[MerklePatriciaTrieNode, None]] = [None] * 17
        self.key_segment: str = key_segment
        self.data: bytes = data
        self.is_leaf = is_leaf

class MerklePatriciaTrie:
    def __init__(self):
        self.root = MerklePatriciaTrieNode()

    def _update_hashes(self, node: MerklePatriciaTrieNode):
        if node.is_leaf: return node.data
        child_hashes = [self._update_hashes(child) for child in node.children if child is not None]
        # print(f"Child hashes: {[val.hex() for val in child_hashes]}")
        node.data = hash(b''.join(child_hashes))
        return node.data
    
    def display(self):
        q: List[MerklePatriciaTrieNode] = []
        q.append(self.root)
        while len(q) > 0:
            print("[ ", end="")
            sz = len(q)
            while sz > 0:
                element = q.pop(0)
                print(f"<{element.key_segment},{element.data.hex()}> ", end="")
                for ch in element.children:
                    if ch is not None:
                        q.append(ch)
                sz -= 1
            print("]")

    def addUser(self, accHash: str, data: bytes):
        # print(f"Account Hash: {accHash}")
        node = self.root
        i = 0
        while i < len(accHash):
            char = int(accHash[i], 16)
            if node.children[char] is not None:
                child = node.children[char]
                j = 0
                while i + j < len(accHash) and j < len(child.key_segment) and accHash[i + j] == child.key_segment[j]:
                    j += 1
                if j == len(child.key_segment):
                    # print("Node used up")
                    node = child
                    i += j
                else:
                    # print(f"Common part: {accHash[:i+j]}")
                    existing_child = MerklePatriciaTrieNode()
                    existing_child.key_segment = child.key_segment[j:]
                    existing_child.children = child.children
                    existing_child.data = child.data
                    existing_child.is_leaf = True

                    new_child = MerklePatriciaTrieNode()
                    new_child.key_segment = accHash[i + j:]
                    new_child.data = hash(data)
                    new_child.is_leaf = True

                    node.children[char] = MerklePatriciaTrieNode()
                    node.children[char].key_segment = child.key_segment[:j]
                    node.children[char].children[int(child.key_segment[j], 16)] = existing_child
                    node.children[char].children[int(accHash[i + j], 16)] = new_child
                    node.children[char].is_leaf = False
                        
                    break
            else:
                # print("Didn't exist")
                node.children[char] = MerklePatriciaTrieNode()
                node.children[char].key_segment = accHash[i:]
                node.children[char].data = hash(data)
                node.children[char].is_leaf = True
                break
        
        self._update_hashes(self.root)

    def getUser(self, accHash: str):
        node = self.root
        i = 0
        while i < len(accHash):
            char = int(accHash[i], 16)
            if node.children[char] is not None:
                child = node.children[char]
                j = 0
                while i + j < len(accHash) and j < len(child.key_segment) and accHash[i + j] == child.key_segment[j]:
                    j += 1
                if j == len(child.key_segment):
                    node = child
                    i += j
                else:
                    return None
            else:
                return None
        return node.data
    
    def get_root_hash(self):
        return self.root.data.hex()

if __name__ == "__main__":
    user1 = hash(os.urandom(256)).hex()
    data1 = ["John",5]
    user2 = hash(os.urandom(256)).hex()
    data2 = ["Jane",10]
    user3 = hash(os.urandom(256)).hex()
    data3 = ["Josh",15]

    print(f"Account hash 1: {user1}")
    print(f"Account hash 2: {user2}")
    print(f"Account hash 3: {user3}")

    trie1 = MerklePatriciaTrie()
    trie1.addUser(user1, pickle.dumps(data1))
    trie1.addUser(user2, pickle.dumps(data2))
    # print(f"Root Hash 1: {trie1.get_root_hash()}")

    trie2 = MerklePatriciaTrie()
    trie2.addUser(user1, pickle.dumps(data1))
    trie2.addUser(user3, pickle.dumps(data3))
    # print(f"Root Hash 2: {trie2.get_root_hash()}")

    trie3 = MerklePatriciaTrie()
    trie3.addUser(user1, pickle.dumps(data1))
    trie3.addUser(user2, pickle.dumps(data2))
    # print(f"Root Hash 3: {trie3.get_root_hash()}")

    # verify data hash calculation
    assert(trie1.getUser(user1) == hash(pickle.dumps(["John",5])))

    # verify comparison of root hashes
    assert(trie1.get_root_hash() != trie2.get_root_hash()) # different data, different root hash
    assert(trie1.get_root_hash() == trie3.get_root_hash()) # same data, same root hash

    print("===== Generated MPT 1 =====")
    trie1.display()
    print("===== Generated MPT 2 =====")
    trie2.display()
    print("===== Generated MPT 3 =====")
    trie3.display()
