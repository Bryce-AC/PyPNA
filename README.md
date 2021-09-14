# PyPNA
Interfacing Keysight PNA with Python.
This library is a work in progress.

Install: `pip install PyPNA`

Commands from: http://na.support.keysight.com/pna/help/latest/Programming/XComFinderSet.htm

Guide: https://towardsdatascience.com/deep-dive-create-and-publish-your-first-python-library-f7f618719e14

## Todo
- Configure the PNA (run once)
  - Connect, load setup file, etc
- Read S11 and S21
  - Return numpy array (complex and frequency data)
  - Support averaging
