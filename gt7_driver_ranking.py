import os
from datetime import datetime

from PIL import Image


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
    print("pythonista")
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

timestamp = parse_playstation_app_picture_file_time_stamp(
    os.path.basename(picture_filepath)
)

print(
    "Driver Rating: %d\nMax Driver Rating: %d\nPercentage: %d%%\nDate: %s"
    % (driver_rating, max_driver_rating, driver_rating / max_driver_rating * 100, timestamp)
)

with open(csv_path, "a") as f:
    f.write(
        "%s,%d,%d\n"
        % (timestamp.strftime("%Y-%m-%d"), driver_rating, max_driver_rating)
    )
