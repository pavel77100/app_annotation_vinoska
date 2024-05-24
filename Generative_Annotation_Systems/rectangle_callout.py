import numpy as np
# from PIL import Image, ImageEnhance, ImageOps
import math
# import sys

# import matplotlib.pyplot as plt

import random




class Rectangle_callout():
    # counter = 0
    # size_of_list = (100, 100)
    penny = 3
    r_line = 2
    R_line = 5
    scale = 1
    # image_compress = []
    # image = []

    def __init__(self, sizeofbox, obj_dot, id, size_of_list, image, image_compress):
        self.sizeofbox = sizeofbox
        # print(sizeofbox)
        self.obj_dot = obj_dot
        self.id = id
        self.size_of_list = size_of_list
        self.image = image
        self.image_compress = image_compress

        self.box_zone = np.ones(sizeofbox) * 3
        self.box_zone[1:sizeofbox[0]-1, 1:sizeofbox[1]-1] = 3

        # self.slise_right, self.slise_left, self.slise_y = self.scale_for_circle()
        self.slise_left,self.slise_right, self.slise_y = self.scale_for_circle()
        # self.zone_for_plant_right, self.zone_for_plant_left = self.circle_zone_generator()

        self.zone_for_plant_left, self.zone_for_plant_right = self.circle_zone_generator()

        # Rectangle_callout.counter += 1

        # def circle(y, x, a, b, R, r, s, h, w):

    def scale_for_circle(self):
        m_for_left = np.copy(self.image_compress)+np.copy(self.image)
        m_for_right = np.copy(self.image_compress)+np.copy(self.image)
        m_for_y = np.copy(self.image_compress)
        size_x = self.size_of_list[1]
        size_y = self.size_of_list[0]
        m_for_left3 = np.copy(m_for_left)
        m_for_right3 = np.copy(m_for_right)


        for i in range(self.sizeofbox[1]):
            m_for_left[0:size_y, i:size_x] += m_for_left3[0:size_y, 0:size_x - i]# картинка двигается вправо
            m_for_right[0:size_y, 0:size_x - i] += m_for_right3[0:size_y, i:size_x]# картинка двигается вдево

        m_for_left2 = np.copy(m_for_left)
        m_for_right2 = np.copy(m_for_right)


        for i in range(self.sizeofbox[0]):  # картинка двигается вправо
            m_for_y[0:size_y - i, 0:size_x] += self.image_compress[i:size_y, 0:size_x]
            m_for_left2[0:size_y - i, 0:size_x] += m_for_left[i:size_y, 0:size_x]
            m_for_right2[0:size_y - i, 0:size_x] += m_for_right[i:size_y, 0:size_x]

        return m_for_left2, m_for_right2, m_for_y#!!!!!!!!!!!!!!!!!!!!!!!!!!!


    @staticmethod
    def circle_left(y, x, obj, R, r, s, scr_res):
        r_test = (y - obj[0]) ** 2 + (x - obj[1]) ** 2
        funk_test = (R ** 2 > r_test) and (r ** 2 < r_test)
        tester = 0
        y_test = scr_res[0] - y > s[0]
        # center_test = (scr_res[1] - x > s[1]) and (x > s[1])
        sector_test = not((x<obj[1]) and (y<obj[0]))

        if funk_test:
            if y_test:
                if ( x+s[1] <scr_res[1] ) and (x>1) and sector_test and not(obj[1]-2<x and obj[1]+2>x):
                    tester = 1
                else:
                    tester = 0


        return tester

    @staticmethod
    def circle_right(y, x, obj, R, r, s, scr_res):
        r_test = (y - obj[0]) ** 2 + (x - obj[1]) ** 2
        funk_test = (R ** 2 > r_test) and (r ** 2 < r_test)
        tester = 0
        y_test = scr_res[0] - y > s[0]
        # center_test = (scr_res[1] - x > s[1]) and (x > s[1])
        sector_test = not ((x > obj[1]) and (y < obj[0]) )


        if funk_test:
            if y_test:
                if (x - s[1]> 1) and (scr_res[1] - x > 1) and sector_test and not(obj[1]-2<x and obj[1]+2>x):
                    tester = 1
                else:
                    tester = 0


        return tester



    def dd_tube(self, pixel):
        if pixel == 1:
            return (1)
        elif pixel != 0 and pixel != 1:
            return (0.3)
        else:
            return (0)


    def circle_zone_generator(self):
        print("бокс")

        # k_l_test = np.zeros(Rectangle_callout.size_of_list)
        # k_r_test = np.zeros(Rectangle_callout.size_of_list)
        k_l = np.zeros(
            self.size_of_list) - self.slise_right * 10 - self.slise_y * 10
        k_r = np.zeros(
            self.size_of_list) - self.slise_left * 10 - self.slise_y * 10
        self.zone_for_plant_left = []
        self.zone_for_plant_right = []

        # for i in range(2+self.obj_dot[0] - self.R_line, self.obj_dot[0] + self.R_line-2):
        #
        #     for j in range(2+self.obj_dot[1] - self.R_line, self.obj_dot[1] + self.R_line-2):
        #         try:
        #
        #             k_l[i][j] = self.dd_tube(k_l[i][j])
        #             k_r[i][j] = self.dd_tube(k_r[i][j])
        #
        #
        #             if k_r[i][j] == 0:
        #                 k_r[i][j] += self.circle_right(i, j, self.obj_dot, Rectangle_callout.R_line,
        #                                                Rectangle_callout.r_line, self.sizeofbox, self.size_of_list)
        #             if (k_r[i][j] == 1):
        #                 self.zone_for_plant_right.append([i, j])
        #
        #
        #
        #
        #             if k_l[i][j] == 0:
        #                 k_l[i][j] += self.circle_left(i, j, self.obj_dot, Rectangle_callout.R_line,
        #                                        Rectangle_callout.r_line, self.sizeofbox, self.size_of_list)
        #
        #             if (k_l[i][j] == 1):
        #                 self.zone_for_plant_left.append([i, j])
        #         except:
        #             pass

        for i in range(self.size_of_list[0]):

            for j in range(self.size_of_list[1]):

                k_l[i][j] = self.dd_tube(k_l[i][j])
                k_r[i][j] = self.dd_tube(k_r[i][j])


                if k_r[i][j] == 0:
                    k_r[i][j] += self.circle_right(i, j, self.obj_dot, Rectangle_callout.R_line,
                                                   Rectangle_callout.r_line, self.sizeofbox, self.size_of_list)
                if (k_r[i][j] == 1):
                    self.zone_for_plant_right.append([i, j])




                if k_l[i][j] == 0:
                    k_l[i][j] += self.circle_left(i, j, self.obj_dot, Rectangle_callout.R_line,
                                           Rectangle_callout.r_line, self.sizeofbox, self.size_of_list)

                if (k_l[i][j] == 1):
                    self.zone_for_plant_left.append([i, j])


        return self.zone_for_plant_left, self.zone_for_plant_right

    def coordinate_base_generator(self):

        random_spec = random.randint(0, 1)
        coordinate_base = []
        if random_spec == 0:#ОТРАЗИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            coordinate_base = random.choice(self.zone_for_plant_right)
        else:
            coordinate_base = random.choice(self.zone_for_plant_left)


        return coordinate_base + [random_spec]


    @staticmethod
    def line_creator(y_size, x_size):

        if math.isclose(y_size, 0, abs_tol=1 * 2):
            y_size += 2
        if x_size == 0:
            x_size += 2

        c = np.zeros((y_size, x_size))
        for i in range(y_size):
            for j in range(x_size):
                right = y_size / x_size * j

                right_2 = i / y_size * x_size
                if math.isclose(i, right, abs_tol=Rectangle_callout.scale) or math.isclose(j, right_2,
                                                                                           abs_tol=Rectangle_callout.scale):
                    c[i][j] = Rectangle_callout.penny

        return c, y_size, x_size
    def coordinate_box_gen(self, c):
        if c[2] == 1:
            x1 = c[1]
            y1 = c[0]
            x2 = c[1]+self.sizeofbox[1]
            y2 = c[0]+self.sizeofbox[0]
        else:
            x1 = c[1] - self.sizeofbox[1]
            y1 = c[0]
            x2 = c[1]
            y2 = c[0] + self.sizeofbox[0]
        return [(y1, x1), (y2, x2)]


    def k_find(self, y1, x1):
        try:
            k = (self.obj_dot[0] - y1) / (self.obj_dot[1] - x1)
        except:
            k = (self.obj_dot[0] - y1) / (self.obj_dot[1] - x1 + 1)

        b = self.obj_dot[0] - k*self.obj_dot[1]
        return k, b


    def drawing_of_box(self, c):

        zero = np.zeros(self.size_of_list)

        line_array, y_line, x_line = self.line_creator(abs(c[0] - self.obj_dot[0]),
                                                       abs(c[1] - self.obj_dot[1]))

        if c[2] == 1:

            zero[c[0]:c[0] + self.sizeofbox[0], c[1]:c[1] + self.sizeofbox[1]] = self.box_zone

        else:

            zero[c[0]:c[0] + self.sizeofbox[0], c[1] - self.sizeofbox[1]:c[1]] = self.box_zone

        if c[1] >= self.obj_dot[1]:
            x_plant = (self.obj_dot[1], self.obj_dot[1] + x_line)
        else:
            x_plant = (self.obj_dot[1] - x_line, self.obj_dot[1])

        if c[0] >= self.obj_dot[0]:
            y_plant = (self.obj_dot[0], self.obj_dot[0] + y_line)
        else:
            y_plant = (self.obj_dot[0] - y_line, self.obj_dot[0])

        if (c[1] >= self.obj_dot[1] and c[0] < self.obj_dot[0]) or (c[1] < self.obj_dot[1] and c[0] >= self.obj_dot[0]):
            line_array = np.flip(line_array, 0)

        zero[y_plant[0]:y_plant[1], x_plant[0]:x_plant[1]] += line_array

        return zero, abs(y_line / x_line), y_line, x_line

