import re
import csv
from dataclasses import dataclass, astuple

russian_upper = list(map(chr, range(ord("А"), ord("Я") + 1)))
russian_lower = list(map(chr, range(ord("а"), ord("я") + 1)))
english_lower = list(map(chr, range(ord("a"), ord("z") + 1)))


@dataclass
class User:
    email: str
    address: str
    offset: int


def load_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        users = []

        for item in reader:
            users.append(User(item[0], item[1], 0))

        return users


def save_to_file(filename, data):
    # newline = "" for Windows
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        for item in data:
            writer.writerow(item)


def find_offset(target, source):
    if target in russian_lower and source in russian_lower:
        target_index = russian_lower.index(target)
        source_index = russian_lower.index(source)

        return target_index - source_index


def make_offset(char, offset):
    if char in russian_upper:
        index = russian_upper.index(char)

        return russian_upper[(index + offset) % len(russian_upper)]

    if char in russian_lower:
        index = russian_lower.index(char)

        return russian_lower[(index + offset) % len(russian_lower)]

    if char in english_lower:
        index = english_lower.index(char)

        return english_lower[(index + offset) % len(english_lower)]


def decrypt(user):
    flat = re.findall(r" ..\.\d+", user.address)[0][1]
    offset = find_offset("к", flat)

    address = []
    email = []

    for char in user.address:
        if re.match(r"[а-яА-Я]+", char):
            address.append(make_offset(char, offset))
        else:
            address.append(char)

    for char in user.email:
        if re.match(r"[a-z]+", char):
            email.append(make_offset(char, offset))
        else:
            email.append(char)

    building = re.search(r"д.\d+", "".join(address))
    address.insert(building.start(), " ")

    user.address = "".join(address)
    user.email = "".join(email)
    user.offset = -offset


def main():
    users = load_from_file("in.csv")
    result = []

    for user in users:
        decrypt(user)
        result.append(astuple(user))
        print(user)

    save_to_file("out.csv", result)


if __name__ == "__main__":
    main()
