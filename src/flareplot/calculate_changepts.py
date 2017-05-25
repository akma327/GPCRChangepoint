import os
import sys
import numpy as np
import json
import ast
import time
from SIMPLEchangepoint import ComputeChanges


USAGE_STR = """

# Purpose
# Input: Timeseries flareplot JSON
# Output: Changepoints regarding how the network evolves over time

# Usage
# python calculate_changepts.py <INPUT_JSON> <-lambda>

# Arguments
# <INPUT_JSON> Absolute path to the input flareplot json 
# <-lambda> Optional penalization parameter. Default 0.1

# Example
INPUT_JSON="/scratch/PI/rondror/akma327/DynamicNetworks/data/crystal-analysis/interaction-footprint-analysis/simulation-evobundle/flareplot-dataset/water-network/M2R-active-restrained-unpublished-rep_1.json"
cd /scratch/PI/rondror/akma327/GPCRChangepoint/src/flareplot
python calculate_changepts.py $INPUT_JSON

"""

K_MIN_ARG = 2

def calc_cpts(INPUT_JSON, LAMBDA=0.1):
    """
    Calculates the changepoints and associated time-series observables 
    associated with a particular change in evolving graph network.
    """


    ### Process time-series network graph 
    f = open(INPUT_JSON, 'r')
    json_str = ""
    for line in f:
        json_str += line 

    flareplot = json.loads(json_str)
    edges = flareplot["edges"]

    edge_to_tppts = {}
    max_frame = 0
    for e in edges:
        name1, name2 = str(e['name1']), str(e['name2'])
        if("-" in name1 or "-" in name2): continue
        frames = e['frames']
        mf = max(frames)
        if(mf > max_frame):
            max_frame = mf 
        key = (name1, name2)
        edge_to_tppts[key] = frames

    ### Generate the JxT dataframe where J = time series observables, T = number of time points
    data = []
    row_labels = []
    for key in edge_to_tppts:
        row_labels.append(key)
        row_info = np.zeros((max_frame + 1))
        row_info[edge_to_tppts[key]] = 1
        data.append(list(row_info))

    data = np.array(data)

    changepoints = ComputeChanges(data, LAMBDA)
    return changepoints, row_labels


def driver(INPUT_JSON, LAMBDA):
    changepoints, row_labels = calc_cpts(INPUT_JSON, LAMBDA)

    for cp_time in changepoints:
        variables = list(changepoints[cp_time])
        n1, n2 = row_labels[variables[0]]
        var_str = n1 + "--" + n2
        for i, v in enumerate(variables):
            if(i> 0):
                n1, n2 = row_labels[variables[i]]
                var_str += ", " + n1 + "--" + n2
        print("Time: " + str(cp_time) + ";\t\t\tVariables: " + var_str)



if __name__ == "__main__":
    if(len(sys.argv) < K_MIN_ARG):
        print(USAGE_STR)
        exit(1)

    (INPUT_JSON) = (sys.argv[1])
    LAMBDA = 0.1
    if("-lambda" in sys.argv):
        LAMBDA = sys.argv[sys.argv.index("-lambda") + 1]

    driver(INPUT_JSON, LAMBDA)
        
