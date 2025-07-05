from functools import cache
from typing import List, Set, Dict, Optional
from english_words import get_english_words_set

class TrieNode:
    __slots__ = ('end', 'children')

    def __init__(self):
        self.end: bool = False
        self.children: Dict[str, TrieNode] = {}

class Trie:
    def __init__(self, dictionary: Set[str]):
        self.head = TrieNode()
        for word in dictionary:
            self.add_word(word)

    def add_word(self, word: str) -> None:
        node = self.head
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end = True

@cache
def find_neighbors(i: int) -> Set[int]:
    N = 4
    ret = set()
    top = i // N == 0
    bottom = i // N == N-1
    left = i % N == 0
    right = i % N == N-1

    if not top:
        ret.add(i-N)
    if not bottom:
        ret.add(i+N)
    if not left:
        ret.add(i-1)
    if not right:
        ret.add(i+1)
    if not top and not left:
        ret.add(i-N-1)
    if not top and not right:
        ret.add(i-N+1)
    if not bottom and not left:
        ret.add(i+N-1)
    if not bottom and not right:
        ret.add(i+N+1)

    return ret

def find_words(root: TrieNode, board: str, start_tile: int, words: Set[str]):
    visited = set()

    def search(tile: int, trie: TrieNode, partial_word):
        visited.add(tile)
        if board[tile] not in trie.children:
            visited.remove(tile)
            return

        trie = trie.children[board[tile]]
        partial_word += board[tile]
        if trie.end:
            words.add(partial_word)

        for neighbor in find_neighbors(tile):
            if neighbor not in visited:
                search(neighbor, trie, partial_word)

        visited.remove(tile)

    search(start_tile, root, "")

def boggle(board: str) -> Set[str]:
    if len(board) != 16:
        raise Exception("Invalid board size")

    board = board.lower()
    alphabet = {c for c in board}
    dictionary = get_english_words_set(['web2'], lower=True)
    pruned_dictionary = {word for word in dictionary if len(word) > 2 and len(word) <= 16 and set(word).issubset(alphabet)}
    trie = Trie(pruned_dictionary)

    words = set()
    for i in range(len(board)):
        find_words(trie.head, board, i, words)

    return words
