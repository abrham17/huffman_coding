from collections import Counter
from heapq import heappop, heappush
class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        """
        Initialize a Huffman node
        
        Args:
            char: The character this node represents (None for internal nodes)
            freq: Frequency of the character
            left: Left child node
            right: Right child node
        """

        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        """
        Compare two Huffman nodes by frequency
        """
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
    
    def frequency_analysis(self, text):
        return dict(Counter(text))
    
    def build_heap(self, frequency):
        for char, freq in frequency.items():
            heappush(self.heap, HuffmanNode(char, freq))
    
    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heappop(self.heap)
            node2 = heappop(self.heap)
            merged = HuffmanNode(left=node1, right=node2, freq=node1.freq + node2.freq)
            heappush(self.heap, merged)
    
    def generate_codes(self):
        pass
    
    def encode(self, text):
        pass
    
    def decode(self, encoded_text):
        pass
