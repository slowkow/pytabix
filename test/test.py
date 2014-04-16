#!/usr/bin/env python
"""
test_tabix.py
Hyeshik Chang <hyeshik@snu.ac.kr>
Kamil Slowikowski <slowikow@broadinstitute.org>
April 15, 2014

The MIT License

Copyright (c) 2011 Seoul National University.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import unittest
import random
import gzip
import tabix


EXAMPLEFILE = 'test/example.gtf.gz'


def load_example_regions(path):
    alldata = []

    for line in gzip.open(EXAMPLEFILE):
        fields = line.rstrip().split('\t')
        seq = fields[0]
        low = int(fields[3])
        high = int(fields[4])
        alldata.append([seq, low, high, fields[:7]])

    return alldata


def does_overlap(A, B, C, D):
    return (A <= D <= B) or (C <= B <= D)


def sample_test_dataset(regions, ntests):
    seqs = [fields[0] for fields in regions]
    lowerbound = max(0, min(fields[1] for fields in regions) - 1000)
    upperbound = max(fields[2] for fields in regions) + 1000

    tests = []
    for i in range(ntests):
        seq = random.choice(seqs)
        low = random.randrange(lowerbound, upperbound)
        high = random.randrange(low, upperbound)

        # for 1-based both-end inclusive intervals
        matches = [info for seq_, begin, end, info in regions
                   if seq == seq_ and does_overlap(begin, end, low, high)]

        tests.append((seq, low, high, matches))

    return tests


class TabixTest(unittest.TestCase):
    regions = load_example_regions(EXAMPLEFILE)
    testset = sample_test_dataset(regions, 500)

    def setUp(self):
        self.tb = tabix.open(EXAMPLEFILE)

    def test_query(self):
        for seq, low, high, tests in self.testset:
            results = [fields[:7] for fields in self.tb.query(seq, low, high)]
            self.assertEqual(results, tests)

    def test_querys(self):
        for seq, low, high, tests in self.testset:
            query = "{}:{}-{}".format(seq, low, high)
            results = [fields[:7] for fields in self.tb.querys(query)]
            self.assertEqual(results, tests)

    def test_remote_file(self):
        file1 = "ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20100804/" \
                "ALL.2of4intersection.20100804.genotypes.vcf.gz"
        tb = tabix.open(file1)

    def test_remote_file_bad_url(self):
        file1 = "ftp://badurl"
        with self.assertRaises(tabix.TabixError):
            tb = tabix.open(file1)


if __name__ == '__main__':
    unittest.main()
