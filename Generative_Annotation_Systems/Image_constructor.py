import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import math
# import matplotlib.pyplot as plt



FINE_FOR_TUBE = 3.0


def chech_tube(pixel):
    if pixel < 100:
        return (FINE_FOR_TUBE)
    else:
        return (0)

def chech_tube2(pixel):
    if pixel < 200:
        return (FINE_FOR_TUBE)
    else:
        return (0)

def image_convert(img, sheet_height, scale_step, sheet_width):
    pass

def point_sort(x_min, y_min, x_max, y_max, dot_array):
    result = []
    for item in dot_array:
        test1 = x_min < item[1]<x_max
        test2 = y_min <item[0]<y_max
        if test1 and test2: result.append(item)
    pass

def image_main_genetator(img, sheet_height, scale_step, sheet_width):
    # img = Image.open(path)
    img = img.convert("L")

    img = img.resize((sheet_width, sheet_height))

    factor = 2000
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(factor)
    img_test = np.array(ImageOps.flip(img))
    img2 = np.array(np.vectorize(chech_tube)(img_test))

    img_compress = img.resize((int(sheet_width/3), int(sheet_height/3)))

    factor = 1000
    enhancer = ImageEnhance.Sharpness(img_compress)
    img_compress = enhancer.enhance(factor)

    img_compress = img_compress.resize((sheet_width, sheet_height))
    img_test_compress = np.array(ImageOps.flip(img_compress))
    img2_compress = np.array(np.vectorize(chech_tube2)(img_test_compress))

    # fig1111 = plt.figure()
    #
    # plt.pcolor(img2_compress, cmap="plasma", edgecolors='k')
    # plt.colorbar()
    #
    # fig1 = plt.figure()
    #
    # plt.imshow(np.array(img), cmap="gray")
    # plt.colorbar()
    # fig2 = plt.figure()
    #
    # plt.pcolor(img2, cmap="plasma", edgecolors='k')
    # plt.colorbar()
    #
    # plt.show()

    return img2, img2_compress

def image_generator(img, sheet_height, scale_step, sheet_width):
    # img = Image.open(path)
    img = img.convert("L")

    img = img.resize((sheet_width, sheet_height))

    factor = 2000
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(factor)
    img_test = np.array(ImageOps.flip(img))
    img2 = np.array(np.vectorize(chech_tube)(img_test))

    img_compress = img.resize((int(sheet_width/3), int(sheet_height/3)))

    factor = 1000
    enhancer = ImageEnhance.Sharpness(img_compress)
    img_compress = enhancer.enhance(factor)

    img_compress = img_compress.resize((sheet_width, sheet_height))
    img_test_compress = np.array(ImageOps.flip(img_compress))
    img2_compress = np.array(np.vectorize(chech_tube2)(img_test_compress))

    # fig1111 = plt.figure()
    #
    # plt.pcolor(img2_compress, cmap="plasma", edgecolors='k')
    # plt.colorbar()
    #
    # fig1 = plt.figure()
    #
    # plt.imshow(np.array(img), cmap="gray")
    # plt.colorbar()
    # fig2 = plt.figure()
    #
    # plt.pcolor(img2, cmap="plasma", edgecolors='k')
    # plt.colorbar()
    #
    # plt.show()

    return img2, img2_compress


def line_creatot(y_size, x_size, scale, penny):

    if math.isclose(y_size, 0, abs_tol=1*2):
        y_size +=2
    if x_size == 0:
        x_size += 2

    c = np.zeros((y_size, x_size))
    for i in range(y_size):
        for j in range(x_size):
            right = y_size / x_size * j

            right_2 = i / y_size * x_size
            if math.isclose(i, right, abs_tol=scale) or math.isclose(j, right_2, abs_tol=scale):
                c[i][j]=penny



    return c, y_size,x_size


def image_generator_devide(img, sheet_height, scale_step, sheet_width):
    # img = Image.open(path)
    img = img.convert("L")

    img = img.resize((sheet_width, sheet_height))

    factor = 2000
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(factor)
    img_test = np.array(ImageOps.flip(img))
    img2 = np.array(np.vectorize(chech_tube)(img_test))

    img_compress = img.resize((int(sheet_width/3), int(sheet_height/3)))

    factor = 1000
    enhancer = ImageEnhance.Sharpness(img_compress)
    img_compress = enhancer.enhance(factor)

    img_compress = img_compress.resize((sheet_width, sheet_height))
    img_test_compress = np.array(ImageOps.flip(img_compress))
    img2_compress = np.array(np.vectorize(chech_tube2)(img_test_compress))

    # fig1111 = plt.figure()
    #
    # plt.pcolor(img2_compress, cmap="plasma", edgecolors='k')
    # plt.colorbar()
    #
    # fig1 = plt.figure()
    #
    # plt.imshow(np.array(img), cmap="gray")
    # plt.colorbar()
    # fig2 = plt.figure()
    #
    # plt.pcolor(img2, cmap="plasma", edgecolors='k')
    # plt.colorbar()
    #
    # plt.show()

    return img2, img2_compress
