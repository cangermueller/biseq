#!/usr/bin/env python

import pandas as pd
import sys
import os
import argparse
import biseq.hdf

if __name__ == '__main__':
    name = sys.argv[0]
    p = argparse.ArgumentParser(prog=os.path.basename(name),
                                description='Dump content of HDF file',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('hdf_path', help='HDF path name (file.h5:/group)', nargs='+')
    p.add_argument('--where', help='WHERE statement in HDF query')
    p.add_argument('--start', help='Start index', type=int)
    p.add_argument('--stop', help='Stop index', type=int)
    p.add_argument('--head', help='Print first 10 lines', action='store_true')
    opts = p.parse_args()
    if opts.head == True and opts.start is None and opts.stop is None:
        opts.stop = 10

    for hdf_path in opts.hdf_path:
        file, group = biseq.hdf.split_filename(hdf_path)
        if group == '/':
            raise RuntimeError('No HDF group provided!')

        df = pd.read_hdf(file, group, where=opts.where, start=opts.start,
                         stop=opts.stop)
        print(df)
