import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_color_scheme():
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config.get("primary_color", "#D3D3D3"), config.get("secondary_color", "#F5F5F5")
    except FileNotFoundError:
        return "#4C721D", "#FFFFFF"

def save_color_scheme(primary_color, secondary_color):
    config = {
        "primary_color": primary_color,
        "secondary_color": secondary_color
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

def get_format_type(lines):
    for line in lines:
        line = line.strip()
        if line and line != "-99999":
            if not line.lstrip('+-').isdigit():
                return "Invalid instruction"
            word_length = len(line.lstrip('+-'))
            program_format = 'new' if word_length == 6 else 'old'
            return program_format