#!/usr/bin/env python3
"""Decide which upstream IdentityServer releases need a -nota build.

Rule, per major.minor line (>= MIN_LINE):
  * if the line already has -nota builds, build every stable upstream release
    newer than the newest -nota build;
  * otherwise build only the newest stable upstream release of that line.

Usage: discover.py <upstream-tags-file> <existing-tags-file>
Both files contain one tag name per line (e.g. output of `git ls-remote --tags`
reduced to names). Prints a JSON array of versions, e.g. ["7.4.15","8.0.11"].
"""
import json
import re
import sys
from collections import defaultdict

MIN_LINE = (7, 4)
UPSTREAM_RE = re.compile(r"^is-(\d+)\.(\d+)\.(\d+)$")
NOTA_RE = re.compile(r"^is-(\d+)\.(\d+)\.(\d+)-nota(?:\.\d+)?$")


def parse(path, pattern):
    with open(path) as f:
        names = {line.strip() for line in f if line.strip()}
    return {tuple(map(int, m.groups())) for m in map(pattern.match, names) if m}


def select(upstream, built):
    by_line = defaultdict(list)
    for v in upstream:
        if v[:2] >= MIN_LINE:
            by_line[v[:2]].append(v)

    selected = []
    for line, versions in by_line.items():
        built_in_line = [v for v in built if v[:2] == line]
        if built_in_line:
            newest_built = max(built_in_line)
            selected += [v for v in versions if v > newest_built]
        else:
            selected.append(max(versions))
    return sorted(selected)


if __name__ == "__main__":
    upstream = parse(sys.argv[1], UPSTREAM_RE)
    built = parse(sys.argv[2], NOTA_RE)
    print(json.dumps([".".join(map(str, v)) for v in select(upstream, built)]))
