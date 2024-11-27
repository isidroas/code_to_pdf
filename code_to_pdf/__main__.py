import sys
from code_to_pdf import generate
from pathlib import Path
def main():
    sys.stdout.write(generate(Path(sys.argv[1])))

if __name__ == '__main__':
    main()
