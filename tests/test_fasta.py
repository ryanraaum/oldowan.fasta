from oldowan.fasta.fasta import fasta

import os

SIMPLE_TEXT = """
> indian
TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACAGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCCTCAACTATCACACATCAACTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTTAACAGTACATAGTACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGCCCCCATGGATGACCCCCCTCA
> ethiopian
TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACGGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCTTCAACTATCACACATCACCTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTTAACAGTACATAGCACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGCCCCCATGGATGACCCCCCTCA
"""

SIMPLE_FILEPATH = os.path.join(os.path.dirname(__file__), 
        'test_files', 'simple.fasta')


def test_read_fasta_from_string():
    """read fasta given a string of fasta data"""

    # 's' is the 'string' mode
    ff = fasta(SIMPLE_TEXT, 's')
    entries = ff.readentries()
    ff.close()
    print entries
    assert 2 == len(entries)

    assert isinstance(entries[0], dict)
    assert 'indian' == entries[0]['name']
    assert 360 == len(entries[0]['sequence'])

    assert isinstance(entries[1], dict)
    assert 'ethiopian' == entries[1]['name']
    assert 360 == len(entries[1]['sequence'])


def test_read_fasta_from_file():
    """read fasta given a filename"""
    
    # first, explicitly tell it this is a filename
    ff = fasta(SIMPLE_FILEPATH, 'r')
    entries = ff.readentries()
    ff.close()
    assert 2 == len(entries)

    assert isinstance(entries[0], dict)
    assert 'indian' == entries[0]['name']
    assert 360 == len(entries[0]['sequence'])

    assert isinstance(entries[1], dict)
    assert 'ethiopian' == entries[1]['name']
    assert 360 == len(entries[1]['sequence'])
    
    
def test_read_fasta_from_file():
    """read fasta given an open file"""
    
    f = open(SIMPLE_FILEPATH, 'r')
    ff = fasta(f, 'f')
    entries = ff.readentries()
    ff.close()
    assert 2 == len(entries)

    assert isinstance(entries[0], dict)
    assert 'indian' == entries[0]['name']
    assert 360 == len(entries[0]['sequence'])

    assert isinstance(entries[1], dict)
    assert 'ethiopian' == entries[1]['name']
    assert 360 == len(entries[1]['sequence'])


def test_iterate_fasta_with_parsing():
    """iterate fasta with parsing"""
    # first, from a string of fasta data
    for entry in fasta(SIMPLE_TEXT, 's'):
        assert isinstance(entry, dict)
    # next, from a filename with fasta data
    for entry in fasta(SIMPLE_FILEPATH):
        assert isinstance(entry, dict)


def test_iterate_fasta_without_parsing():
    """iterate fasta without parsing"""
    # first, from a string of fasta data
    for entry in fasta(SIMPLE_TEXT, 's', parse=False):
        assert isinstance(entry, str)
    # next, from a filename with fasta data
    for entry in fasta(SIMPLE_FILEPATH, 'r', parse=False):
        assert isinstance(entry, str)

