import pandas as pd
import argparse
import logging
import sys
import re


class UcscRegions(object):

    def __init__(self):
        pass

    def main(self, args):
        self.name = args[0]
        p = argparse.ArgumentParser(prog=self.name,
                                    description='Extract regions from UCSC web output',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        p.add_argument('ucsc_file', help='USCS table file', metavar='ucsc-file')
        p.add_argument('-o', '--output-file', help='Output file')
        p.add_argument('--verbose', help='More detailed log messages')
        p.add_argument('--log-file', help='Write log messages to file', dest='log_file')
        opts = p.parse_args(args[1:])

        logging.basicConfig(filename=opts.log_file, format='%(levelname)s (%(asctime)s): %(message)s')
        log = logging.getLogger(__name__)
        if opts.verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

        log.info('Reading data file ...')
        table = pd.read_table(opts.ucsc_file)
        table.columns = [x.split('.')[2] for x in table.columns]
        regions = table.groupby('geneSymbol').apply(lambda x: pd.DataFrame({
            'chromo': [x.chrom.iloc[0]],
            'start': [x.txStart.min()],
            'end': [x.txEnd.max()]
        }))
        regions.index = regions.index.droplevel(1)
        regions.reset_index(inplace=True)
        regions = regions[['chromo', 'start', 'end', 'geneSymbol']]
        regions['chromo'] = list(map(lambda x: re.sub('^CHR', '', x.upper()), regions['chromo']))
        regions.sort('geneSymbol', inplace=True)

        log.info('Writing output ...')
        if opts.output_file is None:
            f = sys.stdout
        else:
            f = open(opts.output_file, 'w')
        regions.to_csv(f, sep='\t', index=False)
        if opts.output_file is None:
            f.close()
