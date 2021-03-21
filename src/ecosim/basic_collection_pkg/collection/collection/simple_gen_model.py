import pyomo.environ as aml


class Solver:
    def __init__(
        self,
        solver: str = "glpk",
        solver_params: dict = None,
        ):
        self.optimizer = aml.SolverFactory(solver)

        if solver_params:
            for param, value in solver_params:
                self.optimizer.options[param] = value

    def solve(self, model, tee=True):
        result = self.optimizer.solve(model, tee=tee)
        return result


class Model:
    def __init__(
        self,
        ):
        super().__init__()

        self.model = aml.ConcreteModel()

        self.objective_terms = {}

        self.component_elements = {}


    def add_element(self, element):
        self.component_elements[element.id] = element
        setattr(self.model, element.id, element.block)

    def build(self):
        self.update_coupling()
        self.create_objective()

    def update_coupling(self):
        # could also just search for block component elements rather than needing to define additional lists
        # will also likely need to differentiate between physical and market/economic objects
        for component_element in self.component_elements.values():
            if hasattr(component_element, "update_coupling_constraints"):
                component_element.update_coupling_constraints()

    def create_objective(self):
        nested_all_objective_terms = [list(component_element.objective_terms.values()) for component_element in self.component_elements.values()]
        all_objective_terms = [item for sublist in nested_all_objective_terms for item in sublist]
        self.model.objective = aml.Objective(expr = sum(objective_term for objective_term in all_objective_terms))
                    

class Generator:
    def __init__(
        self,
        interval_set,
        params: dict,
        ):
        super().__init__()

        self.block = aml.Block(concrete=True)

        self.id = params["name"]
        self.objective_terms = {}

        self.block.maxMW = params["maxMW"]
        self.block.minMW = params["minMW"]
        self.block.max_ramp = params["max_ramp"]
        self.block.marginal_cost = params["marginal_cost"]
        self.block.fixed_cost =  params["fixed_cost"]
        self.block.unit_price   = params["unit_price"]

        self.block.output = aml.Var(interval_set, bounds = (0,self.block.maxMW))

        def _net_export(b,idx):
            return b.output[idx]
        
        self.block.net_export = aml.Expression(interval_set, rule=_net_export)

        def _output_upper_bound(b,idx):
            return b.output[idx] - b.maxMW <= 0

        self.block.con_output_upper_bound = aml.Constraint(interval_set, rule=_output_upper_bound)

        def _output_lower_bound(b,idx):
            return  b.minMW - b.output[idx] <= 0

        self.block.con_output_lower_bound = aml.Constraint(interval_set, rule=_output_lower_bound)

        # todo Add constraints/costs for ramping, min up, min down, startup/shutdown costs, etc.

        ## Objective Terms
        # Unclear whether this expression object needs to be added to block/model - may be enough just to have it in the objective

        def _interval_cost(b,idx):
            return b.marginal_cost * b.output[idx] + b.fixed_cost - b.unit_price* b.output[idx]

        self.block.interval_cost = aml.Expression(interval_set, rule=_interval_cost)
        
        def _total_cost(b):
            return sum(b.interval_cost[idx] for idx in interval_set)

        self.block.total_cost = aml.Expression(rule=_total_cost)

        self.objective_terms["marginal_cost"] = self.block.total_cost 
