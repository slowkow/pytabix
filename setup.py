#!/usr/bin/env python
#
# The MIT License
#
# Copyright (c) 2011 Seoul National University.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Contact: Hyeshik Chang <hyeshik@snu.ac.kr>
#          Kamil Slowikowski <slowikow@broadinstitute.org>

from setuptools import setup, find_packages, Extension

EXT_MODULES = [
    Extension("tabix",
        sources=[
            "src/bgzf.c", "src/bgzip.c", "src/index.c",
            "src/knetfile.c", "src/kstring.c",
            "src/tabixmodule.c"
        ],
        include_dirs=["src"],
        libraries=["z"],
        define_macros=[("_FILE_OFFSET_BITS", 64), ("_USE_KNETFILE", 1)]
    )
]

setup(
    name = "pytabix",
    version = "0.0.2",
    description = "Python interface for tabix",
    url = "https://github.com/slowkow/pytabix",
    author = "Hyeshik Chang, Kamil Slowikowski",
    author_email = "hyeshik@snu.ac.kr, slowikow@broadinstitute.org",
    license = "MIT",
    keywords = ["tabix", "bgzip", "bioinformatics", "genomics"],
    packages = find_packages(),
    package_data = { "": ["*.gz", "*.gz.tbi"] },
    ext_modules = EXT_MODULES,
    test_suite = "test",
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    long_description = """\
April 16, 2014

This module allows fast random access to files compressed with bgzip_ and
indexed by tabix_. It includes a C extension with code from klib_. The bgzip
and tabix programs are available here_.


Installation
------------

::

    pip install --user pytabix


Synopsis
--------

Genomics data is often in a table where each row corresponds to a genomic
region (start, end) or a position:


::

    chrom  pos      snp
    1      1000760  rs75316104
    1      1000894  rs114006445
    1      1000910  rs79750022
    1      1001177  rs4970401
    1      1001256  rs78650406


With tabix_, you can quickly retrieve all rows in a genomic region by
specifying a query with a sequence name, start, and end:


::

    import tabix

    # Open a remote or local file.
    url = "ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20100804/"
    url += "ALL.2of4intersection.20100804.genotypes.vcf.gz"

    tb = tabix.open(url)

    # These queries are identical. A query returns an iterator over the results.
    records = tb.query("1", 1000000, 1250000)

    records = tb.queryi(0, 1000000, 1250000)

    records = tb.querys("1:1000000-1250000")

    # Each record is a list of strings.
    for record in records:
        print record[:5]
        break


::

    ['1', '1000071', '.', 'C', 'T']


.. _bgzip: http://samtools.sourceforge.net/tabix.shtml
.. _tabix: http://samtools.sourceforge.net/tabix.shtml
.. _klib: https://github.com/jmarshall/klib
.. _here: http://sourceforge.net/projects/samtools/files/tabix/

"""
)

