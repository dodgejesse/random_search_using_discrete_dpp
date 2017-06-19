#just a dummy class to store "None" as a hparam setting. 
#should be turned back into None before being returned
class None_storage():
    def get_result():
        return None
    def __str__(self):
        return "None_object"
    def __repr__(self):
        return "None_object"
    def __eq__(self, other):
        return isinstance(other, None_storage)
    def __ne__(self, other):
        return not isinstance(other, None_storage)
            
