from numpy import exp, maximum

class Potential:
    #load in any default parameters needed
    def __init__(self):
        self.num_params = 8
        self.param_names = set(['d', 'e1', 'e2', 'a1', 'a2', 'n1', 'n2', 'typ'])
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
        typ = int(params_val['typ'])        
 
        #calculate the dimensionless potential (over k_B*T)
        r = maximum(0.00001, r)
        if typ == 1:
            ur=-e1*exp(-((r-d-(a1/2.))/(a1/2.))**n1)+e2*exp(-((r-d-(a2/2.)-a1)/(a2/2.))**n2)
        if typ == 3:
            ur=-e1*exp(-((r-d-(a1/2.))/(a1/2.))**n1)*((-r+d+a1)/a1)+e2*exp(-((r-d-(a2/2.)-a1)/(a2/2.))**n2)
        if typ == 2:
            ur=-e1*exp(-((r-d-(a1/2.))/(a1/2.))**n1)+e2*exp(-((r-d-(a2/2.)-a1)/(a2/2.))**n2)*((-r+d+a1+a2)/a2)
        if typ == 4:
            ur=-e1*exp(-((r-d-(a1/2.))/(a1/2.))**n1)*((-r+d+a1)/a1)+e2*exp(-((r-d-(a2/2.)-a1)/(a2/2.))**n2)*((-r+d+a1+a2)/a2)
        return ur
