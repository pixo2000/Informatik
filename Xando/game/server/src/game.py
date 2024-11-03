import json

class Game:
    def __init__(self):
        self.state = {}

    def update_state(self, message):
        # Update the game state based on the message
        pass

    def get_map_name_from_message(self, message):
        # Extract and return the map name from the message
        # Assuming the message format is "player_id,x,y,map_name"
        return message.split(',')[-1]

    def get_state(self):
        # Return the current game state
        return str(self.state)