from scipy.interpolate import Akima1DInterpolator as Akima
from numpy import cumsum, zeros, array, nan_to_num

#class for defining an akima spline with regard to increments between points
class AkimaCumulative:
    #load in the initial 
    def __init__(self, x, dy):
        self.x = x
        self.y = cumsum(dy[::-1])[::-1]
        self.akima = Akima(self.x, self.y)
        return None
    
    #evaluates the akima at specified x values
    def __call__(self, x, nu=0, extrapolate=None):
        return self.akima.__call__(x, nu=nu, extrapolate=extrapolate)

#actual splines potential class
class Potential:
    #load in any default parameters needed
    def __init__(self):
        self.num_params = None
        self.param_names = None
        return None
    
    #initialize the state
    def SetParamsState(self, params_state):
        self.num_params = len(params_state)
        self.param_vals_array = zeros(self.num_params)
        self.param_names = set(params_state.keys())
        self.params_state = params_state
        #create a map of entries to locations in an array
        map_tuple = []
        [map_tuple.append((float(param_name), param_name)) for param_name in self.param_names]
        map_tuple = sorted(map_tuple)
        self.param_names_array = array(zip(*map_tuple)[0])
        self.map_dict = {}
        index = 0
        for _, param_name in map_tuple:
            self.map_dict[param_name] = index
            index = index + 1
        return None
        
    #this is the actual potential
    def Potential(self, r, params_val):
        #load in the opt params
        r__ur = []
        for param_name in params_val:
            self.param_vals_array[self.map_dict[param_name]] = params_val[param_name]    
        #make the akima with linear extrapolation backwards to zero
        akima = AkimaCumulative(self.param_names_array, self.param_vals_array)
        ur = akima.__call__(r)
        ur = nan_to_num(ur)
        r0, r1 = self.param_names_array[0], self.param_names_array[1]
        ur0, ur1 = akima.__call__(r0), akima.__call__(r1)
        m = (ur1 - ur0)/(r1 - r0)
        ur = ur + (r < r0)*(m*(r - r0) + ur0)
        return ur