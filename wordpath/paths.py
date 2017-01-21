from collections import defaultdict, namedtuple
from heapq import heappush, heappop
from wordpath.exceptions import NotFound
from wordpath.constants import DICT_FILE


class FilteredWords(object):

    def __init__(self, maxlen):
        self.length = maxlen

    def get_filtered_words(self):
        """
        Gets the list of words which have length
        max_len
        """
        dictionary = [w.strip() for w in open(DICT_FILE) if w == w.lower()]
        max_len_letter_words = [w for w in dictionary if len(w) == self.length]
        return max_len_letter_words


class BucketBuilder(object):

    def __init__(self, words):
        self.words = words

    def build_buckets(self):
        """ Build a dict of matches
        and one for neighbours.
        """
        # build buckets function
        placeholder = '*'
        matches = defaultdict(list)
        neighbours = defaultdict(list)
        for word in self.words:
            for i in range(len(word)):
                # build a string with a * in place of the i'th
                # character in the string
                pattern = tuple(placeholder if i == j else c
                                for j, c in enumerate(word))
                m = matches[pattern]
                m.append(word)
                neighbours[word].append(m)
        return neighbours


def heuristic(word_one, word_two):
    """Returns the number of chars
    that are different between word_one and word_two"""
    return sum(a != b for a, b in zip(word_one, word_two))

Node = namedtuple('Node', 'f g word previous')

class Graph(list):

    def __init__(self, root):
        self = self.append(root)

    def add_node(self, node):
        heappush(self, node)

    def get_node(self):
        return heappop(self)

class NodeLists(object):

    """This is a class wrapper for the
    list of visited/unvisited nodes"""
    def __init__(self, start):
        self.visited = set()
        self.unvisited = set([start])

    def remove(self, node, list_name):
        attribute = getattr(self, list_name)
        attribute.remove(node)

    def add(self, node, list_name):
        attribute = getattr(self, list_name)
        attribute.add(node)

    def contains(self, word):
        return word not in self.visited and word not in self.unvisited

class WordLadder(object):

    def __init__(self, start, end, word_length):
        self.start = start
        self.end = end
        self.word_length = word_length
        self._preprocess()

    def _get_path(self, node):
        path = []
        while node:
            path.append(node.word)
            node = node.previous
        return path[::-1]

    def _preprocess(self):
        self.words = FilteredWords(self.word_length).get_filtered_words()
        self.neighbours = BucketBuilder(self.words).build_buckets()

    def word_ladder(self):
        """
        Calculates the word ladder between the two words
        """
        node_lists = NodeLists(self.start)
        graph = Graph(Node(heuristic(self.start, self.end), 0, self.start, None))
        while graph:
            node = graph.get_node()
            if node.word == self.end:
                return self._get_path(node)
            node_lists.remove(node.word, 'unvisited')
            node_lists.add(node.word, 'visited')
            g = node.g + 1
            for neighbourhood in self.neighbours[node.word]:
                for word in neighbourhood:
                    if node_lists.contains(word):
                        next_node = Node(heuristic(word, self.end) + g, g, word, node)
                        graph.add_node(next_node)
                        node_lists.add(word, 'unvisited')
        raise NotFound("No ladder from {} to {}".format(self.start, self.end))
