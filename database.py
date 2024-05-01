import pygame
import csv
import pandas as pd

opt = [{"full_screen": "off", "resolution": "1280x720", "volume": "30"}]
kb1 = [{"up": "W",
        "down": "S",
        "left": "A",
        "right": "D",
        "jump": "G",
        "dash": "H",
        "normal attack": "F",
        "strong attack": "R",
        "special attack": "T"}]
kb2 = [{"up": "UP",
        "down": "DOWN",
        "left": "LEFT",
        "right": "RIGHT",
        "jump": "K",
        "dash": "L",
        "normal attack": "J",
        "strong attack": "U",
        "special attack": "I"}]


# with open("settings.csv", mode="w") as file:
#     fieldnames = opt[0].keys()
#     writer = csv.DictWriter(file, fieldnames = fieldnames)
#     writer.writeheader()
#     writer.writerows(opt)
#
# with open("keyBinds.csv", mode="w") as file:
#         fieldnames = kb1[0].keys()
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(kb1)
#         writer.writerows(kb2)
