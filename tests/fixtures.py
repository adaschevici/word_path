import io
from collections import defaultdict

WORDFILE = """cat
dog
combine
filtered
Dog"""

WORDLIST = ["dog", "bog", "log", "cog"]
MATCHES_EXPECTED = defaultdict(list,
             {("*", 'o', 'g'): ['dog',
                                'bog',
                                'log',
                                'cog'],
              ('b', "*", 'g'): ['bog'],
              ('b', 'o', "*"): ['bog'],
              ('c', "*", 'g'): ['cog'],
              ('c', 'o', "*"): ['cog'],
              ('d', "*", 'g'): ['dog'],
              ('d', 'o', "*"): ['dog'],
              ('l', "*", 'g'): ['log'],
              ('l', 'o', "*"): ['log']})

NEIGHBOURS_EXPECTED = defaultdict(list,
             {'bog': [['dog', 'bog', 'log', 'cog'], ['bog'], ['bog']],
              'cog': [['dog', 'bog', 'log', 'cog'], ['cog'], ['cog']],
              'dog': [['dog', 'bog', 'log', 'cog'], ['dog'], ['dog']],
              'log': [['dog', 'bog', 'log', 'cog'], ['log'], ['log']]})

PATH_FOUND = """dog
cog
log
cag
for
cat"""

PATH_NOT_FOUND = """dog
cog
log
cag
for
cat"""
