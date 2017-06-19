Random Search for Hyperparameters using Determinantal Point Processes
=====================================================================

This library is an extension to Hyperopt (with the original hyperopt
README.txt below). This is the associated code for the paper found
here: https://arxiv.org/abs/1706.01566

At a high level, this is simply an extension to hyperopt which 
incorporates sampling from a DPP. The DPP sampling code is from 
Alex Kuleza's website (here: http://www.alexkulesza.com/ and
the code here: http://www.alexkulesza.com/code/dpp.tgz). The original 
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

# if installing on aws ec2 linux instance in location:
# /home/ec2-user/software/matlab
# then do the following: 
export LD_LIBRARY_PATH="/usr/lib64:/lib64:/home/ec2-user/software/matlab/v901/runtime/glnxa64:/home/ec2-user/software/matlab/v901/bin/glnxa64:/home/ec2-user/software/matlab/v901/sys/os/glnxa64:/home/ec2-user/software/matlab/v901/sys/opengl/lib/glnxa64"
export PYTHONPATH="/home/ec2-user/software/matlab/v901/extern/engines/python/dist"


# to install hyperopt, navigate to the hyperopt directory and run:
pip install -e .

# install the dpp sampler (from the location you installed it):
cd dpp_sampler/application
python setup.py install

# then the normal dependencies of hyperopt, e.g.:
pip install scipy
pip install pymongo
pip install networkx
pip install pandas








#####################################################################
# jesse's notes:
# to install on aws:
yes | sudo yum groupinstall "Development Tools"
yes | sudo yum install emacs
yes | sudo yum install xorg-x11-xauth.x86_64 xorg-x11-server-utils.x86_64 dbus-x11.x86_64

# here you have to exit the instance, then ssh back in

mkdir software
mkdir projects
cd software
mkdir dpp_sampler
cd dpp_sampler
scp -r jessedd@pinot.cs.washington.edu:/homes/gws/jessedd/projects/dpp_sampler/DPP_Sampler ./
cd DPP_Sampler/for_redistribution
./MyAppInstaller_web.install

# this opens up a gui
# install DPP_Sampler to /home/ec2-user/software/DPP_Sampler
# install matlab runtime to /home/ec2-user/software/matlab
# put this in ~/.bashrc (the "/usr/lib64:/lib64" are to help tensorflow import /usr/lib64/libstdc++.so.6 and /lib64/libgcc_s.so.1 correctly, i.e. not the ones installed with matlab)

export LD_LIBRARY_PATH="/usr/lib64:/lib64:/home/ec2-user/software/matlab/v901/runtime/glnxa64:/home/ec2-user/software/matlab/v901/bin/glnxa64:/home/ec2-user/software/matlab/v901/sys/os/glnxa64:/home/ec2-user/software/matlab/v901/sys/opengl/lib/glnxa64"
export PYTHONPATH="/home/ec2-user/software/matlab/v901/extern/engines/python/dist"



# install anaconda:
cd ~/software
wget https://repo.continuum.io/archive/Anaconda2-4.3.1-Linux-x86_64.sh
bash Anaconda2-4.3.1-Linux-x86_64.sh

# install into /home/ec2-user/software/anaconda2

rm Anaconda2-4.3.1-Linux-x86_64.sh

# exit the instance, then ssh back in

cd projects 

git clone https://github.com/Noahs-ARK/ARKcat.git
git clone https://github.com/dodgejesse/hyperopt.git

yes | conda create --name arkcat python
source activate arkcat

cd hyperopt
pip install -e .

cd /home/ec2-user/software/DPP_Sampler/application
sudo python setup.py install

pip install scipy
pip install pymongo
pip install networkx
pip install pandas


############# if we want to also install arkcat

pip install scikit-learn
pip install xgboost
pip install tensorflow










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
