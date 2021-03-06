import sys
import json
from numpy import arange, maximum, minimum, array
import re
#wp:Program that takes input to generate intial potential files 'specs' and 'vals'
#wp:Input: 1. Specify if uniform r points 'gen_spacing', or user defined r points 'filename.txt' in 'r[number]' format, or 'user_ascii' for r and ur values
#	   2. spline name
#	   3. positive constraint ('false' or 'true')
#	   4. particle diameter (d)
#	   (5). name of ascii file to read if option 1 == 'user_ascii' 

def GenerateAkimaCumulative(r_min, r_max, dr, d, epsilon=1.0, alpha=8, max_ur=float(1e8)):
    r_max = r_max + 1.0*dr
    r = arange(r_min, r_max+dr/2.0, dr)
    r = maximum(0.0001, r)
    return ManualAkimaCumulative(r, d, epsilon, alpha, max_ur)

def ManualAkimaCumulative(r, d, epsilon=1.0, alpha=8, max_ur=float(1e8)):
    if max(r) <= d*(2.0**(1.0/alpha)):
        raise Exception('The provided "r_max" is to short for generating an initial guess. Increase this by at least a little bit or decrease the input "d".')
    ur = (r <= d*(2.0**(1.0/alpha)))*(4.0*epsilon*((d/r)**(2*alpha) - (d/r)**(alpha)) + epsilon)
    ur = minimum(max_ur, ur)
    return zip(r, ur)

if __name__ == "__main__":    
    #get provided input
    mode = sys.argv[1].strip()
    spline_id = sys.argv[2].strip()
    positive_constraint = sys.argv[3].lower() == 'true'
    d = float(sys.argv[4])
    if mode == 'gen_spacing':
        r_min = float(sys.argv[5])
        r_max =float(sys.argv[6])
        dr = float(sys.argv[7])
    if mode == 'user_ascii': 
        try:     
            ascii_file = sys.argv[5].strip()
	except:
            print "Must provide a filename to read potential data if using 'user_ascii' option. Program killed."
            exit()

    #generate the data based on spcaing input or manual specification of not locations
    if mode == 'gen_spacing':
         r__ur = GenerateAkimaCumulative(r_min, r_max, dr, d)
    elif mode == 'user_ascii':
    #wp:user provided knots and positions. As long as it is a column separated file it can be anything.
        f = open(ascii_file, 'r')
        data = f.readlines()
        r = []; ur=[];
        for line in data:
            cols=line.split() 
            r.append(float(cols[0])) 
            ur.append(float(cols[1])) 
        f.close()
        r = array(r)
        ur = array(ur)
        r__ur = zip(r,ur)
    elif mode:
        f = open(mode, 'r')
        data = f.readlines()
        r = []
        num_re = r'^\s*([0-9eE\+\-\.]+)\s*'
        for line in data:
            match = re.match(num_re, line)
            if match:
                r.append(float(match.group(1)))
        f.close()
        r = array(r)
        r__ur = ManualAkimaCumulative(r, d)
    else:
         raise Exception('Invalid input provided for the mode. Enter "gen_spacing", "user_ascii"(with file name) or a filename that is not "gen_spacing".')

    #format the data
    params_val = {}
    params_state = {}
    for r, ur in r__ur[:-2]:
        param_id = spline_id + '__' + unicode(r)
        params_val[param_id] = ur
        if positive_constraint:
            params_state[param_id] = {'opt': True, 'min': 0.0}
        else:
            params_state[param_id] = {'opt': True}
    for r, ur in r__ur[-2:]:
        param_id = spline_id + '__' + unicode(r)
        params_val[param_id] = ur
        params_state[param_id] = {'opt': False}
    
    potential_specs__params_state = {'specs': {spline_id: 'akima_cumulative'},
                                     'state': params_state
                                    }
    #dump the potential_specs__params_state
    with open('./potential_specs__params_state.json', 'w') as data_file:      
        json.dump(potential_specs__params_state, data_file, indent=4, sort_keys=True)
        
    #dump the params_val
    with open('./params_val.json', 'w') as data_file:      
        json.dump(params_val, data_file, indent=4, sort_keys=True)
