"""
Annealing algorithm for hyperopt

Annealing is a simple but effective variant on random search that
takes some advantage of a smooth response surface.

The simple (but not overly simple) code of simulated annealing makes this file
a good starting point for implementing new search algorithms.

"""

__authors__ = "mostly Jesse Dodge, but influenced by James Bergstra"
__license__ = "3-clause BSD License"
__contact__ = "github.com/jaberg/hyperopt"

import logging

import numpy as np
from pyll.stochastic import (
    # -- integer
    categorical,
    # randint, -- unneeded
    # -- normal
    normal,
    lognormal,
    qnormal,
    qlognormal,
    # -- uniform
    uniform,
    loguniform,
    quniform,
    qloguniform,
    )
import pyll
from collections import deque
from .base import miscs_to_idxs_vals

import random
from discretize_space import Discretizer

    

def output_format(vals, new_id, domain, trials):
    idxs = {}
    for k in vals:
        if vals[k] == []:
            idxs[k] = []
        else:
            idxs[k] = [new_id]
    new_result = domain.new_result()

    new_misc = dict(tid=new_id, cmd=domain.cmd, workdir=domain.workdir)
    from base import miscs_update_idxs_vals
    miscs_update_idxs_vals([new_misc], idxs, vals)
    rval = trials.new_trial_docs([new_id], [None], [new_result], [new_misc])
    return rval

def suggest(new_ids, domain, trials, seed, *args, **kwargs):
    #if first time through, sample set of hparams 
    #import pdb; pdb.set_trace()
    if new_ids[0] == 0:
        discretizer = Discretizer()
        d_space = discretizer.discretize_space(domain)
        
        trials.random_sampled_points = np.random.choice(d_space, trials.max_evals, replace=False)
        print("The hyperparameter settings that will be evaluated:")
        for thing in trials.random_sampled_points:
            print thing
        print("")

    return output_format(trials.random_sampled_points[new_ids[0]], new_ids[0], domain, trials)

