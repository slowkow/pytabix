pytabix
=======

This module allows fast random access to sorted files compressed with bgzip_ and
indexed by tabix_. It includes a C extension with code from klib_. The bgzip
and tabix programs are available here_.

Alternatives: 

- Instead of using this module, you can install tabix_ yourself and
  easily call it from Python as shown at the bottom of this page.
  
- pysam_ - A python module for reading and manipulating Samfiles.
  It's a lightweight wrapper of the samtools C-API.
  Pysam also includes an interface for tabix_.

- hts-python_ - A pythonic wrapper for htslib_ C-API using python cffi_.

.. _pysam: https://github.com/pysam-developers/pysam
.. _hts-python: https://github.com/brentp/hts-python
.. _htslib: https://github.com/samtools/htslib
.. _cffi: https://cffi.readthedocs.org


Synopsis
--------

Open a local or remote file that has already been sorted, compressed, and indexed:

.. code:: python

    import tabix

    url = "ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20100804/"
    url += "ALL.2of4intersection.20100804.genotypes.vcf.gz"

    tb = tabix.open(url)

    records = tb.query("1", 1000000, 1250000)
    records = tb.queryi(0, 1000000, 1250000)
    records = tb.querys("1:1000000-1250000")

    for record in records:
        print record[:3]

.. code:: python

    ['1', '1000760', 'rs75316104']
    ['1', '1000760', 'rs75316104']
    ['1', '1000894', 'rs114006445']
    ['1', '1000910', 'rs79750022']
    ['1', '1001177', 'rs4970401']
    ['1', '1001256', 'rs78650406']


Install
-------

.. code:: bash

    pip install --user pytabix

or

.. code:: bash

    wget https://pypi.python.org/packages/source/p/pytabix/pytabix-0.1.tar.gz
    tar xf pytabix-0.1.tar.gz
    cd pytabix-0.1
    python setup.py install --user

How to prepare a file for `tabix`
---------------------------------

1. Sort_ the file by chromosome, start, and end.
2. Compress the file with bgzip_.
3. Index the compressed file with tabix_.

.. code:: bash

    $ head -n5 example.bed | column -t
    chr19  53611131   53636172   ZNF415
    chr10  72149121   72150375   CEP57L1P1
    chr4   185009858  185139113  ENPP6
    chrX   132669772  133119672  GPC3
    chr6   134924279  134925376  FAM8A6P

1. Sort_ it by chromosome, start, and end.
2. Then, use bgzip_ to deflate the file into compressed blocks:

.. code:: bash

    $ sort -k1V -k2n -k3n example.bed | bgzip > example.bed.gz

3. Index the compressed file with tabix_:

.. code:: bash

    $ tabix -s 1 -b 2 -e 3 example.bed.gz
    
    $ ls
    example.bed  example.bed.gz  example.bed.gz.tbi


Alternative: Use `subprocess`
-----------------------------

.. code:: python

    from subprocess import Popen, PIPE
    
    def bgzip(filename):
        """Call bgzip to compress a file."""
        Popen(['bgzip', '-f', filename])
    
    def tabix_index(filename,
            preset="gff", chrom=1, start=4, end=5, skip=0, comment="#"):
        """Call tabix to create an index for a bgzip-compressed file."""
        Popen(['tabix', '-p', preset, '-s', chrom, '-b', start, '-e', end,
            '-S', skip, '-c', comment])
    
    def tabix_query(filename, chrom, start, end):
        """Call tabix and generate an array of strings for each line it returns."""
        query = '{}:{}-{}'.format(chrom, start, end)
        process = Popen(['tabix', '-f', filename, query], stdout=PIPE)
        for line in process.stdout:
            yield line.strip().split()


.. _bgzip: http://samtools.sourceforge.net/tabix.shtml
.. _tabix: http://samtools.sourceforge.net/tabix.shtml
.. _klib: https://github.com/jmarshall/klib
.. _here: http://sourceforge.net/projects/samtools/files/tabix/
.. _Sort: https://www.gnu.org/software/coreutils/manual/html_node/Details-about-version-sort.html#Details-about-version-sort
