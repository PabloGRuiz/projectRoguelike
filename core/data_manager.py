import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENEMIES_PATH = os.path.join(BASE_DIR, 'data', 'enemies.json')

def load_enemies():
    try:
        with open(ENEMIES_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ENEMIES_PATH}")
        return{}
    
ENEMY_DB = load_enemies()