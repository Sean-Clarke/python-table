class Table:
    """A class representing a simple data table consisting of a list of dictionary objects"""
    
    def __init__(self):
        """Initialization method for table class"""
        self._hdr = []
        self._row = [{'index':0}]
    
    def _update_header_row(self):
        """Updates 0-index row with header names"""
        for row in self._row:
            if row['index'] == 0:
                row.clear()
                row['index'] = 0
                for hdr in self._hdr:
                    row[hdr] = hdr
                break
    
    def add_column(self, h, *args, **kwargs):
        """Adds a new column with header h"""
        self._hdr.append(h)
        self._update_header_row()
        
    def _add_empty_column(self):
        """Returns new column header and adds column to table"""
        h = 'h%s' % str(len(self._hdr) + 1)
        self.add_column(h)
        return h
                
    def append(self, *args, **kwargs):
        """Appends a new row to the table"""
        nwr = {}
        nwr['index'] = (len(self._row) + 1)
        for k,v in kwargs.items():
            if not k in self._hdr:
                self.add_column(k)
            nwr[k] = v
        _arg = iter(args)
        for hdr in self._hdr:
            if not hdr in nwr:
                nwr[hdr] = next(_arg)
        for arg in _arg:
            h = self._add_empty_column()
            nwr[h] = arg
        self._row.append(nwr)
