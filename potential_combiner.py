from importlib import import_module
import re

class Potential:
    #load in a list of potentials (names)
    def __init__(self, potential_specs):
        #reformat
        potential_specs = potential_specs.items()
        #make sure no whitespace
        potential_specs = [(potential_id_name.strip(), potential_type.strip()) 
                           for potential_id_name, potential_type in potential_specs]
        #initial checks on data
        self.potential_id_names = zip(*potential_specs)[0]
        for potential_id_name in self.potential_id_names:
            if re.search(r'\_', potential_id_name):
                raise AttributeError('Cannot have underscores in potential id name')
        if len(set(self.potential_id_names)) != len(self.potential_id_names):
            raise AttributeError('Each potential id name must be unique')
        else:
            self.potential_id_names = set(self.potential_id_names)
        #load in the modules
        self.potentials = {}   
        import_potential = lambda x: import_module(x)
        for potential_id_name, potential_type in potential_specs:
            self.potentials[potential_id_name] = import_potential(('potentials.' + potential_type)).Potential() 
        return None
    
    #separates the parameters for funneling to individual potentials
    def Separate(self, params):
        params_separated = {}
        for param in params:
            potential_id_name = self.param_map[param]['potential_id_name']
            potential_param = self.param_map[param]['potential_param']
            if potential_id_name not in params_separated:
                params_separated[potential_id_name] = {}
            params_separated[potential_id_name][potential_param] = params[param]
        return params_separated
        
    #initialize the state
    def SetParamsState(self, params_state):
        self.params_state = params_state
        #go through and create a hash mapping to the individual potential to use now and later
        self.param_map = {}
        for param in params_state:
            match = re.match(r'\s*([a-z0-9]+)\_\_([^\s]+)', param)
            potential_id_name = match.group(1)
            potential_param = match.group(2)
            if potential_id_name in self.potential_id_names:
                self.param_map[param] = {'potential_id_name': potential_id_name, 'potential_param': potential_param}
            else:
                raise AttributeError('Potential id name not found in initial names provided.')
        #map to the individual potentials
        params_state_separated = self.Separate(params_state)
        for potential_id_name in params_state_separated:
            self.potentials[potential_id_name].SetParamsState(params_state_separated[potential_id_name])
        return None
    
    #this is the actual potential
    def Potential(self, r, params_val):
        #compute potential
        params_val_separated = self.Separate(params_val)
        ur = 0.0    
        for potential_id_name in self.potentials:
            ur = ur + self.potentials[potential_id_name].Potential(r, params_val_separated[potential_id_name])
        return ur