import argparse
import pandas as pd
import numpy as np
import logging
import os
from biseq import utils


class TxtToHdfOpts(object):
    def __init__(self):
        self.counts_files = None
        self.out_hdf = 'counts.h5'
        self.verbose = False
        self.log_file = None

    def __str__(self):
        return str(vars(self))


class TxtToHdf(object):
    def __init__(self):
        self.opts = TxtToHdfOpts()

    def add_counts_file(self, counts_file, hdf_path):
        counts = pd.read_table(counts_file)
        counts.set_index(['chromo', 'start', 'end'], inplace=True)
        dset = os.path.basename(counts_file)
        dset = os.path.splitext(dset)[0]
        filename, path = utils.split_hdf_path(hdf_path)
        counts.to_hdf(filename, os.path.join(path, dset),
                    format='t', data_columns=['chromo', 'start', 'end', 'fw','rv'])

    def main(self, args):
        self.name=os.path.basename(args[0])
        p = argparse.ArgumentParser(prog=self.name,
                                    description='Add txt counts file to HDF file',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        p.add_argument('counts_files', help='Counts files', metavar='counts-file', nargs='+')
        p.add_argument('-o', '--out-hdf', help='Output HDF path', default=self.opts.out_hdf)
        p.add_argument('--verbose', help='More detailed log messages', default=False, action='store_true')
        p.add_argument('--log-file', help='Write log messages to file')
        p.parse_args(args[1:], self.opts)
        print(self.opts)

        logging.basicConfig(filename=self.opts.log_file, format='%(levelname)s (%(asctime)s): %(message)s')
        log = logging.getLogger(__name__)
        if self.opts.verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

        for counts_file in self.opts.counts_files:
            log.info('Adding %s ...' % counts_file)
            self.add_counts_file(counts_file, self.opts.out_hdf)
