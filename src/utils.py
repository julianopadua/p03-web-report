import yaml

def load_config(filepath):
    """Load configuration from a YAML file."""
    with open(filepath, "r") as file:
        return yaml.safe_load(file)
