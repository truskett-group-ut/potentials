import numpy as np

class Potential:
    #load in any default parameters needed
    def __init__(self):
        self.num_params = 7
        self.param_names = set(['d', 'e1', 'e2', 'a1', 'a2', 'n1', 'n2'])
        return None
    
    #initialize the state
    def SetParamsState(self, params_state):
        self.params_state = params_state
        if len(self.params_state) != self.num_params:
            raise AttributeError('Wrong number of parameters for gaussian pair potential')
        return None
        
    #this is the actual potential
    def Potential(self, r, params_val):
        #load in the opt params
        d = float(params_val['d'])                   #core diameter
        e1 = float(params_val['e1'])                   #first well depth
        e2 = float(params_val['e2'])                   #second well depth
        a1 = float(params_val['a1'])                   #first well width
        a2 = float(params_val['a2'])                   #second well width
        n1 = float(params_val['n1'])                   #first gaussian power
        n2 = float(params_val['n2'])                   #second gaussian power
 
        #calculate the dimensionless potential (over k_B*T)
        r = np.maximum(0.00001, r)
        ur=-e1*np.exp(-((r-d-(a1/2.)-(a2/4.))/(a1/2.+a2/4.))**n1)*((-r+d+a1+a2/2.)/(a1+a2/2.))**2.+e2*1*(r <= d+a1+a2/2.)+1*(r > d+a1+a2/2.)*e2*np.exp(-((r-d-(a2/2.)-a1)/(a2/2.))**n2)
        return ur
