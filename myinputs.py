import yaml

# reads input yaml file
def read_yaml_file(filepath):
    """
    read_input_from_file: read inputs from a yaml file
    Arguments:
    filepath: path of YAML file
    Returns:
    dictionary 
    """
    # read the yaml file
    with open(filepath, 'r') as f:
        params = yaml.safe_load(f)

    return params 
