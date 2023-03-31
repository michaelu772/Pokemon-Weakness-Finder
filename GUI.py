# *****************************************************************************
# * GUI.py
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

import difflib
import pypokedex
import pytesseract
import pyautogui
import re
from PIL import ImageTk
from PIL import Image as PILImage
from time import sleep
from tkinter import *
from tkinter.ttk import *
import os
import keyboard


# Add the path to the Tesseract OCR engine's "tesseract.exe" file
os.environ["PATH"] += os.pathsep + 'path_to_tesseract'

BATTLE_COLOR_BAR = (109, 117, 93)

LEFT_X = 20
LEFT_Y = 212
X_OFFSET = 314
Y_OFFSET = 75

TYPE1_ENTRY = None
TYPE2_ENTRY = None
OUTPUT = None
DEFAULT_ENTRY = None
NAME_ENTRY = None
ALL_POKEMON = []
AFTER_ID = None
root = None
canvas_output = None
IMAGES = []
master_output = ""

POKEMON = ""
# Dictionary containing the type matchups (DEFENSIVE TABLE)
type_matchups = {
    "normal": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 2, "poison": 1,
               "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 1, "ghost": 0, "dragon": 1, "dark": 1,
               "steel": 1, "fairy": 1},
    "fire": {"normal": 1, "fire": 0.5, "water": 2, "electric": 1, "grass": 0.5, "ice": 0.5, "fighting": 1, "poison": 1,
             "ground": 2, "flying": 1, "psychic": 1, "bug": 0.5, "rock": 2, "ghost": 1, "dragon": 1, "dark": 1,
             "steel": 0.5, "fairy": 0.5},
    "water": {"normal": 1, "fire": 0.5, "water": 0.5, "electric": 2, "grass": 2, "ice": 0.5, "fighting": 1, "poison": 1,
              "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 1, "dark": 1,
              "steel": 0.5, "fairy": 1},
    "electric": {"normal": 1, "fire": 1, "water": 1, "electric": 0.5, "grass": 1, "ice": 1, "fighting": 1, "poison": 1,
                 "ground": 2, "flying": 0.5, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 1, "dark": 1,
                 "steel": 0.5, "fairy": 1},
    "grass": {"normal": 1, "fire": 2, "water": 0.5, "electric": 0.5, "grass": 0.5, "ice": 2, "fighting": 1, "poison": 2,
              "ground": 0.5, "flying": 2, "psychic": 1, "bug": 2, "rock": 1, "ghost": 1, "dragon": 1, "dark": 1,
              "steel": 1, "fairy": 1},
    "ice": {"normal": 1, "fire": 2, "water": 1, "electric": 1, "grass": 1, "ice": 0.5, "fighting": 2, "poison": 1,
            "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 2, "ghost": 1, "dragon": 1, "dark": 1, "steel": 2,
            "fairy": 1},
    "fighting": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 1, "poison": 1,
                 "ground": 1, "flying": 2, "psychic": 2, "bug": 0.5, "rock": 0.5, "ghost": 1, "dragon": 1, "dark": 0.5,
                 "steel": 1, "fairy": 2},
    "poison": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 0.5, "ice": 1, "fighting": 0.5,
               "poison": 0.5, "ground": 2, "flying": 1, "psychic": 2, "bug": 0.5, "rock": 1, "ghost": 1, "dragon": 1,
               "dark": 1, "steel": 1, "fairy": 0.5},
    "ground": {"normal": 1, "fire": 1, "water": 2, "electric": 0, "grass": 2, "ice": 2, "fighting": 1, "poison": 0.5,
               "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 0.5, "ghost": 1, "dragon": 1, "dark": 1,
               "steel": 1, "fairy": 1},
    "flying": {"normal": 1, "fire": 1, "water": 1, "electric": 2, "grass": 0.5, "ice": 2, "fighting": 0.5, "poison": 1,
               "ground": 0, "flying": 1, "psychic": 1, "bug": 0.5, "rock": 2, "ghost": 1, "dragon": 1, "dark": 1,
               "steel": 1, "fairy": 1},
    "psychic": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 0.5, "poison": 1,
                "ground": 1, "flying": 1, "psychic": 0.5, "bug": 2, "rock": 1, "ghost": 2, "dragon": 1, "dark": 2,
                "steel": 1, "fairy": 1},
    "bug": {"normal": 1, "fire": 2, "water": 1, "electric": 1, "grass": 0.5, "ice": 1, "fighting": 0.5, "poison": 1,
            "ground": 0.5, "flying": 2, "psychic": 1, "bug": 1, "rock": 2, "ghost": 1, "dragon": 1, "dark": 1,
            "steel": 1, "fairy": 1},
    "rock": {"normal": 0.5, "fire": 0.5, "water": 2, "electric": 1, "grass": 2, "ice": 1, "fighting": 2, "poison": 0.5,
             "ground": 2, "flying": 0.5, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 1, "dark": 1,
             "steel": 2, "fairy": 1},
    "ghost": {"normal": 0, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 0, "poison": 0.5,
              "ground": 1, "flying": 1, "psychic": 1, "bug": 0.5, "rock": 1, "ghost": 2, "dragon": 1, "dark": 2,
              "steel": 1, "fairy": 1},
    "dragon": {"normal": 1, "fire": 0.5, "water": 0.5, "electric": 0.5, "grass": 0.5, "ice": 2, "fighting": 1,
               "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 2,
               "dark": 1, "steel": 1, "fairy": 2},
    "dark": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 2, "poison": 1,
             "ground": 1, "flying": 1, "psychic": 0, "bug": 2, "rock": 1, "ghost": 0.5, "dragon": 1, "dark": 0.5,
             "steel": 1, "fairy": 2},
    "steel": {"normal": 0.5, "fire": 2, "water": 1, "electric": 1, "grass": 0.5, "ice": 0.5, "fighting": 2, "poison": 0,
              "ground": 2, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 0.5, "ghost": 1, "dragon": 0.5, "dark": 1,
              "steel": 0.5, "fairy": 0.5},
    "fairy": {"normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 0.5, "poison": 2,
              "ground": 1, "flying": 1, "psychic": 1, "bug": 0.5, "rock": 1, "ghost": 1, "dragon": 0, "dark": 0.5,
              "steel": 2, "fairy": 1}
}


def custom_input():
    global TYPE1_ENTRY, TYPE2_ENTRY, OUTPUT
    type1 = TYPE1_ENTRY.get()
    type2 = TYPE2_ENTRY.get()
    if not type2:
        type2 = "none"
    super_effective_types = custom_super_effective(type1, type2)
    if super_effective_types:
        OUTPUT.delete('1.0', END)
        OUTPUT.insert(END, show_weaknesses(super_effective_types))


def auto_mode():
    global DEFAULT_ENTRY
    default_pokemon = DEFAULT_ENTRY.get()
    automatic_battle_check(default_pokemon)


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


def take_screenshot():
    image = pyautogui.screenshot()
    image.show()


def search_pokemon(none=None):
    global NAME_ENTRY, OUTPUT, POKEMON
    name = NAME_ENTRY.get()
    print(f"Got {name}")
    if not name[0].isalpha():
        try:
            p = pypokedex.get(dex=int(name))
        except:
            # OUTPUT.delete('1.0', END)
            OUTPUT.insert(END, f"Sorry, the Pokemon with entry #{name} was not found.")
            return
    try:
        p = pypokedex.get(name=name)
    except:
        # OUTPUT.delete('1.0', END)
        OUTPUT.insert(END, f"Sorry, '{name}' was not found, going to try most similar named pokemon.")
        p = pypokedex.get(name=get_similar_name(name))

    POKEMON = p
    super_effective_types = super_effective(p.types)
    if super_effective_types:
        # OUTPUT.delete('1.0', END)
        OUTPUT.insert(END, show_weaknesses(super_effective_types))


def get_similar_name(wrong_name):
    pokemon_list = []

    # Opening a list of strings to search
    with open('pokemon_names.txt', 'r') as f:
        for line in f:
            pokemon_list.append(line.strip())

    # Get a list of similar strings from the list
    matches = difflib.get_close_matches(wrong_name, pokemon_list)
    if matches:
        return matches
    else:
        print("No similarly named pokemon was found.")
        return None


def show_weaknesses(completed_dict):
    global OUTPUT, POKEMON, master_output
    # OUTPUT.delete('1.0', END)
    lock = True
    fourX_damage = []
    twoX_damage = []
    oneX_damage = []
    halfX_damage = []
    quarterX_damage = []
    zeroX_damage = []
    all_damage = []

    sorted_dict = dict(sorted(completed_dict.items(), key=lambda item: item[1], reverse=True))
    for key, value in sorted_dict.items():
        if lock and key == 'ground':
            for ability in POKEMON.abilities:
                if ability.name == "levitate":
                    zeroX_damage.append(key)
                    lock = False
                    break
            continue

        if value == 4:
            fourX_damage.append(key)
            all_damage.append(key)
        elif value == 2:
            twoX_damage.append(key)
            all_damage.append(key)
        elif value == 1:
            oneX_damage.append(key)
            all_damage.append(key)
        elif value == 0.5:
            halfX_damage.append(key)
            all_damage.append(key)
        elif value == 0.25:
            quarterX_damage.append(key)
            all_damage.append(key)
        elif value == 0:
            zeroX_damage.append(key)
            all_damage.append(key)

    num = "%03d" % (POKEMON.dex,)
    # OUTPUT.insert(1.0, f"\t\t\t   {POKEMON.name.capitalize()}(#{num}):\n\n")

    master_output = f"\t\t\t   {POKEMON.name.capitalize()}(#{num}):\n\n"

    if fourX_damage:
        # OUTPUT.insert(1.0, "\t\t\t    4x Damage:\n")
        master_output += "\t\t\t    4x Damage:\n"
        display_type_list(fourX_damage)
    if twoX_damage:
        # OUTPUT.insert(1.0, "\t\t\t    2x Damage:\n")
        master_output += "\t\t\t    2x Damage:\n"
        display_type_list(twoX_damage)

    if not fourX_damage and not twoX_damage:
        # OUTPUT.insert(1.0, f"\t\t\t    {POKEMON.name.capitalize()} doesn't have any weaknesses.\n\n")
        master_output += f"\t\t\t    {POKEMON.name.capitalize()} doesn't have any weaknesses.\n\n"

    if oneX_damage:
        # OUTPUT.insert(1.0, "\t\t\t    1x Damage:\n")
        master_output += "\t\t\t    1x Damage:\n"
        display_type_list(oneX_damage)
    if halfX_damage:
        # OUTPUT.insert(1.0, "\t\t\t    0.5x Damage:\n")
        master_output += "\t\t\t    0.5x Damage:\n"
        display_type_list(halfX_damage)
    if quarterX_damage:
        # OUTPUT.insert(1.0, "\t\t\t    0.25x Damage:\n")
        master_output += "\t\t\t    0.25x Damage:\n"
        display_type_list(quarterX_damage)
    if zeroX_damage:
        # OUTPUT.insert(1.0, "\t\t\t    Immune to:\n")
        master_output += "\t\t\t    Immune to:\n"
        display_type_list(zeroX_damage)

    if not lock:
        # OUTPUT.insert(1.0, f"\n\t\t\t    This pokemon has levitate so [ground] moves have no effect.\n")
        master_output += f"\n\t\t\t    This pokemon has levitate so [ground] moves have no effect.\n"

    OUTPUT.insert(1.0, master_output)

    passed_list_copy = [f"imgs/{item}.png" for item in all_damage]
    try:
        passed_list_copy.insert(0, f"sprites/{POKEMON.name.lower()}.jpg")
    except:
        passed_list_copy.insert(0, f"sprites/{POKEMON.name.lower()}.png")
    lengths = [1, len(fourX_damage), len(twoX_damage), len(oneX_damage), len(halfX_damage), len(quarterX_damage), len(zeroX_damage)]
    display_images(passed_list_copy, lengths)

    OUTPUT.insert(1.0, "======================================================================\n\n")


def display_type_list(type_list):
    global OUTPUT, canvas_output, master_output
    passed_list_copy = [f"imgs/{item}.png" for item in type_list]
    formatted_list = "\t\t\t  "
    for i, string in enumerate(type_list):
        formatted_list += "[{}]".format(string)
        # master_output.append("[{}]".format(string))
        if (i + 1) % 2 == 0:
            formatted_list += "\n\t\t\t  "
            # master_output.append("\n\t\t\t  ")

    # OUTPUT.insert(1.0, formatted_list)
    master_output += formatted_list
    # OUTPUT.insert(1.0, "\n\n")
    master_output += "\n\n"

    # display_images(passed_list_copy)


# Function that gets all matchups against every other type
def super_effective(pokemon_type):
    global OUTPUT
    super_effective_dict1 = {}
    super_effective_dict2 = {}

    # print(f"\t{POKEMON_TO_BE_SEARCHED.capitalize()}: {pokemon_type}")

    if len(pokemon_type) > 1:
        type1 = pokemon_type[0]
        type2 = pokemon_type[1]
    else:
        type1 = pokemon_type[0]
        type2 = ""

    #OUTPUT.insert(END, "\n")
    #OUTPUT.insert(END, f"\t\t{POKEMON.name.capitalize()} is a [{type1}] and [{type2}] type.") if type2 else print(
        #f"\t\t{POKEMON.name.capitalize()} is a [{type1}] type.")

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


def custom_super_effective(type1, type2):
    global OUTPUT
    super_effective_dict1 = {}
    super_effective_dict2 = {}

    if type2.lower() == "none":
        type2 = ""

    OUTPUT.insert(END, "\n")
    OUTPUT.insert(END, f"\t\tThis pokemon is a [{type1}] and [{type2}] type.\n") if type2 else OUTPUT.insert(END,
                                                                                                             f"This pokemon is a [{type1}] type.\n")

    for search_type, matchups_list in type_matchups.items():
        if search_type == type1:
            for subtype, multiplier in matchups_list.items():
                super_effective_dict1.update({subtype: multiplier})
            if type2 == "":
                show_weaknesses(super_effective_dict1)
            else:
                for search_type2, matchups_list2 in type_matchups.items():
                    if search_type2 == type2:
                        for subtype, multiplier in matchups_list2.items():
                            super_effective_dict2.update({subtype: multiplier})
                return double_type_calc(super_effective_dict1, super_effective_dict2)


def double_type_calc(sup_eff_dict1, sup_eff_dict2):
    new_dict = {}

    for key in sup_eff_dict1.keys():
        new_dict[key] = sup_eff_dict1[key] * sup_eff_dict2[key]

    return new_dict


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


def update_pokemon_names(event):
    global ALL_POKEMON, NAME_ENTRY
    current_input = event.widget.get().lower()
    matching_names = [name for name in ALL_POKEMON if name.lower().startswith(current_input)]
    event.widget['values'] = matching_names


'''    if matching_names:
        event.widget.configure(state='readonly')
        event.widget.event_generate('<Down>')
    else:
        event.widget.configure(state='normal')'''


def update_pokemon_names(event):
    global ALL_POKEMON, NAME_ENTRY
    current_input = event.widget.get().lower()
    matching_names = [name for name in ALL_POKEMON if name.lower().startswith(current_input)]
    event.widget['values'] = matching_names

    if matching_names:
        event.widget.event_generate('<Down>')
    else:
        update_pokemon_names_matches(event)


def update_pokemon_names_matches(event):
    global ALL_POKEMON, NAME_ENTRY
    current_input = event.widget.get().lower()
    event.widget['values'] = get_similar_name(current_input)
    event.widget.event_generate('<Down>')


def on_key_release(event):
    global ALL_POKEMON, NAME_ENTRY, AFTER_ID, root
    current_input = event.widget.get().lower()
    matching_names = [name for name in ALL_POKEMON if name.lower().startswith(current_input)]
    event.widget['values'] = matching_names

    if AFTER_ID is not None:
        root.after_cancel(AFTER_ID)

    AFTER_ID = root.after(850, update_pokemon_names, event)


def display_images(image_paths, lengths):
    global canvas_output, IMAGES
    IMAGES = []
    max_size = (150, 150)
    row = .7
    col = 1.1
    count = 0
    for i, length in enumerate(lengths):
        text_id = canvas_output.create_text(100, 215, text="Most Effective Moves")
        for j in range(length):

            # get the next image path
            image_path = image_paths[count]

            # check if file exists
            if not os.path.isfile(image_path):
                print(f"Error: image file not found at {image_path}")
                continue

            # create image object
            image = PILImage.open(image_path)

            # resize the image to fit in the canvas
            image.thumbnail(max_size, PILImage.ANTIALIAS)

            # create PhotoImage object for the image
            photo = ImageTk.PhotoImage(image)

            # add the image to the canvas
            IMAGES.append(photo)
            canvas_output.create_image(col * max_size[0], row * max_size[1], image=photo)

            # save a reference to the image to prevent it from being garbage collected
            canvas_output.image = photo

            count += 1

            if i == 0:
                max_size = (70, 70)
                row = 2.5

            col += 1
            if col > 4:
                col = 1
                row += .5
        if length != 0:
            row += 1
            col = 1
    canvas_output.delete(text_id)


def main():
    global OUTPUT, TYPE1_ENTRY, TYPE2_ENTRY, NAME_ENTRY, DEFAULT_ENTRY, ALL_POKEMON, AFTER_ID, root, canvas_output
    # Create the root window
    root = Tk()
    root.title("Pokemon Weakness Checker")

    # Create the frame for the inputs
    input_frame = Frame(root)

    pokemon_names = []

    # Open the Pokemon names file and add each name to the list
    with open('pokemon_names.txt', 'r') as f:
        for line in f:
            pokemon_names.append(line.strip())

    ALL_POKEMON = pokemon_names

    # Create the labels and entries for the inputs
    name_label = Label(input_frame, text="Pokemon Name/Number:")
    NAME_ENTRY = Combobox(input_frame, values=pokemon_names)

    custom_label = Label(input_frame, text="Custom Type:")
    TYPE1_ENTRY = Entry(input_frame)
    TYPE2_ENTRY = Entry(input_frame)

    auto_label = Label(input_frame, text="Default Pokemon in Auto Mode:")
    DEFAULT_ENTRY = Entry(input_frame)

    # Add the labels and entries to the input frame
    name_label.grid(row=0, column=0)
    NAME_ENTRY.grid(row=0, column=1)

    custom_label.grid(row=1, column=0)
    TYPE1_ENTRY.grid(row=1, column=1)
    TYPE2_ENTRY.grid(row=1, column=2)

    auto_label.grid(row=2, column=0)
    DEFAULT_ENTRY.grid(row=2, column=1)

    # Create the buttons for each input
    name_search_button = Button(input_frame, text="Search", command=search_pokemon)
    custom_search_button = Button(input_frame, text="Search", command=custom_input)
    auto_button = Button(input_frame, text="Start", command=auto_mode)
    screenshot_button = Button(input_frame, text="Take Screenshot", command=take_screenshot)

    # Add the buttons to the input frame
    name_search_button.grid(row=0, column=2)
    custom_search_button.grid(row=1, column=3)
    auto_button.grid(row=2, column=2)
    screenshot_button.grid(row=0, column=3)

    NAME_ENTRY.bind("<KeyRelease>", on_key_release)
    NAME_ENTRY.bind("<Return>", search_pokemon)
    # NAME_ENTRY.pack()

    # Create the frame for the output
    output_frame = Frame(root)

    # Create the output text widget
    OUTPUT = Text(output_frame, height=40, width=70)
    OUTPUT.pack(side=RIGHT, fill=Y, expand=True)

    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)
    OUTPUT.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=OUTPUT.yview)

    canvas_output = Canvas(root, height=500, width=350)
    canvas_output.pack(side=LEFT, fill=BOTH, expand=True)

    # Add the output text widget to the output frame
    # OUTPUT.pack()

    # Add the input and output frames to the root window
    input_frame.pack()
    output_frame.pack()

    # Run the GUI
    root.mainloop()


main()
