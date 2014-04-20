pytabix
=======

Hyeshik Chang, Kamil Slowikowski

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
region (start, end) or a position::

    chrom  pos      snp
    1      1000760  rs75316104
    1      1000894  rs114006445
    1      1000910  rs79750022
    1      1001177  rs4970401
    1      1001256  rs78650406

With tabix_, you can quickly retrieve all rows in a genomic region by
specifying a query with a sequence name, start, and end:

.. code:: python

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

.. code:: python

    ['1', '1000760', 'rs75316104']
    ['1', '1000760', 'rs75316104']
    ['1', '1000894', 'rs114006445']
    ['1', '1000910', 'rs79750022']
    ['1', '1001177', 'rs4970401']
    ['1', '1001256', 'rs78650406']


Example
-------

Let's say you have a table of gene coordinates:

.. code:: bash

    $ zcat example.bed.gz | shuf | head -n5 | column -t
    chr19  53611131   53636172   55786   ZNF415
    chr10  72149121   72150375   221017  CEP57L1P1
    chr4   185009858  185139113  133121  ENPP6
    chrX   132669772  133119672  2719    GPC3
    chr6   134924279  134925376  114182  FAM8A6P

Sort_ it by chromosome, then by start and end positions. Then, use bgzip_ to
deflate the file into compressed blocks:

.. code:: bash

    $ zcat example.bed.gz | sort -k1V -k2n -k3n | bgzip > example.bed.bgz

The compressed size is usually slightly larger than that obtained with gzip.

Index the file with tabix_:

.. code:: bash

    $ tabix -s 1 -b 2 -e 3 example.bed.gz
    
    $ ls
    example.bed.gz  example.bed.gz.tbi

.. _bgzip: http://samtools.sourceforge.net/tabix.shtml
.. _tabix: http://samtools.sourceforge.net/tabix.shtml
.. _klib: https://github.com/jmarshall/klib
.. _here: http://sourceforge.net/projects/samtools/files/tabix/
.. _Sort: https://www.gnu.org/software/coreutils/manual/html_node/Details-about-version-sort.html#Details-about-version-sort
