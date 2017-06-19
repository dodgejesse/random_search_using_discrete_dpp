import numpy as np

class Compute_Dist():
    
    def __init__(self, root):
        self.root = root

    # prints the min and max elements of L, and where those are found
    # perhaps all horizontal neighbors less than num_discrete_steps apart in L
    # should be different, assuming only hparams are floats (not switches)
    def check_distances_correct(self, L):
        max_L = float('-inf')
        max_L_index = []
        min_L = float('inf')
        min_L_index = []
        for i in range(len(L)):
            for j in range(len(L)):
                if L[i, j] > max_L:
                    max_L = L[i, j]
                    max_L_index = [[i, j]]
                elif L[i, j] == max_L:
                    max_L_index.append([i, j])
                if L[i, j] < min_L:
                    min_L = L[i, j]
                    min_L_index = [[i, j]]
                elif L[i, j] == min_L:
                    min_L_index.append([i, j])
        print("min_L: ", min_L)
        print("min_L_index: ", min_L_index)
        print("max_L: ", max_L)
        print("max_L_index: ", max_L_index)
        

    def compute_distance(self, first, second):
        return self.compute_pair_distance(first, second, self.root)


    #if first is none and second isn't, switch them. 
    #this way we only have to check if second is none
    def compute_pair_distance(self, first, second, node):
        if node.name == 'dict':
            return self.dict_distance(first, second, node)
        elif node.name == 'switch':
            return self.switch_distance(first, second, node)
        elif node.name == 'pos_args':
            return self.pos_args_distance(first, second, node)
        elif node.name == 'float':
            return self.float_distance(first, second, node)
        elif node.name == 'literal':
            return 0
        else:
            raise ValueError("some kind of leaf node that isn't supported in measuring distance!")

    def dict_distance(self, first, second, node):
        cur_dist = 0
        for name, child in node.named_args:
            cur_dist += self.compute_pair_distance(first, second, child)
        return cur_dist

    def switch_distance(self, first, second, node):
        cur_dist = 0
        switch_name = node.pos_args[0].pos_args[0].obj
        #if at least one switch is off, or they're both on but not equal, add 1 to dist
        if not first[switch_name] == second[switch_name]:
            cur_dist += 1
        for i in range(len(node.pos_args)-1):
            cur_dist += self.compute_pair_distance(first, second, node.pos_args[i+1])
        return cur_dist
        
    def pos_args_distance(self, first, second, node):
        cur_dist = 0
        for i in range(len(node.pos_args)):
                cur_dist += self.compute_pair_distance(first, second, node.pos_args[i])
        return cur_dist

    def float_distance(self, first, second, node):
        float_name = node.pos_args[0].pos_args[0].obj
        if first[float_name] == second[float_name]:
            return 0
        elif (first[float_name] == [] and not second[float_name] == []) or (not first[
                float_name] == [] and second[float_name] == []):
            return 1
        distribution = node.pos_args[0].pos_args[1].name
        handler = getattr(self, '%s_distance' % distribution)
        return handler(first[float_name][0], second[float_name][0], node)
    
    def uniform_distance(self, first, second, node):
        lower_bound = node.pos_args[0].pos_args[1].pos_args[0].obj
        upper_bound = node.pos_args[0].pos_args[1].pos_args[1].obj
        return abs(1.0*max(first, second) - min(first, second))/abs(upper_bound - lower_bound)
        
    def loguniform_distance(self, first, second, node):
        return self.uniform_distance(np.log(first), np.log(second), node)
    
    def quniform_distance(self, first, second, node):
        return self.uniform_distance(first, second, node)
            
        
