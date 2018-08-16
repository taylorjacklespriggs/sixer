import argparse
import os
import sys

from sixer import check_file

def valid_file(filename):
    return filename.endswith('.py') and os.path.isfile(filename)

def all_paths(path):
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            full_filename = os.path.join(dirpath, filename)
            if valid_file(full_filename):
                yield full_filename

def all_files(paths):
    for path in paths:
        for filename in all_paths(path):
            yield filename

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+', help="Files to check")
    args = parser.parse_args()
    source_names = all_files(args.file)
    if any([check_file(source_name) for source_name in source_names]):
        exit_code = 1
    else:
        exit_code = 0
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
