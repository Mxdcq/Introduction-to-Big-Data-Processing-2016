import urllib.request
import sys
import math
from PIL import Image

north_west = sys.argv[1:3]
east_south = sys.argv[3:5]
png = sys.argv[5]

# Lon./lat. to tile numbers
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

# Tile numbers to lon./lat.
def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

# This returns the NW-corner of the square. Use the function with xtile+1
#  and/or ytile+1 to get the other corners.
# With xtile+0.5 & ytile+0.5 it will return the center of the tile.

north_west_xy = deg2num(float(north_west[0]), float(north_west[1]), 13)
east_south_xy = deg2num(float(east_south[0]), float(east_south[1]), 13)
# print(north_west_xy, east_south_xy)

files = {}
for i in range(int(north_west_xy[0]), int(east_south_xy[0]) + 1):
    for j in range(int(north_west_xy[1]), int(east_south_xy[1]) + 1):
        url_one = "http://tile.openstreetmap.org/13/%s/%s.png" % (i, j)
        print(url_one)
        image = urllib.request.urlopen(url_one)
        with open("./Tiles/%s_%s.png" % (i, j), "bw") as f:
            f.write(image.read())
            files[i, j] = ("./Tiles/%s_%s.png" % (i, j))
print(files)

count = len(files)
tile_image = Image.open(files[north_west_xy[0], north_west_xy[1]])
(tile_width, tile_height) = tile_image.size
# print(count, tile_width, tile_height)

blank_img = Image.new("RGB", [tile_width * (east_south_xy[0] - north_west_xy[0] + 2),
                              tile_height * (east_south_xy[1] - north_west_xy[1] + 2)], "white")
for key_x, key_y in files:
    source_image = Image.open(files[key_x, key_y])
    blank_img.paste(source_image, ((key_x - north_west_xy[0]) * 256, (key_y - north_west_xy[1]) * 256))

blank_img.save(png)

# merger image in row
"""def mergei(files, output_file):
    tot = len(files)
    img = Image.open(files[0])
    w, h = img.size[0], img.size[1]
    merge_img = Image.new('RGB', (w * tot, h), 0xffffff)
    i = 0
    for f in files:
        print(f)
        img = Image.open(f)
        merge_img.paste(img, (i, 0))
        i += w
    merge_img.save(output_file)"""

# merger image in line
"""def mergej(files, output_file):
    tot = len(files)
    img = Image.open(files[0])
    w, h = img.size[0], img.size[1]
    merge_img = Image.new('RGB', (w, h * tot), 0xffffff)
    j = 0
    for f in files:
        print(f)
        img = Image.open(f)
        merge_img.paste(img, (0, j))
        j += h
    merge_img.save(output_file)"""

"""mergej(files[0:6], "j_1.png")
mergej(files[6:12], "j_2.png")
mergej(files[12:18], "j_3.png")
mergej(files[18:24], "j_4.png")
mergej(files[24:30], "j_5.png")
mergej(files[30:36], "j_6.png")
mergej(files[36:42], "j_7.png")
mergej(files[42:48], "j_8.png")
mergej(files[48:54], "j_9.png")

mergei(["j_1.png", "j_2.png", "j_3.png",
        "j_4.png", "j_5.png", "j_6.png",
        "j_7.png", "j_8.png", "j_9.png"], png)"""
