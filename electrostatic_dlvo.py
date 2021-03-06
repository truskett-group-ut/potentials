from numpy import exp, maximum

class Potential:
    #load in any default parameters needed
    def __init__(self):
        self.num_params = 2
        self.param_names = set(['A', 'z'])
        return None
    
    #initialize the state
    def SetParamsState(self, params_state):
        self.params_state = params_state
        if len(self.params_state) != self.num_params:
            raise AttributeError('Wrong number of parameters for weeks chandler anderson potential')
        return None
        
    #this is the actual potential
    def Potential(self, r, params_val):
        #load in the opt params
        A = float(params_val['A'])                   #electro amplitude
        z = float(params_val['z'])                   #screening length
        #calculate the dimensionless potential (over k_B*T)
        r = maximum(0.00001, r)
        ur = A*exp(-r/z)/r
        return ur