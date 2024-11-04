import json
import os

# Generate the path to the config.json file
config_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'config.json')

# Load the JSON file
with open(config_path, 'r') as file:
    config = json.load(file)

# Extract the values
# Server:
host = config["Server"]["Host"]
port = config["Server"]["Port"]

# Maps:
maps = config["Maps"]
map_names = list(maps.keys())
map_files = [maps[map_name]["File"] for map_name in map_names]