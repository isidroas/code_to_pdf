from typing import Any
from dataclasses import dataclass
import subprocess
def disk_usage(path):
    if path.is_file():
        return path.stat().st_size

    # TODO: more efficient
    #       - caching child sizes when calculating parent size
    #       - traverse at the same time that filtering. Do not return childs if parent does not satisfy `--size-bigger X`
    # TODO: if no `du` program, fallback to sum(... rglob('*')). Source: https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
    # TODO: use this for filtering also, not only for sorting
    size, name = subprocess.run(['du', '-bs', str(path)], capture_output=True).stdout.decode().split()
    return int(size.strip())

# en realidad sirve para cualquier objeto! ints, o por ejemplo uno custom
@dataclass
class NegateCmp:
    value: Any
    def __eq__(self, other):
        return self.value == other.value
    def __lt__(self,other):
        return self.value >= other.value


from fnmatch import fnmatch

def sort_key(path):
    return (
        # fnmatch(p.name, '*.pdf'),
        # path.is_dir(),
        disk_usage(path) if not path.name == 'heap_test.stdout' else disk_usage(path.parent/'main.c') + 1,
        # NegateCmp(path.name),
        path.name,
    )
