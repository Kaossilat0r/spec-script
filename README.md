script
===========

Quick and dirty Python 3 script to utilize results from the spec omp

### Requirements
* Python3
* matplotlib
* (numpy)


### on matplotlib / numpy
If you struggle with matplotlib on win7 x64 as I did too ... this is what finally worked for me.
* download and install matplotlib binary from: http://cznic.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.3.1/matplotlib-1.3.1.win-amd64-py3.3.exe
*  run ```pip install pyparsing```
*  download and install an unofficial numpy binary from: http://www.lfd.uci.edu/~gohlke/pythonlibs/gmqofism/numpy-MKL-1.8.0.win-amd64-py3.3.exe
*  pray to Monty Python


### Running
```python results.py PATH/TO/SPEC/RESULTS/DIRECTORY```
* Directory should be sth. like ```SPEC_OMP/result/```
* The script does not have much error handling, so you better provide valid paths..

###Generates
* Statistical information to stdout
* Figures for Runtime, Speedup and Efficiency to ```./results```
