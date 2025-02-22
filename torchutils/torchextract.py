import numpy as np 
import torch
import torch.nn as nn
from torch.fx import symbolic_trace
from torch.fx.passes.shape_prop import ShapeProp
import torch.fx as fx
from graphviz import Digraph
import json 
from torchvision import models as tmodels
from scipy import interpolate

def is_simple_value(val):
    """
    Returns True if 'val' is one of:
      - int, bool, float
      - tuple/list of ints, bools, or floats
    Returns False otherwise (including tensors, parameters, or nested objects).
    """
    # Direct scalar check
    if isinstance(val, (int, bool, float)):
        return True
    
    # Check tuple or list
    if isinstance(val, (tuple, list)):
        return all(isinstance(x, (int, bool, float)) for x in val)
    
    return False

def extract_model_properties(model,name=""):

    interpolate_space = np.linspace(0, 1, num=256)

    parameters = model.named_parameters()
    #outjson = {'model_type':modelType,'name':modelName,'parameter_in_order_files':[], 'trained_parameter_in_order_files':[], 'number_of_parameters':len(list(parameters))}
    name = name if name != "" else model.__class__.__name__
    outjson = {'name':name,'library':'torch'}
    seen_parameters = []
    module_param_map = {}
    modules = []
    for module_name, module in model.named_modules():


        module_json = {}
        module_json['name'] = module_name
        module_json['type'] = module.__class__.__name__
        parameters = []
        for param_name, param in module.named_parameters(recurse=False):
         parameter = {}
         parameter['name'] = param_name
         parameter['shape'] = list(param.shape)
         param = param.detach().numpy().flatten()

         interpolator = interpolate.interp1d(np.linspace(0,1,param.shape[0]), param ,kind='linear')
         param = interpolator(interpolate_space)
         parameter['interpolated_vector'] =  param.tolist()
         parameters.append(parameter)
        module_json['parameters'] = parameters #[{'name':param_name,'shape':param.shape} for param_name, param in module.named_parameters(recurse=False)]
        attributes = {}

        attrs = vars(module)
        for item in attrs.items():
            if is_simple_value(item[1]):
                attributes[item[0]] = item[1]
        module_json['attributes'] = attributes
        modules.append(module_json)
    outjson['network'] = modules # I am assuming this in order
    outjson['graph'] = extract_graph(model)

    return outjson

def extract_graph(model):
    first_parameter = next(model.parameters())
    traced = symbolic_trace(model)
    shapes = ShapeProp(traced)

    #for name, param in traced.named_parameters():
    #    print("PARAM:", name)

    # Prints all buffers (non-parameter tensors) with their names
    #for name, buf in traced.named_buffers():
    #    print("BUFFER:", name)
    #print(set([node.op for node in traced.graph.nodes]))
    #input()

    computeGraph = { "model":model.__class__.__name__,"library":"torch","nodes": []}
    for node in traced.graph.nodes:
        node_info = {
            "op": node.op,
            "name": node.name,
            "target": str(node.target),
            "input": [str(arg) for arg in node.args],  # Convert inputs to strings for JSON serialization
            "parameters": {}  # Initialize empty parameters
        }
        if node.op == 'placeholder':
            pass
        # If the node is calling a module, retrieve its type and parameter shapes
        if node.op == 'call_module':
            module = traced.get_submodule(node.target)
            module_type = type(module).__name__
            node_info['type'] = module_type
            #print([str(arg) for arg in node.args])
            #for k,v in module.state_dict().items():
            #    print('key',k)
            #input()
            # Retrieve shapes of parameters
            param_shapes = {k: list(v.shape) for k, v in module.state_dict().items()}
            #print(param_shapes)
            #input()
            #print(param_shapes)
            #input()
            node_info['parameters'] = param_shapes
            
            # Now you can access the original weights, for example:
            #if 'weights' in original_module:
            #    weights = original_module.weight

            #    print(weights)
            #for name,param in module.named_parameters():
            #    print (name)
        elif node.op == 'call_function':
            node_info['type'] = f"Function: {str(node.target)}"
            # Get the name of the built-in function (like add, relu, etc.)
            if hasattr(node.target, '__name__'):
                func_name = node.target.__name__
            else:
                func_name = str(node.target)  # Fallback for complex functions
            node_info['type'] = f"{func_name}"
        elif node.op == "get_attr":
            pass
            #print(node.target)
            #getattr(traced,node.target)
            #parameter = model.get_parameter(node.target)
            #weight = getattr(model, node.target)
            #print(parameter)
        computeGraph['nodes'].append(node_info)
    # Convert to JSON and return
    return json.dumps(computeGraph, indent=4)


if __name__ == "__main__":
    # Define a simple model with skip connection
    class SimpleSkipConnectionModel(nn.Module):
        def __init__(self):
            super(SimpleSkipConnectionModel, self).__init__()
            self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
            self.relu = nn.ReLU()
            self.conv2 = nn.Conv2d(16, 16, kernel_size=3, padding=1)

        def forward(self, x):
            identity = x  # Skip connection branch
            out = self.conv1(x)
            out = self.relu(out)
            out = self.conv2(out)
            out += identity  # Skip connection (add original input)
            return out

    # Step 1: Trace the model using torch.fx
    model = SimpleSkipConnectionModel()
    model = tmodels.get_model('resnet50',weights='DEFAULT')

    print(extract_model_properties(model))
    #print(extract_graph(model))
