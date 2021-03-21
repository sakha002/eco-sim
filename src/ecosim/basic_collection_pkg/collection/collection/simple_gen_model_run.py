import numpy as np
import pandas as pd
import pyomo.environ as pyo

from simple_gen_model import Model,  Generator, Solver


def instantiate_model():
    
    instance = Model()

    # Sets

    interval_index = set([0]) ## check this

    ## Parameter Definition
    all_gen_params =  {   
            "name": "gen1",
            "maxMW": 100,
            "minMW": 0,
            "max_ramp": 45,
            "marginal_cost": 35,
            "fixed_cost": 250,
            "unit_price": 55,
    } 


    ## Element addition
    instance.add_element(Generator(interval_index, all_gen_params))

    instance.build()

    return instance.model

def solve_instance(instance):
    opt = Solver()
    opt.solve(instance, tee=True)



def get_results(model):
    pyomo_objects = model.component_objects([pyo.Var, pyo.Expression, pyo.Param])
    return {
        obj.name: [[index, pyo.value(obj[index])] for index in obj] for obj in pyomo_objects
    }
    

if __name__ == "__main__":
    instance = instantiate_model()
    solve_instance(instance)

    results_dict = get_results(instance)
