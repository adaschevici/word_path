import argparse
import sys
from wordpath.constants import DICT_FILE
from wordpath.paths import WordLadder

def parse_args(args):
    """Main args_parser for the wordpaths solver"""
    command = argparse.ArgumentParser(description='This is a word ladder calculator program')
    command.add_argument("-d", "--dictionary", dest="dictionary", default=DICT_FILE,
                         help="Dictionary file for the script")
    command.add_argument("-w1", "--word-one", dest="wordone", help="Starting word")
    command.add_argument("-w2", "--word-two", dest="wordtwo", help="Destination word")
    arguments = command.parse_args(args)
    return arguments


def main():
    args = parse_args(sys.argv[1:])
    print(WordLadder(args.wordone, args.wordtwo, len(args.wordone)).word_ladder())

if __name__ == "__main__":
    main()
