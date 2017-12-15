from numpy import maximum, minimum

class Potential:
    #load in any default parameters needed
    def __init__(self):
        self.num_params = 5
        self.param_names = set(['di', 'dj', 'epsilon', 'alpha', 'max_ur'])
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
        di = float(params_val['di'])                 #particle diameter i
        dj = float(params_val['dj'])                 #particle diameter j
        epsilon = float(params_val['epsilon'])       #how steep the wca repulsion should be
        alpha = float(params_val['alpha'])           #the exponent for the wca interaction
        max_ur = float(params_val['max_ur'])         #maximum value of the potential before leveling out
        #calculate the dimensionless potential (over k_B*T)
        alpha = max(0.001, alpha)
        r = maximum(0.0001, r)
        d = (di + dj)/2.0
        ur = (r <= d*(2.0**(1.0/alpha)))*(4.0*epsilon*((d/r)**(2*alpha) - (d/r)**(alpha)) + epsilon)
        ur = minimum(max_ur, ur)
        return ur