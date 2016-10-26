# ming

import io
import json
import math
from PIL import Image
from PIL import ImageDraw, ImageFont

def get_location_speed(file_name):
    bus_data_points = {}
    bus_location_data = {}
    bus_speed_data = {}
    with open('./%s' % file_name, 'r') as busdata_json:
        databuf = io.StringIO()  # Initialize an empty StringIO file.
        for line in busdata_json:  # Read one line from the original file.
            databuf.write(line)  # Write the read line into the StringIO file.
            if line == '}\n':  # Did we reach the end of a top-level dictionary?
                databuf.seek(0)  # Set the StringIO to enable reading from its beginning.
                data = json.load(databuf)  # Read the single top-level JSON dictionary.
                databuf.close()  # Discard the current StringIO object.
                databuf = io.StringIO()  # Initialize a new empty StringIO object.
                # Now data can be used as a normal Python dictionary.
                # print(data.keys())  # One example: lists the keys of the data dictionary.
                for i in data['body']:
                    if i['monitoredVehicleJourney']['lineRef'] not in bus_data_points:
                        bus_data_points[i['monitoredVehicleJourney']['lineRef']] = [
                            i['recordedAtTime'] + i['monitoredVehicleJourney']['vehicleRef']]
                        bus_speed_data[i['monitoredVehicleJourney']['lineRef']] = [
                            i['monitoredVehicleJourney']['speed']]
                        bus_location_data[i['monitoredVehicleJourney']['lineRef']] = [
                            i['monitoredVehicleJourney']['vehicleLocation']]
                    if (i['recordedAtTime'] + i['monitoredVehicleJourney']['vehicleRef']) not in bus_data_points[
                        i['monitoredVehicleJourney']['lineRef']]:
                        bus_data_points[i['monitoredVehicleJourney']['lineRef']] += [
                            i['recordedAtTime'] + i['monitoredVehicleJourney']['vehicleRef']]
                        bus_speed_data[i['monitoredVehicleJourney']['lineRef']] += [
                            i['monitoredVehicleJourney']['speed']]
                        bus_location_data[i['monitoredVehicleJourney']['lineRef']] += [
                            i['monitoredVehicleJourney']['vehicleLocation']]
        databuf.close()  # Discard the StringIO file also in the end.
    return bus_location_data, bus_speed_data


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


location, speed = get_location_speed('busdata.json')
print(location['17'])
print(speed['17'])

upper_left_x, upper_left_y = deg2num(61.5376, 23.626, 21)


def routespeeds(image_name, location_data, speed_value, line_number):
    img = Image.open('./%s' % image_name)
    draw = ImageDraw.Draw(img)
    coordinate_list = []
    for i in range(len(location_data[line_number])):
        coordinate_list.append(
            deg2num(float(location_data[line_number][i]['latitude']), float(location_data[line_number][i]['longitude']),
                    21))
    print(coordinate_list)
    pixels = []
    for i in range(len(coordinate_list)):
        pixels.append((coordinate_list[i][0] - upper_left_x + 144, coordinate_list[i][1] - upper_left_y + 64))
    print(pixels)
    # print(len(pixels))
    pixels_size = []
    for i in range(len(speed[line_number])):
        pixels_size.append(draw.textsize(speed[line_number][i], font=ImageFont.load_default()))
    # print(pixels_size)
    occupied_pixel_area = []
    # for i in range(len(location_data[line_number])):
    #     draw.text(pixels[i], speed[line_number][i], font=ImageFont.load_default(), fill=(0, 0, 0))
    for i in range(len(location_data[line_number])):
        if occupied_pixel_area == []:
            draw.text(pixels[i], speed[line_number][i], font=ImageFont.load_default(), fill=(0, 0, 0))
            occupied_pixel_area.append(pixels[i])
        if occupied_pixel_area != []:
            flag = 0
            for j in range(len(occupied_pixel_area)):
                if not (occupied_pixel_area[j][0] + 24 > pixels[i][0] and pixels[i][0] + 24 > occupied_pixel_area[j][0] and
                                occupied_pixel_area[j][1] + 11 > pixels[i][1] and pixels[i][1] + 11 >
                    occupied_pixel_area[j][1]):
                    flag += 1
                else:
                    flag += 0
            if flag == len(occupied_pixel_area):
                draw.text(pixels[i], speed[line_number][i], font=ImageFont.load_default(), fill=(0, 0, 0))
                occupied_pixel_area.append(pixels[i])
    # draw.text((0, 0), "Ming Xiaodong", font=ImageFont.load_default(), fill=(0, 0, 0))
    img.save('routespeeds.png')
    return img.show()

# print(deg2num(61.5376, 23.626, 17), deg2num(61.4269, 23.964, 17))
routespeeds('tampere.png', location, speed, '17')
