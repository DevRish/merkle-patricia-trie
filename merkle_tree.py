from Crypto.Hash import keccak
from typing import Union

def hash(value: bytes):
    k = keccak.new(digest_bits=256)
    k.update(value)
    return k.digest()

class MerkleTreeNode:
    def __init__(self, value=b'', left=None, right=None):
        self.value: bytes = value
        self.left: Union[MerkleTreeNode, None] = left
        self.right: Union[MerkleTreeNode, None] = right

class MerkleTree:
    def __init__(self):
        self.root = MerkleTreeNode()
    
    def generate(self, data=b''):
        chunks = [data[i:i + 32] for i in range(0, len(data), 32)]
        leaves = [MerkleTreeNode(value=hash(chunk)) for chunk in chunks]
        q = leaves
        while len(q) > 1:
            sz = len(q)
            while sz > 0:
                if sz == 1:
                    e1 = q.pop(0)
                    parent = MerkleTreeNode(value=hash(e1.value), left=e1)
                    q.append(parent)
                    sz -= 1
                else:
                    e1 = q.pop(0)
                    e2 = q.pop(0)
                    parent = MerkleTreeNode(value=hash(b''.join([e1.value,e2.value])), left=e1, right=e2)
                    q.append(parent)
                    sz -= 2
        self.root = q.pop(0)
    
    def display(self):
        q = [self.root]
        while len(q) > 0:
            print("[ ", end="")
            sz = len(q)
            while sz > 0:
                element = q.pop(0)
                print(f"{element.value.hex()} ", end="")
                if element.left is not None: q.append(element.left)
                if element.right is not None: q.append(element.right)
                sz -= 1
            print("]")

if __name__ == "__main__":
    print("===== Merkle Tree 1 =====")
    mt1 = MerkleTree()
    mt1.generate(b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua')
    mt1.display()

    print("===== Merkle Tree 2 =====")
    mt2 = MerkleTree()
    mt2.generate(b'Lorem ipsum dolor sit amet, consectetur adipiscing elit')
    mt2.display()

    print("===== Merkle Tree 3 =====")
    mt3 = MerkleTree()
    mt3.generate(b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua')
    mt3.display()
