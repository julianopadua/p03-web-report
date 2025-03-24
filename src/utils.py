import os
import yaml

def load_config():
    """Load configuration from config.yaml."""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Base script directory
    config_path = os.path.join(script_dir, "config.yaml")   # Path to config.yaml

    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    api_keys = {"groq": config["api_keys"]["groq"]}

    # Construct absolute paths based on script_dir and config.yaml values
    paths = {
        "script_dir": script_dir,
        "report": os.path.join(script_dir, config["paths"]["report"]),
        "images": os.path.join(script_dir, config["paths"]["images"]),
        "price_charts": os.path.join(script_dir, config["paths"]["price_charts"]),
        "header_image": os.path.join(script_dir, config["paths"]["images"], "header.png"),
        "fonts": os.path.join(script_dir, config["paths"]["fonts"]), 
        "groq": config["api_keys"]["groq"],
        "data_processed": os.path.join(script_dir, config["paths"]["data_processed"])
    }

    # Ensure directories exist
    os.makedirs(paths["report"], exist_ok=True)

    return paths
