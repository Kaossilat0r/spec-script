'''
Created on 16.04.2014

A script to utilize the results of the spec omp 2001 benchmark
@author: roman
'''
from os import path, listdir, makedirs
import errno

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

            model[bench][affinity][numThreads].append(runtime)
    
    #print("threads:" + str(numThreads) + " affinity:" + str(affinity) + " queue:" + str(queue))

def generate_figures():
    """
    generate figures for all benchmarks
    """
    # create results directory if necessary
    try:
        makedirs("results")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    for b in benchmarks:
        print("plot " + b)
        generate_figure(model[b], b)

def generate_figure(benchmark, name):
    AVG, NTH, SPU = "avg", "threads", "speedup"
    
    results = {}
    for a in affinities:
        results[a] = {}
        results[a][NTH] = []
        results[a][AVG] = []
        results[a][SPU] =[]
    
    for a in affinities:
        for k in sorted(benchmark[a].keys()):
            
            v = benchmark[a][k]
            if len(v)==0:
                continue
            
            avg = sum(x for x in v) / len(v)
            results[a][NTH].append(k)
            results[a][AVG].append(avg)
  
    if results[a][NTH] == []:
        return  # if there are no values, skip
  
    # some matplotlib magic
    fig, ax = plt.subplots()

    ax.set_title(name + " - Runtime")    
    ax.axis([0.0, max(threads)+1, 0.0, max(results["scatter"][AVG])*1.1])

    markers = {"scatter" : "^", "compact" : "o"}
    colors = {"scatter" : "b", "compact" : "r"}

    for a in affinities:
        ax.plot(results[a][NTH], results[a][AVG], color=colors[a], marker=markers[a], label=a)

    ax.set_xlabel('numThreads')
    ax.set_ylabel('runtime [s]')
    plt.legend(loc="right")
    
    plt.savefig('results/'+name+'.png')
    plt.close()
    

def initialize_model():
    for b in benchmarks:
        model[b] = {}
        for a in affinities:
            model[b][a] = {}
            for t in threads:
                model[b][a][t] = []

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
                lst = model[b][a][t]
                
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
    
    generate_figures()

    # XXX generate a single figure
    #generate_figure(model["scatter"]["330_art_m"], "330_art_m.scatter")
