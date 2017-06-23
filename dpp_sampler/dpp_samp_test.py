import numpy as np
import matlab
import DPP_Sampler


#L = np.ones(3)
L = np.ones([3, 3])
L[0,1] = 0.8
L[1,0] = 0.8
L[1,2] = 0.8
L[2,1] = 0.8
L[0,2] = 0.7
L[2,0] = 0.7

print(L)
L_list = L.tolist()
L = matlab.double(L_list)
print(L)
dpp_samp = DPP_Sampler.initialize()
L_decomp = dpp_samp.decompose_kernel(L)

for i in range(20):
	seed = np.random.randint(500)
	
	dpp_samples = dpp_samp.sample_dpp(L_decomp,seed,2)
	print(dpp_samples)
dpp_samp.terminate()

