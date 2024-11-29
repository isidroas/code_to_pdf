import sys
from code_to_pdf import generate
from pathlib import Path
from argparse import ArgumentParser
def main():
    parser = ArgumentParser(description='Print a latex document to stdout')
    parser.add_argument('source_directory')
    parser.add_argument('--title', help='Defaults to source_directory name')
    args = parser.parse_args()
    sys.stdout.write(generate(Path(args.source_directory), title=args.title))

if __name__ == '__main__':
    main()
