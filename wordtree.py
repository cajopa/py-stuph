'''
Produce shorthand aliases based on a list of all possible commands.
For primary use with git.
'''

class WordTreeNode:
    def __init__(self, word):
        word_iter = iter(word)
        
        self.value = next(word_iter)
        self.children = {}
        
        self.add_subword(word_iter)
    
    def add_subword(self, subword):
        try:
            child = WordTreeNode(subword)
        except StopIteration:
            return
        
        if child.value in self.children:
            self.children[children.value].merge(child)
        else:
            self.children[child.value] = child
    
    def merge(self, other):
        if self.value == other.value:
            pass
        else:
            pass
    
    def __iter__(self):
        for child in self.children:
            for i in iter(child):
                yield self.value + i
