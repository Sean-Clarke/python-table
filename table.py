class Table:
    """A class representing a simple data table consisting of a list of dictionary objects."""
    
    def __init__(self, *args, index='index', show_index=True, width=False, height=False, **kwargs):
        """Initialization special method for table class."""
        self.display_index = show_index
        self.display_headers = True
        self.index = index
        self._hdr = []
        self._row = [{self.index:0}]
        self.width = width
        self.height = height
        self.display_width = width
        self.display_height = height
        if args and len(args) == 1:
            if type(args[0]) == str:
                if '\n' in args[0]:
                    lines = args[0].split('\n')
                    headers = lines[0].split(',')
                    for line in lines[1:]:
                        cells = iter(line.split(','))
                        row = {}
                        for header in headers:
                            row[header] = next(cells, None)
                        self.add_row(**row)
            elif type(args[0]) == list:
                for row in args[0]:
                    self.add_row(**row)

    def __repr__(self):
        """String representation special method for table class."""
        st = '\n'
        if len(self._hdr) == 0 and len(self._row) <= 1:
            st += 'Empty Table\n'
            return st
        dw = None
        dh = None
        if self.display_width:
            dw = self.display_width
        if self.display_height:
            dh = self.display_height
        _hdr = self._hdr[:dw]
        _row = self._row
        if self.display_index:
            _hdr = [self.index] + _hdr
            if dw:
                _hdr = _hdr[:-1]    
        if not self.display_headers:
            _row = _row[1:]
            if dh:
                _row = _row[:dh]
        else:
            _row = _row[:dh]
            _row[0][self.index] = self.index
        sz = {}
        for hdr in _hdr:
            lng = 0
            for row in _row:
                lng = max(len(str(row[hdr])), lng)
            sz[hdr] = lng
        tl = ' |'
        for k,v in sz.items():
            tl += '--' + '-' * (v + 2) + '|'
        st += tl
        st += '\n'
        for row in _row:
            st += ' '
            st += '|  '
            for hdr in _hdr:
                cl = str(row[hdr])
                cl += ' ' * (sz[hdr] + 2 - len(cl))
                cl += '|'
                cl += '  '
                st += cl
            st += '\n'
            tl = ' |'
            for k,v in sz.items():
                tl += '--' + '-' * (v + 2) + '|'
            st += tl
            st += '\n'
        return st
        
    def __getitem__(self, *args):
        """Get item special method for table class"""
        out = {}
        while type(args) == tuple:
            args = list(args)
            if type(args[0]) == tuple: 
                args = args[0]
        print(args)
        for kw in args:
            k,v = kw.split('=')
            out[k]=v
            print(out)
        rows = self.get_row(**out)
        print(rows)
        if len(rows) == 1:
            return rows[0]
        else:
            for row in rows:
                sc = dict(row)
                i = rows.index(row)
                sc.pop(self.index)
                rows[i] = sc
            return Table(rows)
    
    def _update_hdr_row(self):
        """Updates 0-index row with header names."""
        for row in self._row:
            if row[self.index] == 0:
                row.clear()
                row[self.index] = 0
                for hdr in self._hdr:
                    row[hdr] = hdr
                break
    
    def _add_empty_col(self):
        """Returns new column header and adds column to table."""
        h = 'h%s' % str(len(self._hdr) + 1)
        self.add_col(h)
        return h
        
    def show_index(self):
        """Changes tables display_index attribute to True, displaying index column and values when printed."""
        self.display_index = True
        
    def hide_index(self):
        """Changes tables display_index attribute to False, hiding index column and values when printed."""
        self.display_index = False
        
    def show_headers(self):
        """Changes tables display_headers attribute to True, displaying header row and values when printed."""
        self.display_headers = True
        
    def hide_headers(self):
        """Changes tables display_headers attribute to False, hiding header row and values when printed."""
        self.display_headers = False
        
    def get_col(self, h, index=True):
        """Returns values from all rows from the h value column."""
        if h in self._hdr:
            return [rw[h] for rw in self._row if index == True or rw[self.index] != 0]
        else:
            print("No column in table with header: %s" % h)
        
    def get_row(self, index=-1, **kwargs):
        """Either returns row with given index value, or returns rows matching all given key-value pairs."""
        if index >= 0:
            return list(filter(lambda row: row[self.index] == index, self._row))
        elif kwargs:
            sift = self._row
            for k,v in kwargs.items():
                sift = filter(lambda row: row[k] == v, sift)
                print(list(sift))
            return list(sift)
        else:
            print("get_row() requires either a row index or at least 1 key-value pair.")
                
        
    def get_headers(self):
        """Returns this object's headers."""
        return self._hdr
    
    def get_width(self):
        """Returns this object's width property."""
        return len(self._hdr)
        
    def get_height(self):
        """Returns this object's height property."""
        return len(self._row)
        
    def get_display_width(self):
        """Returns this object's display_width property."""
        return self.display_width
        
    def get_display_height(self):
        """Returns this object's display_height property."""
        return self.display_height
        
    def get_dim(self):
        """Returns this object's dimensions."""
        return (self.get_width(),self.get_height())
        
    def set_width(self, w):
        """Sets this object's width property to given int w"""
        self.width = int(w)
        
    def set_height(self, h):
        """Sets this object's height property to given int h"""
        self.height = int(h)
        
    def set_display_width(self, dw):
        """Sets this object's display_width property to given int dw"""
        self.display_width = int(dw)
        
    def set_display_height(self, dh):
        """Sets this object's display_height property to given int dh"""
        self.display_height = int(dh)
    
    def rnm_col(self, **kwargs):
        if kwargs:
            for k,v in kwargs.items():
                if k in self._hdr:
                    self._hdr[self._hdr.index(k)] = v
                    for row in self._row:
                        row[v] = row[k]
                        del row[k]
                        self._update_hdr_row()
                else:
                    print("Given non-existent header to rename: %s" % k)
        else:
            print("rnm_col only takes kv pair arguments eg. rnm_col(title=name)")
            return
    
    def add_col(self, h=False, *args, **kwargs):
        """Adds a new column with header h."""
        if h:
            self._hdr.append(h)
            self._update_hdr_row()
            _arg = iter([])
            if kwargs:
                for k,v in kwargs.items():
                    for row in self._row:
                        if row[k] == v[0]:
                            row[h] = v[1]
            if args:
                _arg = iter(args)
            for row in self._row:
                if h not in row:
                    row[h] = next(_arg, None)
            for arg in _arg:
                kw={h:arg}
                self.add_row(**kw)
        elif kwargs:
            for k,v in kwargs.items():
                self._hdr.append(k)
                self._update_hdr_row()
                for row in self._row[1:]:
                    row[k] = v
        else:
            h = 'h%s' % str(len(self._hdr) + 1)
            self.add_col(h)
            
    
    def add_row(self, *args, **kwargs):
        """Appends a new row to the table."""
        nwr = {}
        nwr[self.index] = len(self._row)
        for k,v in kwargs.items():
            if not k in self._hdr:
                self.add_col(k)
            nwr[k] = v
        _arg = iter(args)
        for hdr in self._hdr:
            if not hdr in nwr:
                nwr[hdr] = next(_arg, None)
        for arg in _arg:
            h = self._add_empty_col()
            nwr[h] = arg
        self._row.append(nwr)
        
    def rmv_col(self, *args):
        """Removes columns with given header names."""
        for arg in args:
            self._hdr.remove(arg)
            for row in self._row:
                del row[arg]
        
    def rmv_row(self, *args, exclude_ind=False, exclude_kv=False, style_kv='strict', **kwargs):
        """Removes rows with given indexes and/or those with matching key-value pairs."""
        if exclude_ind:
            # remove rows with indexes not in *args
            if exclude_kv:
                # remove rows with indexes not in *args that don't match kv pairs
                if style_kv=='strict':
                    # remove rows with indexes not in *args that don't match every kv pair
                    if args:
                        if kwargs:
                            pass
                        else:
                            print("No rows removed, as no kv pair was given")
                            return
                    elif kwargs:
                        print("No rows removed, as no index was given")
                        return
                    else:
                        print("rmv_row() was given no required arguments")
                        return
                elif style_kv=='soft':
                    # remove rows with indexes not in *args that don't match any kv pair
                    if args:
                        if kwargs:
                            pass
                        else:
                            print("No rows removed, as no kv pair was given")
                            return
                    elif kwargs:
                        print("No rows removed, as no index was given")
                        return
                    else:
                        print("rmv_row() was given no required arguments")
                        return
                else:
                    print("Invalid style_kv given: %s, try 'strict' or 'soft'" % style_kv)
                    return
            else:
                # remove rows with indexes not in *args that match kv pairs
                if style_kv=='strict':
                    # remove rows with indexes not in *args that match every kv pair
                    if args:
                        if kwargs:
                            pass
                        else:
                            print("No rows removed, as no kv pair was given")
                            return
                    elif kwargs:
                        pass
                    else:
                        print("rmv_row() was given no required arguments")
                        return
                elif style_kv=='soft':
                    # remove rows with indexes not in *args that match any kv pair
                    if args:
                        if kwargs:
                            pass
                        else:
                            print("No rows removed, as no kv pair was given")
                            return
                    elif kwargs:
                        pass
                    else:
                        print("rmv_row() was given no required arguments")
                        return
                else:
                    print("Invalid style_kv given: %s, try 'strict' or 'soft'" % style_kv)
                    return
        elif exclude_kv:
            # remove rows with indexes in *args that don't match kv pairs
            if style_kv=='strict':
                # remove rows with indexes in *args that don't match every kv pair
                if args:
                    if kwargs:
                        pass
                    else:
                        for row in self._row:
                            if row[self.index] in args:
                                self._row.remove(row)
                elif kwargs:
                    print("No rows removed, as no index was given")
                    return
                else:
                    print("rmv_row() was given no required arguments")
                    return
            elif style_kv=='soft':
                # remove rows with indexes in *args that don't match any kv pair
                if args:
                    if kwargs:
                        pass
                    else:
                        for row in self._row:
                            if row[self.index] in args:
                                self._row.remove(row)
                elif kwargs:
                    print("No rows removed, as no index was given")
                    return
                else:
                    print("rmv_row() was given no required arguments")
                    return
            else:
                print("Invalid style_kv given: %s, try 'strict' or 'soft'" % style_kv)
                return
        else:
            # remove rows with indexes in *args that match kv pairs
            if style_kv=='strict':
                # DEFAULT: remove rows with indexes in *args and those that match every given kv pair
                if args:
                    if kwargs:
                        pass
                    else:
                        for row in self._row:
                            if row[self.index] in args:
                                self._row.remove(row)
                elif kwargs:
                    pass
                else:
                    print("rmv_row() was given no required arguments")
                    return
            elif style_kv=='soft':
                # remove rows with indexes in *args and those that match any given kv pair
                if args:
                    if kwargs:
                        pass
                    else:
                        for row in self._row:
                            if row[self.index] in args:
                                self._row.remove(row)
                elif kwargs:
                    pass
                else:
                    print("rmv_row() was given no required arguments")
                    return
            else:
                print("Invalid style_kv given: %s, try 'strict' or 'soft'" % style_kv)
                return
                
    def set_column(self, col):
        """ """
        pass
    
    def set_row(self, row):
        """ """
        pass
    
    def clear_table(self, keep_hdr=False):
        """Deletes all rows from table; if keep_hdr gets passed True, the header row and data is kept."""
        self._row = [{self.index:0}]
        if keep_hdr:
            self._update_hdr_row()
        else:
            self._hdr = []
    
    def add_cell(self, *args, **kwargs):
        pass
        
    def rmv_cell(self, *args, **kwargs):
        pass
        
    def map_col(self, h, f):
        """Given header h and function f, returns """
        pass
        
    def compare_rows(self, *args, **kwargs):
        """Given filters as either row indexes, or key-value identifiers, compares rows meeting given filters."""
        pass
        
    def merge(self, new, mergetpye='union'):
        """Merges new (table) with calling table."""
        pass
        
    def split(method='default', **kwargs):
        """
        Splits the table into two or more tables by the designated method; options for method are:
        'default':
        'ilimits': Given, atleast one index or k,v pair, table is split at each given index, or each time the k,v pair is matched, returning tables maintaining the number of columns in the calling table.
        'hlimits': Given, atleast one header, table is split at each header, returning number of headers given + 1 tables maintaining the number of rows in the calling table.
        'col': Given n, returns n ~equally sized tables representing n sections of columns from the original table. Given a negative number, table is split into single column tables. Given no argument, table is split in half. 
        'row': Given n, returns n ~equally sized tables representing n sections of rows from the original table. Given a negative number, table is split into single row tables. Given no argument, table is split in half. 
        """
        pass
    
    def sub(self):
        """Returns a subset of the table for which the given function is true"""
        pass
        
    def fill_empty(self, v, row=[], col=[], method='union'):
        """
        Replaces all None values in the specified columns(by header) and rows(by index or k=v pair) with the given value v.
        If no rows or columns are specified, all None values in the table are replaced; options for method are:
        'union': values replaced can be from either any specified row, or any specified column
        'intersection': values replaced must be in both a specified row and column
        """
        pass
        
    def import_from(self):
        pass
