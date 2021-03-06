Random Search for Hyperparameters using Determinantal Point Processes
=====================================================================

This library is an extension to Hyperopt (with the original hyperopt
README.txt below). This is the associated code for the paper found
here: https://arxiv.org/abs/1706.01566

At a high level, this is simply an extension to hyperopt 
(http://hyperopt.github.io/hyperopt/) which incorporates sampling from
a DPP. The DPP sampling code is from Alex Kuleza's website 
(here: http://www.alexkulesza.com/ and the code here: 
http://www.alexkulesza.com/code/dpp.tgz). The original 
code DPP code was written in matlab, but we've compiled that matlab
code to Python and included it here. 

Differences between this library and Hyperopt:

* The example on http://hyperopt.github.io/hyperopt/ shows the fmin() function 
  taking four parameters. Using hyperopt.dpp.suggest or hyperopt.dpp_random.suggest
  search algorithms requires five: the same four as the example, plus a trials 
  object which has two additional fields. an example:

  trials = hyperopt.Trials()
  trials.discretize_num = 4
  trials.dpp_ham = True

  the trials.discretize_num field is the number of discrete steps each hyperparameter
  will take, and the boolean trials.dpp_ham is True when the distance 
  used to construct the L matrix in the DPP is $k$-DPP-Hamm, False when
  $k$-DPP-Cos is to be used. Then the call to fmin from the example is as follows:

  best = fmin(objective, space, algo=tpe.suggest, max_evals=100, trials=trials)


* The priors over hyperparameters which are implemented for DPP sampling are:
  
  hp.choice(label, options)
  hp.randint(label, upper)
  hp.uniform(label, low, high)
  hp.quniform(label, low, high, q)	
  hp.loguniform(label, low, high)
  hp.qloguniform(label, low, high, q)
  
  those based on the normal distribution have not been implemented (though
  that's on the TODO list). 
		      
The search algorithms implemented in Hyperopt (e.g. tpe.suggest, anneal.suggest, etc.)
have not been changed. Three algorithms from the paper have been added: 
$k$-DPP-Hamm:  hyperopt.dpp.suggest, with trials.dpp_ham = True
$k$-DPP-Cos:   hyperopt.dpp.suggest, with trials.dpp_ham = False
Uniform sampling on discretized space: hyperopt.dpp_random



######################################################################################
# As the DPP code is MATLAB compiled to Python, it requires the MATLAB Runtime R2016a.
# The directory dpp_sampler has an installer ("dpp_web.install") which installs both
# the DPP sampling code and the correct version of MATLAB Runtime. If you already have
# MATLAB Runtime R2016a installed you can try to use that instead. 

# It is recommended to install with Anaconda (as the dependencies are easier to deal with)


# Installation instructions: 

# if installing on a fresh aws ec2 linux instance, these steps are necessary:
yes | sudo yum groupinstall "Development Tools"
yes | sudo yum install xorg-x11-xauth.x86_64 xorg-x11-server-utils.x86_64 dbus-x11.x86_64



# first install MATLAB Runtime R2016a
git clone https://github.com/dodgejesse/hyperopt.git
cd hyperopt/dpp_sampler
./dpp_web.install

# in the GUI, choose a location for both DPP sampling code and MATLAB Runtime R2016a. 
# it is recommended to install the DPP sampling code to 
# hyperopt/dpp_sampler, but not necessary. keep track of both locations.

# note: the last page of this installer has some information on how you need to adjust your 
# LD_LIBRARY_PATH. if installing on an aws ec2 linux instance in location:
LOCATION=/home/ec2-user/software/matlab
# then do the following: 
export LD_LIBRARY_PATH="/usr/lib64:/lib64:${LOCATION}/v901/runtime/glnxa64:${LOCATION}/v901/bin/glnxa64:${LOCATION}/v901/sys/os/glnxa64:${LOCATION}/v901/sys/opengl/lib/glnxa64"
export PYTHONPATH="${LOCATION}/v901/extern/engines/python/dist"

#here you enter your conda environment

# to install hyperopt, navigate to the hyperopt directory and run:
pip install -e .

# install the dpp sampler (from the location you installed it):
cd dpp_sampler/application
python setup.py install

# then the normal dependencies of hyperopt, e.g.:
pip install numpy # note if using Anaconda, you must use this, not conda install numpy (which causes out of memory errors)
pip install scipy
pip install pymongo
pip install networkx
pip install pandas








###################################################################################################
# every command needed to install on zin:

git config --global http.sslverify false
git clone https://github.com/dodgejesse/random_search_using_discrete_dpp.git
cd random_search_using_discrete_dpp/dpp_sampler
EXAMPLE_SCRIPT_DIR=`pwd -P`
./dpp_web.install

# installed matlab to /home/jesse/software/matlab_test
# installed dpp_sampler to /home/jesse/software/dpp_sampler_test

MATLAB_DIR="/home/jesse/software/matlab_test"
DPP_SAMP_DIR="/home/jesse/software/dpp_sampler_test"

export LD_LIBRARY_PATH="/usr/lib64:/lib64:${MATLAB_DIR}/v901/runtime/glnxa64:${MATLAB_DIR}/v901/bin/glnxa64:${MATLAB_DIR}/v901/sys/os/glnxa64:${MATLAB_DIR}/v901/sys/opengl/lib/glnxa64"
export PYTHONPATH="${MATLAB_DIR}/v901/extern/engines/python/dist"

yes | conda create --name dpp_test_2 python

source activate dpp_test_2
pip install numpy

cd ${DPP_SAMP_DIR}/application
python setup.py install

cd ${EXAMPLE_SCRIPT_DIR}
python dpp_samp_test.py






# Old README.txt from hyperopt: 

hyperopt: Distributed Asynchronous Hyper-parameter Optimization
===============================================================

Hyperopt is a Python library for serial and parallel optimization over awkward
search spaces, which may include real-valued, discrete, and conditional
dimensions.

Official project git repository:
http://github.com/hyperopt/hyperopt

Documentation:
http://hyperopt.github.io/hyperopt

Announcements mailing list:
https://groups.google.com/forum/#!forum/hyperopt-announce

Thanks
------
This work was supported in part by the National Science Foundation (IIS-0963668),
and by the Banting Postdoctoral Fellowship program.
