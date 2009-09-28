"""This is the oldowan.fasta package."""


import os

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
               'VERSION')).read().strip()

__all__ = ['fasta',
           'parse_fasta',
           'entry2str']

try:
    from oldowan.fasta.fasta import fasta
    from oldowan.fasta.fasta import parse_fasta
    from oldowan.fasta.fasta import entry2str
except:
    from fasta import fasta
    from fasta import parse_fasta
    from fasta import entry2str
