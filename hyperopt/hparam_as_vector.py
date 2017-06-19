import numpy as np

class Make_Vector():
    
    def __init__(self, root):
        self.root = root

    def make_vectors(self, hparam_sets, hamming_dist):
        global HAMMING_DIST
        HAMMING_DIST = hamming_dist
        vectors = []
        for i in range(len(hparam_sets)):
            vect = []
            self.make_vect(hparam_sets[i], vect, self.root)
            vect.append(1)
            vect_as_array = np.asarray(vect)
            if hamming_dist:
                vectors.append(vect_as_array)
            if not hamming_dist:
                vectors.append(vect_as_array/np.linalg.norm(vect_as_array,2))
            
        
        return vectors


    def make_vect(self, hparams, vect, node):
        if node.name == 'dict':
            self.dict_vect(hparams, vect, node)
        elif node.name == 'switch':
            self.switch_vect(hparams, vect, node)
        elif node.name == 'pos_args':
            self.pos_args_vect(hparams, vect, node)
        elif node.name == 'float':
            self.float_vect(hparams, vect, node)
        elif node.name == 'literal':
            return
        else:
            raise ValueError("some kind of leaf node that isn't supported when " + 
                             "making discrete hparams vectors!")

    def dict_vect(self, hparams, vect, node):
        for name, child in node.named_args:
            self.make_vect(hparams, vect, child)

    def switch_vect(self, hparams, vect, node):
        switch_name = node.pos_args[0].pos_args[0].obj
        if len(node.pos_args)-1 > 1:
            for i in range(len(node.pos_args)-1):
                if hparams[switch_name] == [] or not i == hparams[switch_name][0]:
                    vect.append(0)
                else:
                    vect.append(1)
        #this loop was pulled out to keep the order of vect more meaningful
        for i in range(len(node.pos_args)-1):
            self.make_vect(hparams, vect, node.pos_args[i+1])
    
    def pos_args_vect(self, hparams, vect, node):
        for i in range(len(node.pos_args)):
            self.make_vect(hparams, vect, node.pos_args[i])

    def float_vect(self, hparams, vect, node):
        float_name = node.pos_args[0].pos_args[0].obj
        lower_bound = node.pos_args[0].pos_args[1].pos_args[0].obj
        upper_bound = node.pos_args[0].pos_args[1].pos_args[1].obj
        if hparams[float_name] == []:
            vect.append(0)
            return
        elif lower_bound == upper_bound:
            return
        elif HAMMING_DIST:
            vect.append(hparams[float_name][0])
            return
        distribution = node.pos_args[0].pos_args[1].name
        handler = getattr(self, '%s_distance' % distribution)
        handler(hparams[float_name][0], vect, node, float_name)

    def uniform_distance(self, hparam, vect, node, float_name):
        lower_bound = node.pos_args[0].pos_args[1].pos_args[0].obj
        upper_bound = node.pos_args[0].pos_args[1].pos_args[1].obj
        vect.append((1.0*hparam - lower_bound)/(upper_bound - lower_bound))
        
    def loguniform_distance(self, hparam, vect, node, float_name):
        self.uniform_distance(np.log(hparam), vect, node, float_name)

    def quniform_distance(self, hparam, vect, node, float_name):
        self.uniform_distance(hparam, vect, node, float_name)
