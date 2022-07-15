"""Release script."""
import re


VERSION = '1.0.0b12'


def readlines(filename: str) -> list[str]:
    """Read the file to modify."""
    with open(filename) as in_f:
        return in_f.readlines()


def writelines(filename: str, lines: list[str]) -> None:
    """Write the modified file."""
    with open(filename, 'w') as out_f:
        out_f.write(''.join(lines))


def update_version(filename: str, pattern: str, version: str) -> None:
    """Update the version in the file."""
    def replace_version(line: str) -> str:
        if re.match(pattern, line):
            return re.sub(r'[0-9]+\.[0-9]+\.[0-9]+(?:[a-z0-9]+)?', version, line)
        else:
            return line

    writelines(filename, map(replace_version, readlines(filename)))


update_version('toja/server/frontend/package.json', r'^  "version": "[0-9]+\.[0-9]+\.[0-9]+(?:[a-z0-9]+)?",$', VERSION)
update_version('pyproject.toml', r'^version = "[0-9]+\.[0-9]+\.[0-9]+(?:[a-z0-9]+)?"$',  VERSION)
update_version('production/Dockerfile', r'^.*toja-[0-9]+\.[0-9]+\.[0-9]+(?:[a-z0-9]+)?-py3.*$', VERSION)
