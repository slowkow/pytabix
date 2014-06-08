pytabix
=======

This module allows fast random access to files compressed with bgzip_ and
indexed by tabix_. It includes a C extension with code from klib_. The bgzip
and tabix programs are available here_.


Synopsis
--------

Prepare a table for tabix:

.. code:: bash

    $ head -n5 example.bed | column -t
    chr19  53611131   53636172   ZNF415
    chr10  72149121   72150375   CEP57L1P1
    chr4   185009858  185139113  ENPP6
    chrX   132669772  133119672  GPC3
    chr6   134924279  134925376  FAM8A6P

Sort_ it by chromosome, start, and end. Then, use bgzip_ to
deflate the file into compressed blocks:

.. code:: bash

    $ sort -k1V -k2n -k3n example.bed | bgzip > example.bed.gz

Index the compressed file with tabix_:

.. code:: bash

    $ tabix -s 1 -b 2 -e 3 example.bed.gz
    
    $ ls
    example.bed  example.bed.gz  example.bed.gz.tbi

Open a local or remote file that has already been indexed:

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


.. _bgzip: http://samtools.sourceforge.net/tabix.shtml
.. _tabix: http://samtools.sourceforge.net/tabix.shtml
.. _klib: https://github.com/jmarshall/klib
.. _here: http://sourceforge.net/projects/samtools/files/tabix/
.. _Sort: https://www.gnu.org/software/coreutils/manual/html_node/Details-about-version-sort.html#Details-about-version-sort
