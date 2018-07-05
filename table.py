class Table:
    """A class representing a simple data table consisting of a list of dictionary objects"""
    
    def __init__(self, index='index', show_index=True, width=False, height=False):
        """Initialization special method for table class"""
        self.display_index = show_index
        self.index = index
        self._hdr = []
        self._row = [{self.index:0}]
        self.width = width
        self.height = height
        self.max_row = False
        self.max_col = False
        
    def __repr__(self):
        """String representation special method for table class"""
        st = ''
        sp = ' ' * (max([max([max([len(str(v)) for v in tu]) for tu in rw.items()]) for rw in self._row])) + ' '
        if len(sp) % 2 == 1:
            sp += ' '
        _hdr = self._hdr
        if self.display_index:
            _hdr = [self.index] + _hdr
        for row in self._row:
            st += ' '
            for hdr in _hdr:
                cl = str(row[hdr])
                if len(cl) % 2 == 1:
                    cl += ' '
                bf = (len(sp) - len(cl)) // 2
                bf = ' ' * bf
                cl = bf + cl + bf
                st += cl
            st += '\n'
        return st
    
    def _update_hdr_row(self):
        """Updates 0-index row with header names"""
        for row in self._row:
            if row[self.index] == 0:
                row.clear()
                row[self.index] = 0
                for hdr in self._hdr:
                    row[hdr] = hdr
                break
    
    def _add_empty_col(self):
        """Returns new column header and adds column to table"""
        h = 'h%s' % str(len(self._hdr) + 1)
        self.add_col(h)
        return h
        
    def show_index(self):
        """Changes tables display_index attribute to True, displaying index column and values when printed"""
        self.display_index = True
        
    def hide_index(self):
        """Changes tables display_index attribute to False, hiding index column and values when printed"""
        self.display_index = False
        
    def show_headers(self):
        pass
        
    def hide_headers(self):
        pass
        
    def get_col(self, h, index=True):
        """Returns values from all rows from the h value column"""
        if h in self._hdr:
            return [rw[h] for rw in self._row if index == True or rw[self.index] != 0]
        else:
            print("No column in table with header: %s" % h)
        
    def get_row(self, index=-1, **kwargs):
        """Either returns row with given index value, or returns rows matching all given key-value pairs"""
        if index >= 0:
            return list(filter(lambda row: row[self.index] == index, self._row))
        elif kwargs:
            sift = self._row
            for k,v in kwargs.items():
                sift = filter(lambda row: row[k] == v, sift)
            return list(sift)
        else:
            print("get_row() requires either row index or at least 1 key-value pair.")
                
        
    def get_headers(self):
        return self._hdr
    
    def get_width(self):
        return len(self._hdr)
        
    def get_height(self):
        return len(self._row)
        
    def get_max_row(self):
        return self.max_row
        
    def get_max_col(self):
        return self.max_col
        
    def get_dim(self):
        return (self.get_width(),self.get_height())
        
    def set_width(self):
        pass
        
    def set_height(self):
        pass
        
    def set_max_col(self):
        pass
        
    def set_max_row(self):
        pass
    
    def rnm_col(self, h):
        pass
    
    def add_col(self, h, *args, **kwargs):
        """Adds a new column with header h"""
        self._hdr.append(h)
        self._update_hdr_row()
        for row in self._row:
            if h not in row:
                row[h] = 'null'
    
    def add_row(self, *args, **kwargs):
        """Appends a new row to the table"""
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
        """Removes columns with given header names"""
        for arg in args:
            self._hdr.remove(arg)
            for row in self._row:
                del row[arg]
        
    def rmv_row(self, *args):
        pass
    
    def add_cell(self, *args, **kwargs):
        pass
        
    def rmv_cell(self, *args, **kwargs):
        pass
        
    def compare_rows(self, *args, **kwargs):
        """Given filters as either row indeces, or key-value identifiers, compares rows meeting given filters"""
        pass
        
    def merge(self, new, mergetpye='inclusive'):
        """Merges new (table) with calling table"""
        pass
        
    def split():
        pass
    
    def sub():
        pass
