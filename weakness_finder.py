# *****************************************************************************
# * weakness_finder.py
# ****************************************************************************
# * Copyright 2023 Rey Urquiza
#
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * any later version.
#
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *****************************************************************************

import pypokedex
import pyautogui
import pytesseract
import os
from time import sleep
from PIL import Image
import re
import keyboard
import difflib

# Add the path to the Tesseract OCR engine's "tesseract.exe" file
os.environ["PATH"] += os.pathsep + 'path_to_tesseract'

BATTLE_COLOR_BAR = (109, 117, 93)

# 1080p at full screen
LEFT_X = 20
LEFT_Y = 212
X_OFFSET = 314
Y_OFFSET = 75


POKEMON = ""
# Dictionary containing the type matchups (DEFENSIVE TABLE)
type_matchups = {
    "normal": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 2, "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 1, "ghost": 0, "dragon": 1, "dark": 1, "steel": 1, "fairy": 1},
    "fire": {"normal": 1, "fire": 0.5, "water": 2, "electric": 1, "grass": 0.5, "ice": 0.5, "fighting": 1, "poison": 1, "ground": 2, "flying": 1, "psychic": 1, "bug": 0.5, "rock": 2, "ghost": 1, "dragon": 1, "dark": 1, "steel": 0.5, "fairy": 0.5},
    "water": {"normal": 1, "fire": 0.5, "water": 0.5, "electric": 2, "grass": 2, "ice": 0.5, "fighting": 1, "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 1, "dark": 1, "steel": 0.5, "fairy": 1},
    "electric": {"normal": 1, "fire": 1, "water": 1, "electric": 0.5, "grass": 1, "ice": 1, "fighting": 1, "poison": 1, "ground": 2, "flying": 0.5, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 1, "dark": 1, "steel": 0.5, "fairy": 1},
    "grass": {"normal": 1, "fire": 2, "water": 0.5, "electric": 0.5, "grass": 0.5, "ice": 2, "fighting": 1, "poison": 2, "ground": 0.5, "flying": 2, "psychic": 1, "bug": 2, "rock": 1, "ghost": 1, "dragon": 1, "dark": 1, "steel": 1, "fairy": 1},
    "ice": {"normal": 1, "fire": 2, "water": 1, "electric": 1, "grass": 1, "ice": 0.5, "fighting": 2, "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 2, "ghost": 1, "dragon": 1, "dark": 1, "steel": 2, "fairy": 1},
    "fighting": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 1, "poison": 1, "ground": 1, "flying": 2, "psychic": 2, "bug": 0.5, "rock": 0.5, "ghost": 1, "dragon": 1, "dark": 0.5, "steel": 1, "fairy": 2},
    "poison": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 0.5, "ice": 1, "fighting": 0.5, "poison": 0.5, "ground": 2, "flying": 1, "psychic": 2, "bug": 0.5, "rock": 1, "ghost": 1, "dragon": 1, "dark": 1, "steel": 1, "fairy": 0.5},
    "ground": {"normal": 1, "fire": 1, "water": 2, "electric": 0, "grass": 2, "ice": 2, "fighting": 1, "poison": 0.5, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 0.5, "ghost": 1, "dragon": 1, "dark": 1, "steel": 1, "fairy": 1},
    "flying": {"normal": 1, "fire": 1, "water": 1, "electric": 2, "grass": 0.5, "ice": 2, "fighting": 0.5, "poison": 1, "ground": 0, "flying": 1, "psychic": 1, "bug": 0.5, "rock": 2, "ghost": 1, "dragon": 1, "dark": 1, "steel": 1, "fairy": 1},
    "psychic": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 0.5, "poison": 1, "ground": 1, "flying": 1, "psychic": 0.5, "bug": 2, "rock": 1, "ghost": 2, "dragon": 1, "dark": 2, "steel": 1, "fairy": 1},
    "bug": {"normal": 1, "fire": 2, "water": 1, "electric": 1, "grass": 0.5, "ice": 1, "fighting": 0.5, "poison": 1, "ground": 0.5, "flying": 2, "psychic": 1, "bug": 1, "rock": 2, "ghost": 1, "dragon": 1, "dark": 1, "steel": 1, "fairy": 1},
    "rock": {"normal": 0.5, "fire": 0.5, "water": 2, "electric": 1, "grass": 2, "ice": 1, "fighting": 2, "poison": 0.5, "ground": 2, "flying": 0.5, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 1, "dark": 1, "steel": 2, "fairy": 1},
    "ghost": {"normal": 0, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 0, "poison": 0.5, "ground": 1, "flying": 1, "psychic": 1, "bug": 0.5, "rock": 1, "ghost": 2, "dragon": 1, "dark": 2, "steel": 1, "fairy": 1},
    "dragon": {"normal": 1, "fire": 0.5, "water": 0.5, "electric": 0.5, "grass": 0.5, "ice": 2, "fighting": 1, "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 2, "dark": 1, "steel": 1, "fairy": 2},
    "dark": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 2, "poison": 1, "ground": 1, "flying": 1, "psychic": 0, "bug": 2, "rock": 1, "ghost": 0.5, "dragon": 1, "dark": 0.5, "steel": 1, "fairy": 2},
    "steel": {"normal": 0.5, "fire": 2, "water": 1, "electric": 1, "grass": 0.5, "ice": 0.5, "fighting": 2, "poison": 0, "ground": 2, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 0.5, "ghost": 1, "dragon": 0.5, "dark": 1, "steel": 0.5, "fairy": 0.5},
    "fairy": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 0.5, "poison": 2, "ground": 1, "flying": 1, "psychic": 1, "bug": 0.5, "rock": 1, "ghost": 1, "dragon": 0, "dark": 0.5, "steel": 2, "fairy": 1}
}


# Function that gets all matchups against every other type
def super_effective(pokemon_type):
    super_effective_dict1 = {}
    super_effective_dict2 = {}

    # print(f"\t{POKEMON_TO_BE_SEARCHED.capitalize()}: {pokemon_type}")

    if len(pokemon_type) > 1:
        type1 = pokemon_type[0]
        type2 = pokemon_type[1]
    else:
        type1 = pokemon_type[0]
        type2 = ""

    print("\n")
    print(f"\t\t{POKEMON.name.capitalize()} is a [{type1}] and [{type2}] type.") if type2 else print(f"\t\t{POKEMON.name.capitalize()} is a [{type1}] type.")

    for search_type, matchups_list in type_matchups.items():
        if search_type == type1:
            for subtype, multiplier in matchups_list.items():
                super_effective_dict1.update({subtype: multiplier})
            if type2 == "":
                return super_effective_dict1
            else:
                for search_type2, matchups_list2 in type_matchups.items():
                    if search_type2 == type2:
                        for subtype, multiplier in matchups_list2.items():
                            # print(f"{subtype} is super effective against {type1}!")
                            super_effective_dict2.update({subtype: multiplier})
                return double_type_calc(super_effective_dict1, super_effective_dict2)


def get_similar_name(wrong_name):
    pokemon_list = []

    # Opening a list of strings to search
    with open('pokemon_names.txt', 'r') as f:
        for line in f:
            pokemon_list.append(line.strip())

    # Get a list of similar strings from the list
    matches = difflib.get_close_matches(wrong_name, pokemon_list)
    if matches:
        print('Did you mean one of these?')
        for suggestion in matches:
            confirm = input(f'"{suggestion}"? (y/n) ')
            if confirm.lower() == 'y':
                print('Found:', suggestion)
                return suggestion
    else:
        print("No similarly named pokemon was found.")
        return None


def custom_super_effective(type1, type2):
    super_effective_dict1 = {}
    super_effective_dict2 = {}

    if type2.lower() == "none":
        type2 = ""

    print("\n")
    print(f"\t\tThis pokemon is a [{type1}] and [{type2}] type.") if type2 else print(f"{POKEMON.name.capitalize()} is a [{type1}] type.")

    for search_type, matchups_list in type_matchups.items():
        if search_type == type1:
            for subtype, multiplier in matchups_list.items():
                super_effective_dict1.update({subtype: multiplier})
            if type2 == "":
                return super_effective_dict1
            else:
                for search_type2, matchups_list2 in type_matchups.items():
                    if search_type2 == type2:
                        for subtype, multiplier in matchups_list2.items():
                            # print(f"{subtype} is super effective against {type1}!")
                            super_effective_dict2.update({subtype: multiplier})
                return double_type_calc(super_effective_dict1, super_effective_dict2)


# Returns a dict of the two dicts combined after calculating new values
def double_type_calc(sup_eff_dict1, sup_eff_dict2):
    new_dict = {}

    for key in sup_eff_dict1.keys():
        new_dict[key] = sup_eff_dict1[key] * sup_eff_dict2[key]

    return new_dict


def display_type_list(type_list):
    print("\t\t" + ",".join(["[{}]".format(string) for string in type_list]))
    print("\n", flush=True)


def show_weaknesses(completed_dict):
    lock = True
    fourX_damage = []
    twoX_damage = []
    oneX_damage = []
    halfX_damage = []
    quarterX_damage = []
    zeroX_damage = []

    sorted_dict = dict(sorted(completed_dict.items(), key=lambda item: item[1], reverse=True))
    for key, value in sorted_dict.items():
        if lock and key == 'ground':
            try:
                for ability in POKEMON.abilities:
                    if ability.name == "levitate":
                        zeroX_damage.append(key)
                        lock = False
                        continue
            except:
                continue
        if value == 4:
            fourX_damage.append(key)
        elif value == 2:
            twoX_damage.append(key)
        elif value == 1:
            oneX_damage.append(key)
        elif value == 0.5:
            halfX_damage.append(key)
        elif value == 0.25:
            quarterX_damage.append(key)
        elif value == 0:
            zeroX_damage.append(key)

    # print(sorted_dict)
    if fourX_damage:
        print("\n\t\t\t\t4x Damage:")
        display_type_list(sorted(fourX_damage))
    if twoX_damage:
        print("\n\t\t\t\t2x Damage:")
        display_type_list(sorted(twoX_damage))

    if not fourX_damage and not twoX_damage:
        print(f"\n\t{POKEMON.name.capitalize()} doesn't have any weaknesses.")

    if oneX_damage:
        print("\n\t\t\t\t1x Damage:")
        display_type_list(sorted(oneX_damage))
    if halfX_damage:
        print("\n\t\t\t\t0.5x Damage:")
        display_type_list(sorted(halfX_damage))
    if quarterX_damage:
        print("\n\t\t\t\t0.25x Damage:")
        display_type_list(sorted(quarterX_damage))
    if zeroX_damage:
        print("\n\t\t\t\tImmune to:")
        display_type_list(sorted(zeroX_damage))

    if not lock:
        print(f"\tThis pokemon has levitate so [ground] moves have no effect.\n")


def read_text_from_screen(x1, y1, x2, y2):
    # Take a screenshot of the specified area
    # now = datetime.datetime.now()
    # time_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    image = pyautogui.screenshot(region=(x1, y1, x2, y2))
    # image.save('screenshot_{}.png'.format(time_string))

    image = image.resize((image.width * 2, image.height * 2), Image.BILINEAR)
    # Convert the screenshot to text using OCR (Optical Character Recognition)
    text = pytesseract.image_to_string(image)
    return text


def clean_name(poke_name):
    cleaned = poke_name
    # Use the re.sub() function to remove all non-alphanumeric characters, whitespace, and newlines
    cleaned = re.sub(r'[^\w\s]', '', cleaned)  # remove special characters and non-alphanumeric
    cleaned = cleaned.split('\n')[0]
    cleaned = cleaned.replace("\n", "")
    cleaned = cleaned.replace(" ", "")
    cleaned = re.sub(r'\s+', ' ', cleaned)  # remove multiple whitespaces
    cleaned = cleaned.strip()  # remove leading and trailing whitespaces
    # print(f"Read {cleaned} from screenshot.")

    return cleaned


def automatic_battle_check(default):
    in_battle = False
    color_match_x = 0
    color_match_y = 0
    print("made it into auto mode")
    global POKEMON
    POKEMON = pypokedex.get(name=default)
    while True:
        if keyboard.is_pressed('x'):
            return
        image = pyautogui.screenshot(region=(LEFT_X, LEFT_Y, X_OFFSET, Y_OFFSET))

        if image.getpixel((40, 0)) == BATTLE_COLOR_BAR:
            # print("Battle Scene Detected!")
            in_battle = True
            name = read_text_from_screen(LEFT_X, LEFT_Y, X_OFFSET, Y_OFFSET)
            name = clean_name(name)
            if name == "":
                sleep(.1)
                continue
            if POKEMON.name.capitalize() != name:
                # print(f"'{POKEMON.name.capitalize()}' is not '{name}'")
                print(f"Fetching the data for {name}")
                try:
                    POKEMON = pypokedex.get(name=name)
                except:
                    # print(f"Sorry, '{name}' was not found, did you spell it correctly?")
                    continue
                super_effective_types = super_effective(POKEMON.types)
                if super_effective_types:
                    show_weaknesses(super_effective_types)
        else:
            # print("Not in a battle state!")
            continue


def get_mouse_pos():
    while True:
        x, y = pyautogui.position()
        print(x, y)
        sleep(.3)


if __name__ == "__main__":
    while True:
        name = input("Please enter one of the following:\n\tEnter the name of the Pokemon\n\tEnter the Pokedex entry number\n\tEnter 'custom' to input a custom typing\n\tEnter 'auto' to enter automatic mode\n\tEnter 's' to take a screenshot\n\tEnter 'q' to exit: ")
        if name == "q":
            exit()
        elif name == "custom":
            input1, input2 = input("Please enter two types with the primary type first. If the pokemon has only one type, enter 'NONE' for the second type\nSample Input: flying normal: ").split()
            super_effective_types = custom_super_effective(input1, input2)
            if super_effective_types:
                show_weaknesses(super_effective_types)
            continue
        elif name == "s":
            name = read_text_from_screen(LEFT_X, LEFT_Y, X_OFFSET, Y_OFFSET)
            name = clean_name(name)
            # get_mouse_pos()
        elif name == "auto":
            print("Will now constantly check if you are in a battle and will search pokemon automatically. Press 'x' to exit this mode.")
            name = read_text_from_screen(LEFT_X, LEFT_Y, X_OFFSET, Y_OFFSET)
            name = clean_name(name)
            automatic_battle_check("piplup")
        elif not name.isalpha():
            try:
                p = pypokedex.get(dex=int(name))
            except:
                print(f"Sorry, the Pokemon with entry #{name} was not found.")
                continue
        try:
            p = pypokedex.get(name=name)
        except:
            print(f"Sorry, '{name}' was not found, going to try most similar named pokemon.")
            p = pypokedex.get(name=get_similar_name(name))
        POKEMON = p
        super_effective_types = super_effective(p.types)
        if super_effective_types:
            show_weaknesses(super_effective_types)
