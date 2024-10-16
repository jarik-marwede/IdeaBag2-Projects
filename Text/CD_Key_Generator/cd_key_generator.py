#!/usr/bin/env python3
"""Generates random keys.

Title:
CD Key Generator

Description:
Develop a program which generates keys for an application
that you may put on a CD.
A great example would be the keys
you use for installation of a major software product
from companies like Microsoft or Adobe.
Have the user specify the length of keys and
the types of characters they can use in the key
(only letters, letters & numbers or just numbers, any special characters etc).
Your program will then generate a random key value that can also be verified.
For added complexity,
create the mechanism for validating the generated key.
"""
import os
import random


def generate_key(characters: tuple, length: int, file_name: str | None = None) -> str:
    """Return random string containing specified characters."""
    random_result = random.choices(characters, k=length)
    string = ""

    for character in random_result:
        string += character
    # checking whether key already exists in file
    if file_name:
        with open(file_name, "r") as file:
            if string in file.read():
                return generate_key(characters, length)
    return string


def add_key_to_file(key: str, file_name: str):
    """Append specified key to specified file."""
    if os.path.isfile(file_name) is False:
        with open(file_name, "w") as file:
            file.write(key)
    else:
        with open(file_name, "a") as file:
            file.write("\n" + key)


def new_key(characters: tuple, length: int, file_name: str):
    """Generate new key and append to file."""
    key = generate_key(characters, length, file_name)
    add_key_to_file(key, file_name)


def _start_interactively():
    """Start the program interactively through the command line."""
    while True:
        choice = input("Do you want to generate a key or also append it to a file (gen|append): ")
        if choice == "gen":
            characters = tuple(input("Please specify which characters the generator should use: "))
            length = int(input("How long should the key be: "))
            print(generate_key(characters, length))
        elif choice == "append":
            characters = tuple(input("Please specify which characters the generator should use: "))
            length = int(input("How long should the key be: "))
            file_name = input("Please specify the file name that the key should be appended to: ")
            new_key(characters, length, file_name)
        print("")


if __name__ == "__main__":
    _start_interactively()
