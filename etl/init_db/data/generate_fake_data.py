import json
import pandas as pd
from faker import Faker
import random

fake = Faker()
short_filenames = [f"number{i}" for i in range(700_000)]

FILE_EXTENSIONS = [
    ".au",
    ".iff",
    ".voc",
    ".wav",
    ".mp3"
]
FILE_EXT_NUMBER = [1, 2, 3, 4]
STATUS = [1, 0]

SHORT_NAME_TABLE_DATA = []
FULL_NAME_TABLE_DATA = []

for short_filename in short_filenames:
    number = random.sample(FILE_EXT_NUMBER, k=1)
    extentions = random.sample(FILE_EXTENSIONS, k=number[0])
    status = random.sample(STATUS, k=1)
    SHORT_NAME_TABLE_DATA.append(
        {
            "name": short_filename,
            "status": status[0]
        }
    )
    for this_extention in extentions:
        FULL_NAME_TABLE_DATA.append(
            {
                "name": short_filename + this_extention,
                "status": None
            }
        )

FULL_NAME_TABLE_DATA = random.sample(FULL_NAME_TABLE_DATA, k=500_000)

pd.DataFrame(SHORT_NAME_TABLE_DATA).to_csv("full_data.csv")
pd.DataFrame(FULL_NAME_TABLE_DATA).to_csv("short_data.csv")
