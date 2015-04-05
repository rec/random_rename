#!/usr/bin/env python2.7

import glob
import os
import random
import sys

PREFIX = '---xyzzy---'

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
        fnames.extend(glob.glob(f))

    if not fnames:
        print('No files.')
    elif len(fnames) == 1:
        print('Only one file.')
    else:
        return fnames


if __name__ == '__main__':
    fnames = get_filenames()
    if fnames:
        reordered = list(fnames)
        random.shuffle(reordered)

        for fname, _ in zip(fnames, reordered):
            os.rename(fname, add_prefix(fname))

        for fname, newname in zip(fnames, reordered):
            print('%s -> %s' % (fname, newname))
            os.rename(add_prefix(fname), newname)

#
