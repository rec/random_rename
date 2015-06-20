#!/usr/bin/env python2.7

from __future__ import print_function

import glob
import os
import random
import sys

PREFIX = '---xyzzy---'
ARGS = sys.argv
DRY_RUN_FLAG = '-n'
DRY_RUN = DRY_RUN_FLAG in ARGS
if DRY_RUN:
    ARGS.remove(DRY_RUN_FLAG)

def _error(*args):
    print(*args, file=sys.stderr)


def input_filenames():
    while True:
        f = raw_input('filename: ').strip()
        if f:
            yield f
        else:
            return

def add_prefix(fname):
    base, name = os.path.split(fname)
    return os.path.join(base, PREFIX + name)

def get_filenames():
    fnames = []
    for f in sys.argv[1:] or list(input_filenames()):
        match = glob.glob(f)
        if match:
            fnames.extend(match)
        else:
            _error('No files matching', f)

    if not fnames:
        print('No matching files.', file=sys.stderr)
    elif len(fnames) == 1:
        print('Only one file.', file=sys.stderr)
    else:
        return fnames

def random_rename():
    filenames = get_filenames()
    if not filenames:
        return

    reordered = list(filenames)
    random.shuffle(reordered)

    # To prevent having to factor the permutation into cycles and apply them
    # individually, we do the rename in two stages:

    # 1. Add the prefix to every file.
    if DRY_RUN:
        print('Not executing:')
    else:
        for name, _ in zip(filenames, reordered):
            os.rename(name, add_prefix(name))

    # 2. rename the prefix files to the final name.
    for name, newname in zip(filenames, reordered):
        print('%s -> %s' % (name, newname))
        if not DRY_RUN:
            os.rename(add_prefix(name), newname)

if __name__ == '__main__':
    random_rename()

#
