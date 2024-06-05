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
STATUS = [1, 0]

SHORT_NAME_TABLE_DATA = []
FULL_NAME_TABLE_DATA = []

for short_filename in short_filenames:
    extentions = random.sample(FILE_EXTENSIONS, k=1)
    status = random.sample(STATUS, k=1)
    SHORT_NAME_TABLE_DATA.append(
        {
            "name": short_filename,
            "status": status[0]
        }
    )
    FULL_NAME_TABLE_DATA.append(
        {
            "name": short_filename + extentions[0],
            "status": None
        }
    )

FULL_NAME_TABLE_DATA = random.sample(FULL_NAME_TABLE_DATA, k=500_000)

pd.DataFrame(SHORT_NAME_TABLE_DATA).to_csv("short_data.csv")
pd.DataFrame(FULL_NAME_TABLE_DATA).to_csv("full_data.csv")
