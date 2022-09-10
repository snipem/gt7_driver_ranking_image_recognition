import os
from datetime import datetime

from PIL import Image


class Rating:
    def __init__(self, character, level):
        self.character = character
        self.level = level


def detect_rating_character(cropped_image: Image) -> Rating:
    characters = [
        {
            "character": "D",
            "level": 1,
            "light_points": [(3, 3), (3, 30)],
            "dark_points": [(26, 19)],
        },
        {
            "character": "C",
            "level": 2,
            "light_points": [(42, 3), (42, 31)],
            "dark_points": [(26, 19)],
        },
        {
            "character": "B",
            "level": 3,
            "light_points": [(3, 3), (3, 32), (22, 17)],
            "dark_points": [],
        },
        {
            "character": "A",
            "level": 4,
            "light_points": [(6, 33), (45, 33)],  # TODO A flanks to not fit the picture
            "dark_points": [],
        },
        # {
        #     "character": "A+",
        #     "level": 5,
        #     "light_points": [],
        #     "dark_points": [],
        # },
        {
            "character": "S",
            "level": 6,
            "light_points": [(3, 32), (42, 3)],
            "dark_points": [],
        },
    ]

    light_threshold = 200
    dark_threshold = 200

    px = cropped_image.load()

    character_matches = []

    for character in characters:
        # Assume it will match
        this_character_is_matching = True
        for light_point in character["light_points"]:
            r, g, b = px[light_point[0], light_point[1]]
            if not (r + g + b) / 3 >= light_threshold:
                this_character_is_matching = False

        for dark_point in character["dark_points"]:
            r, g, b = px[dark_point[0], dark_point[1]]
            if (r + g + b) / 3 < dark_threshold:
                this_character_is_matching = False

        if this_character_is_matching:
            character_matches.append(character)

    if len(character_matches) != 1:
        # Use this as the default return value if nothing matches
        return Rating(character="X",level=0)

    return Rating(character=character_matches[0]["character"], level=character_matches[0]["level"])


def parse_playstation_app_picture_file_time_stamp(path: str) -> datetime.date:
    # There is a bug in the PlayStation iOS app, where 12 hour is used instead of
    # 24 hour with no indication of a.m. and p.m. We only use the date for now
    parsed = datetime.strptime(path.split(".")[0], "SHARE_%Y%m%d_%H%M%S0")
    return parsed.date()


IN_PYTHONISTA = True
# This is the default iCloud path of Pythonista
csv_path = "/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/gt7_driver_ranking.csv"
try:
    import appex
except:
    print("Not importing apex, running in non Pythonista mode")
    IN_PYTHONISTA = False

if IN_PYTHONISTA:
    i = appex.get_image()
    picture_filepath = appex.get_file_path()
else:
    picture_filepath = "test_data/SHARE_20220908_0312300.jpeg"
    i = Image.open(picture_filepath)
    csv_path = "gt7_driver_ranking.csv"

PROGRESS_BAR_START_X = 1820
PROGRESS_BAR_START_Y = 314
PROGRESS_BAR_END_X = 1892
PROGRESS_BAR_END_Y = PROGRESS_BAR_START_Y

px = i.load()

current_pixel = 0
driver_rating = 0
max_driver_rating = PROGRESS_BAR_END_X - PROGRESS_BAR_START_X

while PROGRESS_BAR_START_X + current_pixel <= PROGRESS_BAR_END_X:
    r, g, b = px[PROGRESS_BAR_START_X + current_pixel, PROGRESS_BAR_START_Y]

    if not IN_PYTHONISTA:
        print(
            "x=%d, y=%d, r=%d, g=%d, b=%d"
            % (PROGRESS_BAR_START_X + current_pixel, PROGRESS_BAR_START_Y, r, g, b)
        )

    # 200 is a good threshold for light grey
    # grayish colors have r,g,b on the same level
    if (r + g + b) / 3 >= 200:
        driver_rating += 1

    current_pixel += 1

# Recognize the character of the driver and sportsmanship class

box_driver_rating_class = (1924, 259, 1970, 293)
box_sportsmanship_rating_class = (2120, 259, 2166, 293)

image_driver_rating_class = i.crop(box_driver_rating_class)
image_sportsmanship_rating_class = i.crop(box_sportsmanship_rating_class)

driver_rating_class = detect_rating_character(image_driver_rating_class)
sportsmanship_rating_class = detect_rating_character(image_sportsmanship_rating_class)

timestamp = parse_playstation_app_picture_file_time_stamp(
    os.path.basename(picture_filepath)
)

print(
    "Driver Rating: %d\nMax Driver Rating: %d\nPercentage: %d%%\nDate: %s\nDriver Class: %s\nSportsmanship Class: %s"
    % (
    driver_rating, max_driver_rating, driver_rating / max_driver_rating * 100, timestamp, driver_rating_class.character,
    sportsmanship_rating_class.character)
)

with open(csv_path, "a") as f:
    f.write(
        "%s,%d,%d,%d,%s,%d,%s\n"
        % (timestamp.strftime("%Y-%m-%d"),
           driver_rating, max_driver_rating,
           driver_rating_class.level, driver_rating_class.character,
           sportsmanship_rating_class.level, sportsmanship_rating_class.character)
    )
