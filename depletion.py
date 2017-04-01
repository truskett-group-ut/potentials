from numpy import tanh, pi, logical_and

class Potential():
    #load in any default parameters needed
    def __init__(self):
        self.num_params = 4
        self.param_names = set(['rho_p', 'd_p', 'd', 'w'])
        return None
    
    #initialize the state
    def SetParamsState(self, params_state):
        self.params_state = params_state
        if len(self.params_state) != self.num_params:
            raise AttributeError('Wrong number of parameters for depletion potential')
        return None
        
    #this is the actual potential
    def Potential(self, r, params_val):
        #load in the opt params
        rho_p = float(params_val['rho_p'])  #polymer concentration
        d_p = float(params_val['d_p'])      #polymer diameter
        d = float(params_val['d'])          #particle diameter
        w = float(params_val['w'])          #how fast to smooth the linearly extrapolated core region to zero
        #calculate the dimensionless potential (over k_B*T)
        #some simplified constants
        R_d = d/2.0 + d_p/2.0
        ur0 = -1.0*(rho_p/d**3)*((4.0*pi/3.0)*(R_d**3 - (3.0/4.0)*d*R_d**2 + (1.0/16.0)*d**3)) 
        dur0 = -1.0*(rho_p/d**3)*((4.0*pi/3.0)*(-1.0*(3.0/4.0)*R_d**2 + (3.0/16.0)*d**2)) 
        #vectorized functional form
        ur = (r < d)*(ur0 + dur0*(r - d))
        ur = ur + logical_and(d <= r, r < d + d_p)*(-1.0*(rho_p/d**3)*((4.0*pi/3.0)*(R_d**3 - (3.0/4.0)*r*R_d**2 + (1.0/16.0)*r**3)))
        #smooth the potential
        ur = 0.5*(1.0 + tanh(w*(r - d)))*ur
        return ur