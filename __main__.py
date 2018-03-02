import argparse
import sys

def main(args):
    source_names = args.file
    if any([check_file(source_name) for source_name in source_names]):
        return 1
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+', help="Files to check")
    sys.exit(main(parser.parse_args()))
