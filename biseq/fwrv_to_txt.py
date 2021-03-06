import argparse
import pandas as pd
import numpy as np
import logging
import os

class FwrvToTxt(object):

    def __init__(self):
        pass

    def main(self, args):
        self.name = os.path.basename(args[0])
        p = argparse.ArgumentParser('Split Babraham forward/reverse counts files by samples',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        p.add_argument('fw_file', help='Forward counts file', metavar='fw-file')
        p.add_argument('rv_file', help='Reverse counts file', metavar='rv-file')
        p.add_argument('-o', '--out-dir', help='Output directory', default='.')
        p.add_argument('--samples', help='Indices of samples', nargs='+')
        p.add_argument('--prefix', help='Prefix of output files', default='s')
        p.add_argument('--nrows', help='Only read that number of rows', type=int)
        p.add_argument('--no-drop', help='Do not drop zero counts sites', dest='drop', default=True, action='store_false')
        p.add_argument('--verbose', help='More detailed log messages', default=False, action='store_true')
        p.add_argument('--log-file', help='Write log messages to file')
        opts = p.parse_args(args[1:])

        logging.basicConfig(filename=opts.log_file, format='%(levelname)s (%(asctime)s): %(message)s')
        log = logging.getLogger(__name__)
        if opts.verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

        if opts.verbose:
            log.debug('Command line arguments:')
            log.debug(str(opts))

        log.info('Reading positions ...')
        pos = pd.read_table(opts.fw_file, usecols=['Chromosome', 'Start', 'End'],
                            dtype=dict(Chromosome=np.str, Start=np.int, End=np.int),
                            nrows=opts.nrows)
        pos.columns = ['chromo', 'start', 'end']
        columns = pd.read_table(opts.fw_file, nrows=1).columns
        if not opts.samples:
            opts.samples = range(list(columns == 'Distance').index(True) + 1, len(columns))

        log.info('Reading forward counts ...')
        fw = pd.read_table(opts.fw_file, usecols=opts.samples, nrows=opts.nrows).astype(np.int16)

        log.info('Reading reverse counts ...')
        rv = pd.read_table(opts.rv_file, usecols=opts.samples, nrows=opts.nrows).astype(np.int16)

        log.info('Splitting counts by samples ...')
        sample_names = fw.columns
        for sample_name in sample_names:
            log.info('\t' + sample_name)
            counts = pd.concat((pos, fw[sample_name], fw[sample_name] + rv[sample_name]), axis=1)
            counts.columns = list(counts.columns[:-2]) + ['nmet','ntot']
            if opts.drop:
                counts = counts[(counts.ntot > 0)]
            filename = os.path.join(opts.out_dir, '%s%s.txt' % (opts.prefix, sample_name))
            counts.to_csv(filename, sep='\t', index=False)

        log.info('Done!')
