import re
import StringIO

class fasta(object):
    """fasta(filename_or_data[, mode[, parse]]) -> a fasta object.

    Create a fasta object. The mode can be 'r' (reading, default), 
    's' (string data), 'f' (file object), 'a' (append), or 'w' (write).
    The file will be created if it doesn't exist for writing or appending;
    it will be truncated when opened for reading. For read mode, 
    universal newline support is automatically invoked. By default, each
    FASTA entry is parsed into a dict with 'name' and 'sequence'
    values (parse=True). For 'raw' strings, set parse=False."""

    __parse = True
    def __get_parse(self):
        return self.__parse
    def __set_parse(self, value):
        if not isinstance(value, bool):
            raise ValueError("'%s' is not a boolean." % value)
        self.__parse = value
    parse = property(fget=__get_parse,
                     fset=__set_parse,
                     doc="parse entry into dict (default=True)")

    __mode = None
    def __get_mode(self):
        return self.__mode
    mode = property(fget=__get_mode,
                    doc="file mode ('r', 's', 'f', 'w', or 'a')")

    def __get_closed(self):
        return self.__fobj.closed
    closed = property(fget=__get_closed,
                      doc="True if the file is closed")

    __fobj = None
    __buff = 'x' # needs to be initialized with non-zero, non-'>' character

    def __init__(self, filename_or_data, mode='r', parse=True):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        if mode[0] in ['r', 'a', 'w']:
            if mode == 'r': 
                # force universal read mode
                mode = 'rU' 
            self.__fobj = open(filename_or_data, mode)
        elif mode == 'f':
            self.__fobj = filename_or_data
        elif mode == 's':
            self.__fobj = StringIO.StringIO(filename_or_data)
        else:
            msg = "mode string must start with 'r', 'a', 'w', 'f' or 's', \
                    not '%s'" % mode[0]
            raise ValueError(msg)
        self.__mode = mode
        self.parse = parse

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        return self

    def __enter__(self):
        """__enter__() -> self."""
        return self

    def __exit__(self, type, value, traceback):
        """__exit__(*excinfo) -> None.  Closes the file."""
        self.__fobj.close()

    def close(self):
        """close() -> None or (perhaps) an integer.  Close the file."""
        return self.__fobj.close()

    def flush(self):
        """flush() -> None.  Flush the internal I/O buffer."""
        return self.__fobj.flush()

    def next(self):
        """next() -> the next entry, or raise StopIteration"""
        nxt = self.readentry()
        if nxt is None:
            self.__fobj.close()
            raise StopIteration
        return nxt

    def read(self):
        """read() -> list of dict entries, reads the remainder of the data.

        Equivalent to readentries()."""
        return self.readentries()

    def readentry(self):
        """readentry() -> next entry, as a dict.
        
        Return None at EOF."""
        # read until the start of the next entry
        while not self.__buff.startswith('>'): 
            self.__buff = self.__fobj.readline()
            if self.__buff == '':
                # EOF
                return None

        current = []
        current.append(self.__buff)
        self.__buff = self.__fobj.readline()
        while not self.__buff.startswith('>') and self.__buff != '':
            current.append(self.__buff)
            self.__buff = self.__fobj.readline()

        current_str = ''.join(current)
        if self.parse:
            return parse_fasta(current_str)
        return(current_str)
        
    def readentries(self):
        """readentries() -> list of entries, each a dict.

        Call readentry() repeatedly and return a list of the entries read."""
        return list(x for x in self)
    
    def write(self, entry, wrap_at=80, endline='\n'):
        """write(entry) -> None. Write entry dict to file.

        argument dict 'entry' must have keys 'name' and 'sequence', both
        with string values."""
        if isinstance(entry, dict):
            if name.has_key('name') and name.has_key('sequence'):
                self.__fobj.write(entry2str(entry, wrap_at, endline))
        else:
            raise ValueError('either name or sequence of incorrect type')

    def writeentries(self, entries):
        """writeentries(entries) -> None. Write list of entries to file.

        The equivalent of calling write for each entry."""
        for entry in entries:
            self.write(entry)


def parse_fasta(entry):
    """parse_fasta(entry) -> dict. entry is a string. 
    
    Parse a string representation of a single FASTA entry into a dict.
    The returned dict has values for 'name' and 'sequence'."""
    if not entry.startswith('>'):
        raise TypeError("entry does not start with '>'")

    # the entry must include at least two lines (a label and a sequence)
    lines = re.split(r'[\r\n]+', entry)
    if len(lines) < 2:
        raise TypeError("entry needs at least two lines")

    # name is everything on the first line after the '>'
    name = lines.pop(0)[1:].strip()
    # sequence is the rest of the entry
    sequence = ''.join(lines)

    return {'name': name, 'sequence': sequence}


def entry2str(entry, wrap_at=80, endline='\n'):
    """entry2str(entry[, wrap_at[, endline]]) -> a string. entry is a dict.

    Given an entry dict with string values for 'name' and 'sequence', will
    return a string in FASTA format. 'endline's (default \\n) will be inserted
    into the sequence every 'wrap_at' characters (default 80)."""
    s = []
    s.append('>%s%s' % (entry['name'], endline))
    # for the wrapping, DON'T use 'textwrap.wrap'. It is very slow because
    # it tries to be clever and find word breaks to wrap at.
    exploded_seq = list(entry['sequence'])
    wrap_points = range(0,len(exploded_seq),wrap_at)
    wrap_points.reverse()
    for i in wrap_points[:-1]:
        exploded_seq.insert(i, '\n')
    s = s + exploded_seq + ['\n']
    return ''.join(s)
    
