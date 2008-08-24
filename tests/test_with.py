from __future__ import with_statement

import os

from oldowan.fasta.fasta import fasta

SIMPLE_FILEPATH = os.path.join(os.path.dirname(__file__), 
        'test_files', 'simple.fasta')

def test_with():
    """test of with statement hooks"""
    with fasta(SIMPLE_FILEPATH, 'r') as f:
        for entry in f:
            assert isinstance(entry, dict)
    assert f.closed
