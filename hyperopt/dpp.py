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


import numpy as np
from hparam_as_vector import Make_Vector
import random
import copy
from discretize_space import Discretizer
from discretized_distance import Compute_Dist
import dpp_sample_compiled_matlab
import time
import sys


def get_num_quantiles(node):
    if node.name == 'literal':
        return 1
    elif node.name == 'pos_args':
        n_q = 1
        for element in node.pos_args:
            n_q = n_q * get_num_quantiles(element)
        return n_q
    elif node.name == 'float':
         dist = node.pos_args[0].pos_args[1].name



def avg_dist_of_set(sampled_items, distance_calc, max_L, min_L):
    avg_dist = 0
    counter = 0
    for j in range(len(sampled_items)):
        for k in range(j,len(sampled_items)):
            if j == k:
                continue
            cur_dist = distance_calc(sampled_items[j], sampled_items[k])
            counter += 1
            if max_L is not None and min_L is not None:
                avg_dist += 2*(cur_dist-min_L)/(max_L-min_L)-1
            else:
                avg_dist += cur_dist
            
    return avg_dist / counter



def check_sampled_points_more_diverse(L,max_L,min_L, distance_calc, d_space,k):
    set_size = k
    dpp_avg = 0
    rand_avg = 0
    num_sets = 2500
    for i in range(num_sets):
        #this next line is how we call the mcmc algorithm
        #dpp_sampled_items = dpp_sampler.sample_k(d_space, L, set_size, max_nb_iterations = 10000)
        dpp_sampled_indices = dpp_sampler.dpp.sample_dpp(L, k)
        dpp_sampled_items = [d_space[index] for index in dpp_sampled_indices]
        cur_dpp_avg = avg_dist_of_set(dpp_sampled_items, distance_calc, max_L, min_L)
        
        dpp_avg = (dpp_avg * i + cur_dpp_avg)/(i+1)
        
        
        rand_sampled_items = random.sample(d_space, set_size)
        cur_rand_avg = avg_dist_of_set(rand_sampled_items, distance_calc, max_L, min_L)
        rand_avg = (rand_avg * i + cur_rand_avg)/(i+1)
        print('iter {}: {}, {}'.format(i,rand_avg, dpp_avg))
        
    print('dpp_avg: {}'.format(dpp_avg))
    print('rand_avg: {}'.format(rand_avg))

def generate_L_from_vectors(vectors, hamming_distance):
    if not hamming_distance:
        L = np.dot(vectors, np.transpose(vectors))
        # make it more symmetric
        L_sym = (np.transpose(L)+L)*(1.0/2)
        #this adds a eps*I to L anyway, just to make double sure it's psd
        L_prime = L_sym + np.identity(len(L_sym))*(np.power(10.0,-14))

    else:
        L = (vectors[:, None, :] == vectors).sum(2)
        # to linearly rescale from [min,max] to [a,b]:
        # f(x) = ((b-a)(x-min))/(max-min)+a
        #      = (x) (b-a)/(max-min)-(b-a)(min)/(max-min)+a
        ma = len(vectors[0])*1.0
        mi = 1*1.0
        a = -1*1.0
        b = 1*1.0
        mult = (b-a)/(ma-mi)
        add = -(b-a)*(mi)/(ma-mi)+a
        L_scaled = np.multiply(L, mult)
        L_prime = L_scaled + add

    return L_prime
    


#DEBUGGING
#This is super janky. i don't know the correct way to make the output format, so i'm guessing
#should replicate what hyperopt.pyll.base.rec_eval does to make the 'vals' object, 
#but i can't figure out how it does it.  
# also mostly coping algobase.SuggestAlgo.__call__
def output_format(vals, new_id, domain, trials):
    idxs = {}
    for k in vals:
        if vals[k] == []:
            idxs[k] = []
        else:
            idxs[k] = [new_id]
    new_result = domain.new_result()

    new_misc = dict(tid=new_id, cmd=domain.cmd, workdir=domain.workdir)
    #DEBUG not sure what this next line does
    from base import miscs_update_idxs_vals
    miscs_update_idxs_vals([new_misc], idxs, vals)
    rval = trials.new_trial_docs([new_id], [None], [new_result], [new_misc])
    return rval


def suggest(new_ids, domain, trials, seed, *args, **kwargs):
    #import pdb; pdb.set_trace()

    #if first time through, sample set of hparams
    if new_ids[0] == 0:
        discretizer = Discretizer(trials.discretize_num)
        d_space = discretizer.discretize_space(domain)

        make_vect = Make_Vector(domain.expr)
        
        hamming_distance=trials.dpp_ham
        vectors = np.asarray(make_vect.make_vectors(d_space, hamming_distance))

        L = generate_L_from_vectors(vectors, hamming_distance)
        
        check_diversity = False
        if check_diversity:
            distance_calc = Compute_Dist(domain.expr)
            check_sampled_points_more_diverse(L, None, None, distance_calc.compute_distance, d_space, 5)
        
        print_dpp_samples = False
        if print_dpp_samples:
            print("ABOUT TO START PRINTING DPP SAMPLES")
            print("")
            for i in range(100):
                dpp_sampled_indices = dpp_sample_compiled_matlab.sample_dpp(L, np.random.randint(seed), trials.max_evals)
                points = []
                for index in dpp_sampled_indices:
                    points.append(d_space[int(index[0])-1])
                    points[len(points)-1]['index'] = int(index[0]-1)
                
                for thing in points:
                    print thing
                print("")
            sys.exit(0)

        start_sample_time = time.time()
        dpp_sampled_indices = dpp_sample_compiled_matlab.sample_dpp(L, seed, trials.max_evals)
        print("sampling {} items from a DPP of size {} took {} seconds".format(trials.max_evals, 
                            len(L), time.time() - start_sample_time))

        
        trials.dpp_sampled_points = [d_space[int(index[0])-1] for index in dpp_sampled_indices]
        print("The hyperparameter settings that will be evaluated:")
        for thing in trials.dpp_sampled_points:
            print thing
        print("")
        random.shuffle(trials.dpp_sampled_points)
    return output_format(trials.dpp_sampled_points[new_ids[0]], new_ids[0], domain, trials)


def time_dpp(domain, trials, num_discrete_steps=11, k=None, print_L_time=False):

    discretizer = Discretizer(num_discrete_steps)
    d_space = discretizer.discretize_space(domain)


    start_vect_time = time.time()
    make_vect = Make_Vector(domain.expr)
    vectors = np.asarray(make_vect.make_vectors(d_space))
    if print_L_time:
        print("took {} seconds to make vectors (B)".format(time.time() - start_vect_time))
    start_L_time = time.time()
    L = generate_L_from_vectors(vectors)
    if print_L_time:
        print("took {} seconds to make L=B^TB".format(time.time() - start_L_time))
    
    if k == None:
        k = trials.max_evals
    dpp_sampled_indices = dpp_sampler.dpp.sample_dpp(L, k)
        
    
    
