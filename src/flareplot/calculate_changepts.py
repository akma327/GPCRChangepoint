import os
import sys
import numpy
import json
from SIMPLEchangepoint import ComputeChanges


USAGE_STR = """

# Purpose
# Input: Timeseries flareplot JSON
# Output: Changepoints regarding how the network evolves over time

# Usage
# python calculate_changepts.py <INPUT_JSON>

# Arguments
# <INPUT_JSON> Absolute path to the input flareplot json 

# Example
INPUT_JSON="/scratch/PI/rondror/akma327/DynamicNetworks/data/crystal-analysis/interaction-footprint-analysis/simulation-evobundle/flareplot-dataset/water-network/M2R-active-restrained-unpublished-rep_1.json"
cd /scratch/PI/rondror/akma327/GPCRChangepoint/src/flareplot
python calculate_changepts.py $INPUT_JSON

"""

K_MIN_ARG = 2

def calc_cpts(INPUT_JSON):
    """
    Calculates the changepoints and associated time-series observables 
    associated with a particular change in evolving graph network.
    """
    f = open(INPUT_JSON, 'r')
    json_str = ""
    for line in f:
        json_str += line 

    flareplot = json.loads(json_str)
    edges = flareplot["edges"]
    print(len(edges))



if __name__ == "__main__":
    if(len(sys.argv) < K_MIN_ARG):
        print(USAGE_STR)
        exit(1)

    (INPUT_JSON) = (sys.argv[1])
    calc_cpts(INPUT_JSON)
        
