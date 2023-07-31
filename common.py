import os
import json
from random import sample
from base64 import b64encode, b64decode


def get_settings():
    with open(os.path.dirname(__file__) + '/files/settings.json', 'r') as json_file:
        return json.load(json_file)


def get_commands_list():
    with open(os.path.dirname(__file__) + '/files/commands.json', 'r') as json_file:
        return json.load(json_file)


def extract_commands_data(commands_list):
    commands_json = dict()

    for command in commands_list:
        commands_json[command.name] = {
            "description": command.description,
            "parameters": [f"{parameter.name}: {parameter.description}" for parameter in command.parameters],
            "guild_only": command.guild_only,
            "extras": command.extras
        }

    with open(os.path.dirname(__file__) + '/files/commands.json', 'w') as json_file:
        json.dump(commands_json, json_file, indent=4)


def encode_id(id: str) -> str:
    id_list = [id[i:i+3] for i in range(0, len(id), 3)]
    pattern = sample(range(0, 6), 6)

    hashed_id = ''.join([id_list[pattern.index(x)] for x in range(0, 6)])

    hashed_id += ''.join(str(e) for e in pattern)

    return b64encode(hashed_id.encode()).decode()


def decode_id(hashed_id: str) -> str:
    blend_id = b64decode(hashed_id).decode()
    id_list = [blend_id[i:i + 3] for i in range(0, len(blend_id) - 6, 3)]
    pattern = [int(blend_id[i:i + 1]) for i in range(len(blend_id) - 6, len(blend_id), 1)]

    id = [id_list[x] for x in pattern]

    return ''.join(id)
