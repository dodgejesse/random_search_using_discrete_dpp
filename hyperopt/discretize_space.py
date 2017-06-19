import numpy as np
import copy
from none_storage import None_storage
class Discretizer():
    def __init__(self,num_discrete_steps=15.0):
        self.num_discrete_steps = float(num_discrete_steps)
    

    def increment_uniform(self, node, hp_out, step_size=None):
        lower_bound = node.pos_args[0].pos_args[1].pos_args[0].obj
        upper_bound = node.pos_args[0].pos_args[1].pos_args[1].obj
        if hp_out == []:
            hp_out.append(lower_bound)
            return False
        if step_size is None:
            step_size = (upper_bound - lower_bound) / self.num_discrete_steps
        #case where upper and lower bound are equal
        if step_size == 0:
            return False
        assert lower_bound <= hp_out[0] <= upper_bound
        if hp_out[0] + step_size > upper_bound:
            hp_out[0] = lower_bound
            return False
        else:
            hp_out[0] = hp_out[0] + step_size
            return True
            
    def increment_quniform(self,node, hp_out):
        step_size=node.pos_args[0].pos_args[1].pos_args[2].obj
        lower_bound = node.pos_args[0].pos_args[1].pos_args[0].obj
        upper_bound = node.pos_args[0].pos_args[1].pos_args[1].obj
        distance = upper_bound-lower_bound
        num_steps = distance/step_size
        multiplier = max(1,int(num_steps/self.num_discrete_steps))
        
        return self.increment_uniform(node, hp_out, step_size*multiplier)
                                      

    def increment_loguniform(self,node, hp_out):
        if not hp_out == []:
            hp_out[0] = np.log(hp_out[0])
        incremented = self.increment_uniform(node, hp_out)
        hp_out[0] = np.exp(hp_out[0])
        return incremented

    #input:
    #node: the current hyperparam to be evaluated
    #
    #returns true if successfully incremented node
    #returns false if this is the first or only value it can take
    def increment_float(self, node, hp_out, enter_vals):
        float_name = node.pos_args[0].pos_args[0].obj
        if not enter_vals:
            hp_out[float_name] = []
            return False
        elif float_name not in hp_out:
            hp_out[float_name] = []
        distribution = node.pos_args[0].pos_args[1].name
        handler = getattr(self, 'increment_%s' % distribution)
        
        #calls an increment method, but only passes in the list for this node, not all of hp_out
        return handler(node, hp_out[float_name])
        
            

    def increment_pos_args(self, node, hp_out, enter_vals):
        for i in range(len(node.pos_args)):
            incremented = self.increment_node(node.pos_args[i], hp_out, enter_vals)
            if incremented:
                return True
        return False

    def increment_dict(self, node, hp_out, enter_vals):
        for name, child in node.named_args:
            incremented = self.increment_node(child, hp_out, enter_vals)
            #if incremented is true, this updates hp_out with new value
            #if it's false, hp_out[name] is reset to first value
            if incremented:
                return True
        return False

    def increment_switch(self, node, hp_out, enter_vals):
        switch_name = node.pos_args[0].pos_args[0].obj
        length_of_switch = len(node.pos_args)-1
        if not enter_vals:
            hp_out[switch_name] = []
            for i in range(1, length_of_switch):
                self.increment_node(node.pos_args[i+1], hp_out, False)
            return False
        if switch_name not in hp_out or hp_out[switch_name] == []:
            hp_out[switch_name] = [0]
            self.increment_node(node.pos_args[1], hp_out, enter_vals)
            
            for i in range(1,length_of_switch):
                #this adds the off elements of the set to hp_out
                self.increment_node(node.pos_args[i+1], hp_out, False)
            return False
        else:
            #current switch route increments
            cur_active = hp_out[switch_name][0]
            
            if self.increment_node(node.pos_args[cur_active+1], hp_out, enter_vals):
                return True
            else:
                self.increment_node(node.pos_args[cur_active+1], hp_out, False)
                #incremented all, reverting back to start
                if cur_active == length_of_switch - 1:
                    hp_out[switch_name] = [0]
                    self.increment_node(node.pos_args[1], hp_out, enter_vals)
                    return False
                else:
                    hp_out[switch_name] = [cur_active+1]
                    self.increment_node(node.pos_args[hp_out[switch_name][0]+1], hp_out, enter_vals)
                    #the line above will likely return False (always?). however, we want
                    #to return true if enter_vals is true, and false if it's false.
                    return enter_vals
                    
    def increment_node(self,node, hp_out, enter_vals):
        if node.name == 'dict':
            return self.increment_dict(node, hp_out, enter_vals)
        elif node.name == 'switch':
            return self.increment_switch(node, hp_out, enter_vals)
        elif node.name == 'pos_args':
            return self.increment_pos_args(node, hp_out, enter_vals)
        elif node.name == 'float':
            return self.increment_float(node, hp_out, enter_vals)
        elif node.name == 'literal':
            return False
        else:
            raise ValueError("some kind of node that isn't supported in discritization!")

    def debug_remove_shit(self, root, max_index_to_keep=None, type_to_keep=None):
        for i in range(len(root.named_args[1][1].pos_args[1].named_args)):
            cur_name = root.named_args[1][1].pos_args[1].named_args[i][0]
            #print root.named_args[1][1].pos_args[1].named_args[i][1]
            if max_index_to_keep is None and type_to_keep is None:
                print [root.named_args[1][1].pos_args[1].named_args[i][0],
                       root.named_args[1][1].pos_args[1].named_args[i][1].name], i
                set_to_keep = ['dropout_0', 'learning_rate_0']
                if cur_name not in set_to_keep:
                    root.named_args[1][1].pos_args[1].named_args[i] = None
            elif max_index_to_keep is not None and i > max_index_to_keep:
                root.named_args[1][1].pos_args[1].named_args[i] = None
            elif type_to_keep is not None:
                if root.named_args[1][1].pos_args[1].named_args[i][1].name != type_to_keep:
                    root.named_args[1][1].pos_args[1].named_args[i] = None

        root.named_args[1][1].pos_args[1].named_args = [x for x in root.named_args[1][1].pos_args[1].named_args if x != None]


    #prints size of total space with only 1 hparam, 2 hparams, 3 hparams, etc.
    def discretize_space_debug(self, domain):
        #current hparam setting
        root = domain.expr
        storage = []
        for i in range(len(root.named_args[1][1].pos_args[1].named_args)):
            storage.append(root.named_args[1][1].pos_args[1].named_args[i])
            print root.named_args[1][1].pos_args[1].named_args[i]
        for i in range(len(root.named_args[1][1].pos_args[1].named_args)):
            self.debug_remove_shit(root,i)
            hp_out_set = self.discretize_space(domain, False)
            set_of_things_kept = ''
            for j in range(i+1):
                set_of_things_kept = set_of_things_kept + ', ' + root.named_args[1][1].pos_args[1].named_args[j][0]
            print(set_of_things_kept + ': ' + str(len(hp_out_set)))
            new_named_args = []
            for j in range(len(storage)):
                new_named_args.append(storage[j])
            root.named_args[1][1].pos_args[1].named_args = new_named_args
        import pdb; pdb.set_trace()


    def discretize_space(self, domain, print_10_k=True):
        #set of hparam settings
        hp_out_set = []
        #current hparam setting
        root = domain.expr
        #import pdb; pdb.set_trace()        
        #self.debug_remove_shit(root, max_index_to_keep=4)

        cur_incremented_values = {}
        self.increment_node(root,cur_incremented_values,True)
        incremented = True
        #print("discretizing hyperparameter search space...")
        while incremented:
            hp_out_set.append(copy.deepcopy(cur_incremented_values))
            incremented = self.increment_node(root, cur_incremented_values, True)
                
            if len(hp_out_set) % 10000 == 0 and print_10_k:
                print("current size of set: " + str(len(hp_out_set)))
                print(hp_out_set[len(hp_out_set)-1])
        print("done discretizing hyperparameter search space. set size: {}".format(len(hp_out_set)))
        
        return hp_out_set
