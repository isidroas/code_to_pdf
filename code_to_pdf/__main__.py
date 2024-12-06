import sys
from argparse import ArgumentParser
from pathlib import Path

from code_to_pdf import generate


def main():
    parser = ArgumentParser(description="Print a latex document to stdout")
    parser.add_argument("source_directory")
    parser.add_argument("--title", help="Defaults to source_directory name")
    parser.add_argument("--mainfont")
    parser.add_argument("--monofont")
    args = parser.parse_args()
    try:
        tex_document = generate(
            Path(args.source_directory),
            title=args.title,
            mainfont=args.mainfont,
            monofont=args.monofont,
        )
    except FileNotFoundError as e:
        sys.exit('not found "%s"' % str(e))

    sys.stdout.write(tex_document)


if __name__ == "__main__":
    main()
