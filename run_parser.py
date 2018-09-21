import argparse
import logging
from parsers.earley import recognize_verbose

PARSERS = {
    'earley': recognize_verbose
}


def run_parser(args):
    if args.parser not in PARSERS:
        raise NotImplementedError('{} parser is not available!'.format(args.parser))
    PARSERS[args.parser](args.lexicon, args.grammar, args.sentence.split())


def main():
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    arg_parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('parser', help='parser that should be run (earley)')
    arg_parser.add_argument('sentence', help='string of tokens separated by whitespace, e.g. "Peter likes hot coffee"')
    arg_parser.add_argument('--lexicon', help='path to lexicon file', default='data/lexicon.txt')
    arg_parser.add_argument('--grammar', help='path to grammar file', default='data/grammar.txt')
    run_parser(arg_parser.parse_args())


if __name__ == '__main__':
    main()
