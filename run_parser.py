import argparse
import logging
from parsers.earley import recognize as earley
from parsers.top_down import parse as top_down
from parsers.graph_search import *

PARSER = {
    'earley': earley,
    'top_down': top_down
}

SEARCH = {
    'dfs_first': dfs_search_first,
    'dfs_all': dfs_search_all,
    'bfs_first': bfs_search_first,
    'bfs_all': bfs_search_all
}


def run_parser(args):
    if args.parser not in PARSER:
        raise NotImplementedError('{} parser is not available!'.format(args.parser))
    if args.search and args.search not in SEARCH:
        raise NotImplementedError('{} search is not available!'.format(args.search))
    tokens = args.sentence.split()
    if args.search:
        PARSER[args.parser](tokens, args.grammar, SEARCH[args.search])
    elif args.lexicon:
        PARSER[args.parser](tokens, args.grammar, args.lexicon)


def main():
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    arg_parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('parser', help='parser that should be run (earley)')
    arg_parser.add_argument('sentence', help='string of tokens separated by whitespace, e.g. "Peter likes hot coffee"')
    arg_parser.add_argument('--lexicon', help='path to lexicon file')
    arg_parser.add_argument('--grammar', help='path to grammar file')
    arg_parser.add_argument('--search', help='search for config parsers')
    run_parser(arg_parser.parse_args())


if __name__ == '__main__':
    main()
