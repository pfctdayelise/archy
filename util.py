import inspect
import sys

def add_functions_as_module_level_functions(functions, module_name):
    '''
    functions: {name: function}
    '''
    # get the module as an object
    module_obj = sys.modules[module_name]

    # Iterate over the methods of the class and dynamically create a function
    # for each method that calls the method and add it to the current module
    for method_name, func in functions.items():
        # add the function to the current module
        setattr(module_obj, method_name, func)
