#!/usr/bin/env python

import pytest
import numpy.testing as npt
import pandas as pd
import numpy as np
import os
from biseq.counts_summer import CountsSummer
import pdb


def test_sum_counts():
    regions = dict(
        chromo=[    1,  1,  1,  2,  2,  'X'],
        start =[    1,  5,  1,  1,  5,    3],
        end   =[   10, 10, 20,  3, 15,    8]
    )
    counts = dict(
        chromo=[    1,  1,  1,  2,  2,  2],
        start =[    1,  4, 14,  2,  3, 20],
        end   =[    1,  4, 14,  2,  3, 20],
        nmet  =[    1,  0,  2,  0,  3,  0],
        ntot  =[    0,  1,  0,  2,  3,  1]
    )
    expected_sum = dict(
        nmet  =[    1,  0,  3,  3,  0,  0],
        ntot  =[    1,  0,  1,  5,  0,  0]
    )

    regions = pd.DataFrame(regions)
    counts = pd.DataFrame(counts)
    expected_sum = pd.DataFrame(expected_sum)
    counts['chromo'] = counts['chromo'].astype(np.str)
    counts.set_index(['chromo', 'start', 'end'], inplace=True)
    actual_sum = CountsSummer().sum_counts(regions, counts)
    assert (actual_sum['nmet'] == expected_sum['nmet']).all()
    assert (actual_sum['ntot'] == expected_sum['ntot']).all()
