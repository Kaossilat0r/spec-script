'''
Created on 16.04.2014

A script to utilize the results of the spec omp 2001 benchmark
@author: roman
'''
from os import path, listdir

#import numpy as np
import matplotlib.pyplot as plt
"""
if you struggle with matplotlib on win7 x64 :
matplotlib binary: http://cznic.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.3.1/matplotlib-1.3.1.win-amd64-py3.3.exe
then run: pip install pyparsing pyparsing
unofficial numpy binary: http://www.lfd.uci.edu/~gohlke/pythonlibs/gmqofism/numpy-MKL-1.8.0.win-amd64-py3.3.exe
"""

def get_last_column_number(line):
    columns = line.split(" ")
    return columns[-1]

def parse_parameters(filePath):
    """
    parse the parameters of a single result file.
    """
    numThreads, queue, affinity = 0,"",""
    
    for line in open(filePath):
        if "spec.omp2001.size:" in line:
            if get_last_column_number(line)=="test":
                print("IS TEST SIZE!!1 : " + filePath)
        
        if "spec.omp2001.sw_threads:" in line:
            numThreads = int(get_last_column_number(line))
        
        if "spec.omp2001.mach:" in line:
            machine = line.split(" ")[-1]
            columns = machine.split(".")
            
            queue = columns[0]
            affinity = columns[1]
    
    return numThreads, queue, affinity

def parse_single_result(fileName):
    """
    parse results from a single file
    """
    filePath = path.relpath(fileName)
    
    numThreads, queue, affinity = parse_parameters(filePath)

    # parse results
    for line in open(filePath):
        if "reported_time" in line:
            s = line.split(" ")[0]
            
            bench = s.split(".")[3]
            runtime = float(get_last_column_number(line))

            model[affinity][bench][numThreads].append(runtime)
    
    #print("threads:" + str(numThreads) + " affinity:" + str(affinity) + " queue:" + str(queue))

def generate_figure(benchmark, name):
    
    numThreads = []
    runTimes = []
    
    for k in sorted(benchmark.keys()):
        v = benchmark[k]
        if len(v)==0:
            continue
        
        avg = sum(x for x in v) / len(v)
        numThreads.append(k)
        runTimes.append(avg)
  
    # the actual figure
    fig, ax = plt.subplots()
    
    ax.set_title(name)
    ax.axis([0.0, max(numThreads)+1, 0.0, max(runTimes)*1.1])

    ax.plot(numThreads, runTimes, 'black')

    ax.set_xlabel('numThreads')
    ax.set_ylabel('runtime [s]')
    
    plt.savefig('fig.png')

def initialize_model():
    for a in affinities:
        model[a] = {}
        for b in benchmarks:
            model[a][b] = {}
            for t in threads:
                model[a][b][t] = []

def dump_to_console():
    """
    dump model on console for debug reasons
    """  
    print()
    for b in benchmarks:
        print(b)
        for a in affinities:
            print("    "+a)

            for t in threads:
                lst = model[a][b][t]
                
                if len(lst)>0:
                    avg = sum(x for x in lst) / len(lst)
                    print("\t{0}\t{1:.2f}\t{2}".format(t,avg,lst))

if __name__ == '__main__':
    
    affinities = ["scatter", "compact"]
    benchmarks = ["310_wupwise_m", "312_swim_m", "314_mgrid_m", \
                  "316_applu_m", "318_galgel_m", "320_equake_m", \
                  "324_apsi_m", "326_gafort_m", "328_fma3d_m", \
                  "330_art_m", "332_ammp_m"]
    threads    = [1,2,4,6,8,12,16]
    
    ### initialize model
    # affinity --> benchmark --> [runtime]
    model = {}  # this might be slow, but i don't care for now
    initialize_model()
    
    ### parse results
    workPath = "../../SPEC_OMP2001/result/"
    for fileName in listdir(workPath):
        if fileName.endswith(".raw"):   # all files ending with .raw
            print(".. Parsing " + fileName)
            parse_single_result(workPath + fileName)

    dump_to_console()

    # XXX generate a single figure
    generate_figure(model["scatter"]["330_art_m"], "330_art_m.scatter")
