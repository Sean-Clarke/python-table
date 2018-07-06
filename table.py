class Table:
    """A class representing a simple data table consisting of a list of dictionary objects."""
    
    def __init__(self, index='index', show_index=True, width=False, height=False):
        """Initialization special method for table class."""
        self.display_index = show_index
        self.display_headers = True
        self.index = index
        self._hdr = []
        self._row = [{self.index:0}]
        self.width = width
        self.height = height
        self.max_row = False
        self.max_col = False

    def __repr__(self):
        """String representation special method for table class."""
        st = '\n'
        if len(self._hdr) == 0 and len(self._row) <= 1:
            st += 'Empty Table\n'
            return st
        _hdr = self._hdr
        _row = self._row
        if self.display_index:
            _hdr = [self.index] + _hdr
        if not self.display_headers:
            _row = _row[1:]
        sz = {}
        for hdr in _hdr:
            lng = 0
            for row in _row:
                lng = max(len(str(row[hdr])), lng)
            sz[hdr] = lng
        if self.display_headers:
            tl = ' |'
            for k,v in sz.items():
                tl += '--' + '-' * (v + 2) + '|'
            st += tl
            st += '\n'
        for row in _row:
            st += ' '
            if self.display_headers:
                st += '|  '
            for hdr in _hdr:
                cl = str(row[hdr])
                cl += ' ' * (sz[hdr] + 2 - len(cl))
                if self.display_headers:
                    cl += '|'
                cl += '  '
                st += cl
            st += '\n'
            if row[self.index] == 0:
                tl = ' |'
                for k,v in sz.items():
                    tl += '--' + '-' * (v + 2) + '|'
                st += tl
                st += '\n'
        if self.display_headers:
            tl = ' |'
            for k,v in sz.items():
                tl += '--' + '-' * (v + 2) + '|'
            st += tl
        return st
    
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
            return list(sift)
        else:
            print("get_row() requires either a row index or at least 1 key-value pair.")
                
        
    def get_headers(self):
        """Returns this object's headers."""
        return self._hdr
    
    def get_width(self):
        """Returns this object's width."""
        return len(self._hdr)
        
    def get_height(self):
        """Returns this object's height."""
        return len(self._row)
        
    def get_max_row(self):
        """Returns this object's max_row."""
        return self.max_row
        
    def get_max_col(self):
        """Returns this object's max_col."""
        return self.max_col
        
    def get_dim(self):
        """Returns this object's dimensions."""
        return (self.get_width(),self.get_height())
        
    def set_width(self, w):
        self.width = w
        
    def set_height(self, h):
        self.height = h
        
    def set_max_col(self, clim):
        self.max_col = clim
        
    def set_max_row(self, rlim):
        self.max_row = rlim
    
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
                    row[h] = next(_arg, 'null')
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
                nwr[hdr] = next(_arg, 'null')
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
        
    def compare_rows(self, *args, **kwargs):
        """Given filters as either row indexes, or key-value identifiers, compares rows meeting given filters."""
        pass
        
    def merge(self, new, mergetpye='inclusive'):
        """Merges new (table) with calling table."""
        pass
        
    def split():
        pass
    
    def sub():
        pass
