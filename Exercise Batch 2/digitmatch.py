# ming

from PIL import Image
from PIL import ImageFilter
from sklearn import svm

def change_image_format(image_name):
    img = Image.open('./digits/%s' % image_name)
    pixels = img.load()
    black_xy = []
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if (img.getpixel((i, j))[0] + 15) <= img.getpixel((i, j))[2] and (img.getpixel((i, j))[1] + 15) <= img.getpixel((i, j))[2]:
                pixels[i, j] = (0, 0, 0)
                black_xy += [(i, j)]
            else:
                pixels[i, j] = (255, 255, 255)
    x_list = []
    y_list = []
    for i in range(len(black_xy)):
        x_list.append(black_xy[i][0])
        y_list.append(black_xy[i][1])
    # upper_left = (min(x_list), min(y_list))
    # lower_right = (max(x_list), max(y_list))
    box = (min(x_list), min(y_list), max(x_list), max(y_list))
    region = img.crop(box)
    square_xy = 0
    if max(x_list) - min(x_list) >= max(y_list) - min(y_list):
        square_xy = max(x_list) - min(x_list)
    else:
        square_xy = max(y_list) - min(y_list)
    blank_img = Image.new("RGB", (square_xy, square_xy), "white")
    offset = (int((square_xy - (max(x_list) - min(x_list))) / 2), int((square_xy - (max(y_list) - min(y_list))) / 2))
    blank_img.paste(region, offset)
    blank_img = blank_img.resize((16, 16)).convert(mode='L').filter(ImageFilter.Kernel((3,3), [0.0625, 0.125, 0.0625, 0.125, 0.25, 0.125, 0.0625, 0.125, 0.0625]))
    # print(img.format, img.size, img.mode, pixels)
    # print(black_xy)
    # print(upper_left, lower_right)
    # img.show()
    # region.show()
    pixels_16_16 = blank_img.load()
    matrix_8_8 = [[0 for i in range(8)] for i in range(8)]
    one_dimension_list = []
    for i in range(8):
        for j in range(8):
            matrix_8_8[j][i] = (256 - ((pixels_16_16[2*i,2*j] + pixels_16_16[2*i+1, 2*j] + pixels_16_16[2*i, 2*j+1] + pixels_16_16[2*i+1, 2*j+1]) / 4)) / 16
    for i in range(8):
        for j in range(8):
            one_dimension_list.append(matrix_8_8[i][j])
    # print(blank_img.format, blank_img.size, blank_img.mode)
    # print(matrix_8_8)
    # print(one_dimension_list)
    # blank_img.show()
    return one_dimension_list

hand_written_data_list = []
hand_written_class_list = []
for i in range(10):
    hand_written_data_list.append(change_image_format('%s.png' % i))
    hand_written_class_list.append(i)
# print(hand_written_data_list)
# print(hand_written_class_list)
classifier = svm.SVC(gamma=0.001)
classifier.fit(hand_written_data_list, hand_written_class_list)
print(classifier.predict(hand_written_data_list))
