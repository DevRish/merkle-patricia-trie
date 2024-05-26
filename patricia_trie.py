from typing import List, Union

class PatriciaTrieNode:
    def __init__(self, value=''):
        self.children: List[Union[PatriciaTrieNode,None]] = [None] * 26
        self.is_end = False
        self.value = value

class PatriciaTrie:
    def __init__(self):
        self.root = PatriciaTrieNode()

    def display(self):
        q: List[PatriciaTrieNode] = []
        q.append(self.root)
        while len(q) > 0:
            print("[ ", end="")
            sz = len(q)
            while sz > 0:
                element = q.pop(0)
                print(f"<{element.value},{element.is_end}> ", end="")
                for ch in element.children:
                    if ch is not None:
                        q.append(ch)
                sz -= 1
            print("]")

    def insert(self, word: str):
        if len(word) == 0:
            self.root.is_end = True
            return
        word = word.lower()
        node = self.root
        i = 0
        while i < len(word):
            char = ord(word[i]) - ord('a')
            if node.children[char] is not None:
                child = node.children[char]
                j = 0
                while i + j < len(word) and j < len(child.value) and word[i + j] == child.value[j]:
                    j += 1
                if j == len(child.value):
                    node = child
                    i += j
                else:
                    existing_child = PatriciaTrieNode(child.value[j:])
                    existing_child.children = child.children
                    existing_child.is_end = child.is_end

                    node.children[char] = PatriciaTrieNode(child.value[:j])
                    node.children[char].children[ord(child.value[j])-ord('a')] = existing_child

                    if i + j == len(word):
                        node.children[char].is_end = True
                    else:
                        new_child = PatriciaTrieNode(word[i + j:])
                        new_child.is_end = True
                        node.children[char].children[ord(word[i + j])-ord('a')] = new_child
                    break
            else:
                node.children[char] = PatriciaTrieNode(word[i:])
                node.children[char].is_end = True
                break

    def search(self, word):
        node = self.root
        i = 0
        while i < len(word):
            char = ord(word[i]) - ord('a')
            if node.children[char] is not None:
                child = node.children[char]
                j = 0
                while i + j < len(word) and j < len(child.value) and word[i + j] == child.value[j]:
                    j += 1
                if j == len(child.value):
                    node = child
                    i += j
                else:
                    return False
            else:
                return False
        return node.is_end

if __name__ == "__main__":
    trie = PatriciaTrie()
    trie.insert("big")
    trie.insert("bigger")
    trie.insert("bill")
    trie.insert("good")
    trie.insert("gosh")
    trie.display()