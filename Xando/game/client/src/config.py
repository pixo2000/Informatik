import json
import os

# Erzeuge den Pfad zur config.json-Datei
config_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'config.json')

# Lade die JSON-Datei
with open(config_path, 'r') as file:
    config = json.load(file)

# Extrahiere die Werte
host = config["Server"]["Host"]
port = config["Server"]["Port"]