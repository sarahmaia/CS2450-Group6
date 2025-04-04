import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_color_scheme():
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config.get("primary_color", "#4C721D"), config.get("secondary_color", "#FFFFFF")
    except FileNotFoundError:
        return "#4C721D", "#FFFFFF"

def save_color_scheme(primary_color, secondary_color):
    config = {
        "primary_color": primary_color,
        "secondary_color": secondary_color
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)