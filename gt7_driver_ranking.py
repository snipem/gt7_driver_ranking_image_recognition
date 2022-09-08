from PIL import Image

IN_PYTHONISTA = True
try:
    import appex
except:
    print("Not importing apex, running in non Pythonista mode")
    IN_PYTHONISTA = False

if IN_PYTHONISTA:
    print("pythonista")
    i = appex.get_image()
else:
    i = Image.open("test_data/SHARE_20220908_0312300.jpeg")

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

    if (r + g + b) / 3 >= 200:
        driver_rating += 1

    current_pixel += 1

print(
    "Driver Rating in Current Group:\n%d/%d\n%d%%"
    % (driver_rating, max_driver_rating, driver_rating / max_driver_rating * 100)
)

path = "/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/gt7_driver_ranking.csv"

with open(path, "a") as fil2:
    fil2.write("%d,%d\n" % (driver_rating, max_driver_rating))
