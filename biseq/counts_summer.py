import argparse
import pandas as pd
import numpy as np
import logging
import os
import h5py as h5
import biseq.hdf
import biseq.dtypes


class CountsSummerOpts(object):
    def __init__(self):
        self.regions_file = None
        self.hdf_path = None
        self.out_hdf = 'sum_counts.h5'
        self.datasets = None
        self.verbose = False
        self.log_file = None

    def __str__(self):
        return str(vars(self))


class CountsSummer(object):
    def __init__(self):
        self.opts = CountsSummerOpts()

    def main(self, args):
        self.name = args[0]
        p = argparse.ArgumentParser(prog=os.path.basename(self.name),
                                    description='Sum counts for regions',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        p.add_argument('regions_file', help='Regions file with chromo, start, end column', metavar='regions-file')
        p.add_argument('hdf_path', help='HDF path to input counts', metavar='hdf-path')
        p.add_argument('-o', '--out-hdf', help='Output HDF path', default=self.opts.out_hdf)
        p.add_argument('--datasets', help='Only apply to these datasets in HDF path', nargs='+')
        p.add_argument('--verbose', help='More detailed log messages', action='store_true')
        p.add_argument('--log-file', help='Write log messages to file')
        p.parse_args(args[1:], self.opts)

        logging.basicConfig(filename=self.opts.log_file, format='%(levelname)s (%(asctime)s): %(message)s')
        self.logger = logging.getLogger(self.name)
        if self.opts.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        self.logger.debug('Command line options:\n' + str(self.opts))
        self.run()

    def run(self):
        self.logger.info('Reading regions ...')
        regions = pd.read_table(self.opts.regions_file,
                                usecols=list(biseq.dtypes.INDEX.keys()),
                                dtype=biseq.dtypes.INDEX)
        infile, ingroup = biseq.hdf.split_filename(self.opts.hdf_path)
        datasets = self.opts.datasets
        if datasets is None:
            datasets = biseq.hdf.ls(infile, ingroup)
        outfile, outgroup = biseq.hdf.split_filename(self.opts.out_hdf)
        self.logger.info('Summing counts ...')
        for dataset in datasets:
            path = os.path.join(ingroup, dataset)
            self.logger.info('  ' + path)
            counts = pd.read_hdf(infile, path)
            sum_counts = self.sum_counts(regions, counts)
            assert sum_counts.shape[0] == regions.shape[0]
            sum_counts.to_hdf(outfile, os.path.join(outgroup, dataset))
        self.logger.info('Done!')


    def sum_counts_chromo(self, regions, counts):
        chromo = str(regions['chromo'].iloc[0])
        index = pd.MultiIndex.from_arrays((regions['chromo'].astype(np.str),
                                           regions['start'], regions['end']),
                                          names=['chromo', 'start', 'end'])
        sum_counts = pd.DataFrame(0.0, index=index, columns=counts.columns, dtype=np.float32)
        if chromo not in counts.index:
            return sum_counts
        counts_chromo = counts.loc[chromo]
        counts_chromo.reset_index(inplace=True)
        i = 0
        for t, region in regions.iterrows():
            region_counts = counts_chromo[(counts_chromo['start'] >= region['start']) & (counts_chromo['end'] <= region['end'])]
            sum_counts.iloc[i, :] = region_counts[counts.columns].sum(axis=0)
            i += 1
        return sum_counts

    def sum_counts(self, regions, counts):
        return regions.groupby('chromo').apply(lambda x: self.sum_counts_chromo(x, counts))
