"""
Random search - presented as hyperopt.fmin_random
"""
import logging
import numpy as np

import sys
import pyll

from .base import miscs_update_idxs_vals

logger = logging.getLogger(__name__)

def print_apply_object(a, indent):
    print indent + "a.name: ",
    print a.name
    print indent + "a.pos_args: "
    for a_child in a.pos_args:
        print_apply_object(a_child, indent + '|\t')
    print(indent + "the named_args:")
    for a_child in a.named_args:

        print_apply_object(a_child[1], indent + '|\t')
    #print(indent + "a.named_args: ", a.named_args)
    print indent + "a.o_len: ",
    print str(a.o_len)
    print indent + "a.pure: ", 
    print str(a.pure)

def suggest(new_ids, domain, trials, seed):
    #logger.debug("in suggest with seed: %s" % (str(seed)))
    #logger.debug('generating trials for new_ids: %s' % str(new_ids))

    #print("\n\n")
    #print_apply_object(domain.s_idxs_vals, "")
    #print("\n\n")
    #import pdb; pdb.set_trace()
    rng = np.random.RandomState(seed)
    rval = []
    for ii, new_id in enumerate(new_ids):
        # -- sample new specs, idxs, vals
        idxs, vals = pyll.rec_eval(
            domain.s_idxs_vals,
            memo={
                domain.s_new_ids: [new_id],
                domain.s_rng: rng,
            })
        #print("new_ids: ", new_ids)
        #print("idxs: ", idxs)
        #print("vals: ", vals)
        #print("domain.s_idxs_vals: ", domain.s_idxs_vals)
        #print("domain.s_new_ids: ", domain.s_new_ids)
        #print("new_result: ", domain.new_result())
        #print("\nprinting domain.s_new_ids, an apply object:")
        #print_apply_object(domain.s_new_ids, "")
        #print("\nprinting domain.s_idxs_vals, an apply object:")
        #print_apply_object(domain.s_idxs_vals, "")
        #print("")
        new_result = domain.new_result()
        new_misc = dict(tid=new_id, cmd=domain.cmd, workdir=domain.workdir)
        miscs_update_idxs_vals([new_misc], idxs, vals)
        rval.extend(trials.new_trial_docs([new_id],
                    [None], [new_result], [new_misc]))
    return rval

# flake8 likes no trailing blank line
