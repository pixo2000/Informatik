import json
import os

# Generate the path to the config.json file
config_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'config.json')

# Load the JSON file
with open(config_path, 'r') as file:
    config = json.load(file)

# Extract the values
# Server:
port = config["Port"]