import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENEMIES_PATH = os.path.join(BASE_DIR, 'data', 'enemies.json')
ITEMS_PATH = os.path.join(BASE_DIR, 'data', 'items.json')
UPGRADES_PATH = os.path.join(BASE_DIR, 'data', 'upgrades.json')
PROJECTILES_PATH = os.path.join(BASE_DIR, 'data', 'projectiles.json')

def load_enemies():
    try:
        with open(ENEMIES_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ENEMIES_PATH}")
        return{}
    
ENEMY_DB = load_enemies()

def load_items():
    try:
        with open(ITEMS_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ITEMS_PATH}")
        return{}

ITEMS_DB = load_items()

def load_upgrades():
    try:
        with open(UPGRADES_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {UPGRADES_PATH}")
        return{}

UPGRADES_DB = load_upgrades()

def load_projectiles():
    try:
        with open(PROJECTILES_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {PROJECTILES_PATH}")
        return{}

PROJECTILES_DB = load_projectiles()