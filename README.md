# Python Table Class
Simple custom python Table class

Version: beta

## Getting Started

### Prerequisites
Python 3+

### Installation
From 'Clone or download' above, select 'Download ZIP'. After download is complete, unpack files into local directory, navigate to this directory in cmd, and run: ```python setup.py install``` 

## Using the Table

### Basic Examples
```
#!/usr/bin/env python
from table import Table

t = Table()

t.add_row(year=2018, host='Korea', city='Pyeongchang', season='winter')
t.add_row(year=2016, host='Brazil', city='Rio de Janeiro', season='summer')
t.add_row(year=2014, host='Russia', city='Sochi', season='winter')
t.add_row(year=2012, host='United Kingdom', city='London', season='summer')
t.add_row(year=2010, host='Canada', city='Vancouver', season='winter')

print(t)
```
### Table Properties
width:

height:

display_width:

display_height:


### Table Methods
add_col()

add_row()

rmv_col()

rmv_row()

rnm_col

## Information

### Data Structure
The table is essentially a list of dictionary objects.

### Why use it
You want a simple hackable python table class.

### Contributing
If you want to become a co-author, please fork the project and send me some push/pull requests that I can review. Acknowledgments go out to whoever contributes concepts, testing, bug alerts, etc, however, doesn't contribute any code.

## Authors
Sean Clarke

## License
This project is held under no license that I am aware of. Feel free to use it. However, I take no responsibility for whatever outcome there is to your use.

## Acknowledgements
