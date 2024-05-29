from deap import base, algorithms
from deap import creator
from deap import tools

import math
from segment import Segment
import random

from datetime import datetime

import numpy as np
import algelitism
import Image_constructor

from rectangle_callout import Rectangle_callout
import time

time_cikl_1 = 0
time_cikl_2 = 0
time_cikl_3 = 0
time_mut_1 = 0
R_MAX = 50
R_MIN = 7

MARGIN_LINE = 1
SCALE_STEP = 0.7
scale_step_int = int(math.ceil(SCALE_STEP))

POPULATION_SIZE = 120  # количество индивидуумов в популяции
P_CROSSOVER = 0.35  # вероятность скрещивания
P_MUTATION = 0.25  # вероятность мутации индивидуума
MAX_GENERATIONS = 2000  # максимальное количество поколений
HALL_OF_FAME_SIZE = 4  # размер зала славы
FINE_FOR_TUBE = 3.0  # штраф за пересечение с системой

def zero_centers(image, bx):
    test_img = np.copy(image)
    # y = len(image)
    # x = len(image[0])
    for elem in bx:
        for i in range(elem.obj_dot[0]-4,elem.obj_dot[0]+4):
            for j in range(elem.obj_dot[1]-4, elem.obj_dot[1]+4):
                try:
                    test_img[i][j] = 0
                except:
                    pass

    return test_img

def genetic_generator_loop(size_of_list, k, k_kompress, data_box):

    r_min_convert = np.around(np.divide(R_MIN, SCALE_STEP)).astype(int)
    r_max_convert = np.around(np.divide(R_MAX, SCALE_STEP)).astype(int)

    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    RANDOM_SEED = 42
    # random.seed(RANDOM_SEED)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    Rectangle_callout.R_line = r_max_convert
    Rectangle_callout.r_line = r_min_convert
    Rectangle_callout.penny = FINE_FOR_TUBE

    array_for_change = np.where(k > 2)
    arrayfor_change_y = array_for_change[0]
    arrayfor_change_x = array_for_change[1]
    # print(array_for_change)
    # print(arrayfor_change_y)
    # print(arrayfor_change_x)






    # -------------------------------------------------------------
    array_k_list = list(zip(arrayfor_change_y, arrayfor_change_x))
    # -------------------------------------------------------------






    print(array_k_list)

    boxes_array = []

    global_counter = len(data_box)
    for i in range(global_counter):
        boxes_array.append(Rectangle_callout((data_box[i]["Height"], data_box[i]["Width"]),
                                             (data_box[i]["LeaderEnd_V"], data_box[i]["LeaderEnd_U"]),
                                             data_box[i]["TagId"], size_of_list, k, k_kompress))
    global_counter = len(boxes_array)
    k_for_test_width_zeros = zero_centers(k, boxes_array)

    print("global_counter")
    print(global_counter)

    print("cоздание боксов закончилось")
    def deserial():
        pass

    def create_box(total):
        boxes = []
        for n in range(global_counter):
            t = boxes_array[n].coordinate_base_generator()
            boxes.extend(t)
        return creator.Individual(boxes)

    toolbox = base.Toolbox()
    toolbox.register("create_box", create_box, global_counter)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.create_box)
    population = toolbox.populationCreator(n = POPULATION_SIZE)

    def clash_detect(pixel):
        if pixel > 3.1:
            return (pixel)
        else:
            return (0)

    def penny_detect_vertical(array):
        counter = 0
        for item in array:
            if item < 5:
                counter += 1
        return (counter)

    start = time.time()

    def find_s(list1, list2):

        x1 = list1[0][1]
        y1 = list1[0][0]
        x2 = list1[1][1]
        y2 = list1[1][0]
        x3 = list2[0][1]
        y3 = list2[0][0]
        x4 = list2[1][1]
        y4 = list2[1][0]

        left = max(x1, x3)
        top = min(y2, y4)
        right = min(x2, x4)
        bottom = max(y1, y3)

        width = right - left+2
        height = top - bottom+2

        if (width < 0 or height < 0):
            return 0
        else:
            return height * width

    def correct_vector(p1, p2, size_b):
        # p1[0] = p1[0] + size_b[0]/2
        p2[0] = p2[0] + int(np.ceil(size_b[0] / 2))
        if p1[0] == p2[0]:
            p2 = (p2[0] + 1, p2[1])
        x_min = min(p1[1], p2[1])

        if p2[1] == x_min:
            p_t = p2
            p2 = p1
            p1 = p_t
        return [p1, p2]

    def k_find(p1):
        x1 = p1[0][1]
        y1 = p1[0][0]
        x2 = p1[1][1]
        y2 = p1[1][0]

        c = 0
        if x2 == x2:
            c = 1

        k = (y2 - y1) / (x2 - x1 + c)
        b = y2 - k * x2
        return (k, b)

    def diag_line_detect(kb_1, kb_2, l1, l2):

        k1 = kb_1[0]
        b1 = kb_1[1]
        k2 = kb_2[0]
        b2 = kb_2[1]

        if k1 == k2:
            k1 += 0.00001

        x = (b2 - b1) / (k1 - k2)
        y = k2 * x + b2

        test1 = (l1[0][1] <= x <= l1[1][1]) and (l2[0][1] <= x <= l2[1][1])
        test2 = (l1[0][0] <= y <= l1[1][0]) and (l2[0][0] <= y <= l2[1][0])

        if test1 and test2:
            return 1
        else:
            return 0


    def vinoska_and_box(kb, line_coord, box_coord):

            b_x1 = box_coord[0][1]
            b_y1 = box_coord[0][0]
            b_x2 = box_coord[1][1]
            b_y2 = box_coord[1][0]

            l_x1 = line_coord[0][1]
            l_y1 = line_coord[0][0]
            l_x2 = line_coord[1][1]
            l_y2 = line_coord[1][0]

            y_max = max(l_y1, l_y2)
            y_min = min(l_y1, l_y2)

            k = kb[0]
            b = kb[1]

            if k == 0:
                k += 0.00001

            test_start = not ((l_x2 < b_x1) or (l_x1 > b_x2) or (y_max < b_y1) or (y_min > b_y2))
            test_finalle = True

            if test_start:
                if (l_x1 < b_x1 < l_x2):
                    iter_1_y = k * b_x1 + b
                    test_1 = y_min < iter_1_y < y_max
                    test_2 = b_y1 < iter_1_y < b_y2
                    if test_1 and test_2:
                        test_finalle = False

                if (l_x1 < b_x2 < l_x2) and test_finalle:
                    iter_1_y = k * b_x2 + b
                    test_1 = y_min < iter_1_y < y_max
                    test_2 = b_y1 < iter_1_y < b_y2
                    if test_1 and test_2:
                        test_finalle = False

                if (y_min < b_y1 < y_max) and test_finalle:
                    iter_3_x = (b_y1 - b) / k
                    test_1 = l_x1 < iter_3_x < l_x2
                    test_2 = b_x1 < iter_3_x < b_x2
                    if test_1 and test_2:
                        test_finalle = False

                if (y_min < b_y2 < y_max) and test_finalle:
                    iter_3_x = (b_y2 - b) / k
                    test_1 = l_x1 < iter_3_x < l_x2
                    test_2 = b_x1 < iter_3_x < b_x2
                    if test_1 and test_2:
                        test_finalle = False

            if not(test_finalle):
                return 1
            else:
                return 0

    global time_cikl_1
    time_cikl_1 = 0

    global time_cikl_2
    time_cikl_2 = 0

    global time_cikl_3
    time_cikl_3 = 0

    global time_mut_1
    time_mut_1 = 0

    def dd_tube(pixel):
        if pixel > 3:
            return (3)
        else:
            return (0)

    def draw_line2(l_y, l_x, coord, k_b, box_img):
            # print("TTTTTT!!!!!!!!!!!!!!TTTTTTTTTTT1!!!!!!!!!!!!!!!!!!!")

            y_min = min(coord[0][0], coord[1][0])
            y_max = max(coord[0][0], coord[1][0])
            # l_y = max(coord[0][0], coord[1][0]) - min(coord[0][0], coord[1][0])
            #
            # if k_b[0] < 0:
            #     b_test = l_y
            # else:
            #     b_test = 0

            ball_for_diag_line = 0

            # for i in range(y_min, y_max):
            #     right = (i - b_test) / k_b[0]
            #     for j in range(coord[0][1], coord[1][1]):
            #         left = k_b[0] * j + b_test
            #         if math.isclose(i, left, abs_tol=1) and math.isclose(j, right, abs_tol=1):
            #             if k_for_test_width_zeros[i][j] > 2:
            #                 ball_for_diag_line += 1

            for i in range(y_min, y_max):
                # xxx1 = int((i - k_b[1]) / k_b[0])
                x_1 = math.floor((i - k_b[1]) / k_b[0])
                x_2 = math.ceil((i + 1 - k_b[1]) / k_b[0])

                x_min = math.floor(min(x_1, x_2))
                x_max = math.ceil(max(x_1, x_2))

                for j in range(x_min-1, x_max+1):
                    if box_img[i][j]:
                        ball_for_diag_line += 1

                # x_max = math.ceil((i - k_b[1]) / k_b[0])

                # xxx2 = math.floor((i - 1 - k_b[1]) / k_b[0] - 1)
                #
                # xxx3 = math.ceil((i + 1 - k_b[1]) / k_b[0] + 1)

                # try:
                #
                #
                #
                #
                #     # for j in range(coord[0][1], coord[1][1]):
                #     #     left = k_b[0] * j + b_test
                #     #     if math.isclose(i, left, abs_tol=1) and math.isclose(j, right, abs_tol=1):
                #     #         if k_for_test_width_zeros[i][j] > 2:
                #     #             ball_for_diag_line += 1
                # except:
                #     pass

            if ball_for_diag_line > 15:
                # print(ball_for_diag_line)
                return 0.5

            else:

                return 0.5*ball_for_diag_line/15
            # else:
            #     return ball_for_diag_line/1

            # return ball_for_diag_line


    def boxFitness(individual):
        # print(__name__)
        box_coord = []
        line_coord = []
        k_b = []
        box_dirt = 0
        diapas_for_line = []
        lenght_y = []
        lenght_x = []
        line_dirt = 0

        coordinates = np.reshape(individual, (-1, 3))
        start_c1 = time.time()
        for boxes_array_item, coordinates_item in zip(boxes_array, coordinates):
            cc = boxes_array_item.coordinate_box_gen(coordinates_item)
            box_coord.append(cc)
            bd = np.sum(k[cc[0][0]:cc[1][0], cc[0][1]:cc[1][1]])
            if bd > 1:
                box_dirt += 1
            cl = correct_vector(boxes_array_item.obj_dot, [coordinates_item[0], coordinates_item[1]], boxes_array_item.sizeofbox)
            line_coord.append(cl)
            kb = k_find(cl)
            k_b.append(kb)
            diapas_for_line.append([[min(cl[0][0], cl[1][0]) - scale_step_int, cl[0][1] - scale_step_int],
                                    [max(cl[0][0], cl[1][0]) + scale_step_int,
                                     cl[1][1] + scale_step_int]])  # [[y_min, x_min], [y_max, x_max]]
            ld = draw_line2(abs(cl[0][0] - cl[1][0]), abs(cl[0][1] - cl[1][1]), cl, kb, boxes_array_item.box_width_zero)
            # ld = 0
            line_dirt += ld
            lenght_y.append(abs(cl[0][0] - cl[1][0]))
            lenght_x.append(abs(cl[0][1] - cl[1][1]))

        end_c1 = time.time()
        global time_cikl_1
        time_cikl_1 += (end_c1 - start_c1)
        square = 0
        lines = 0
        l_and_b = 0
        start_c2 = time.time()

        for i in range(global_counter - 1):
            for j in range(i+1, global_counter):
                t = find_s(box_coord[i], box_coord[j])
                if t > 3:
                    square += 1
                lines += diag_line_detect(k_b[i], k_b[j], diapas_for_line[i], diapas_for_line[j])
        end_c2 = time.time()
        global time_cikl_2
        time_cikl_2 += (end_c2 - start_c2)
        start_c3 = time.time()

        for k_b_item, line_coord_item in zip(k_b, line_coord):
            for box_coord_item in box_coord:
                l_and_b += vinoska_and_box(k_b_item, line_coord_item, box_coord_item)

        end_c3 = time.time()
        global time_cikl_3

        time_cikl_3 += (end_c3 - start_c3)

        mean_lenght_y = np.mean(lenght_y)
        mean_lenght_x = np.mean(lenght_x)

        radius_mean = (mean_lenght_y ** 2 + mean_lenght_x ** 2) ** 0.5

        s = (square + lines + l_and_b + box_dirt + line_dirt) * 7000 + math.ceil(
            (radius_mean) / (r_max_convert) * 200) + \
            (max(mean_lenght_y, mean_lenght_x) / min(mean_lenght_y, mean_lenght_x) - 1) * 80
        return s,

    def crossingover_box(ind1, ind2):
        place = random.randrange(3, global_counter * 3 + 1, 3)
        ind1[place:], ind2[place:] = ind2[place:], ind1[place:]
        return ind1, ind2

    def mutBox(individual, indpb):
        start_m1 = time.time()
        for i in range(len(individual)):
            if i % 3 == 0:
                if random.random() < indpb:
                    coordinate = boxes_array[int(i / 3)].coordinate_base_generator()
                    individual[i] = coordinate[0]
                    individual[i + 1] = coordinate[1]
                    individual[i + 2] = coordinate[2]
        end_m1 = time.time()
        global time_mut_1
        time_mut_1 += (end_m1 - start_m1)
        return individual,

    toolbox.register("evaluate", boxFitness)
    toolbox.register("select", tools.selTournament, tournsize=3)
    # toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mate", crossingover_box)
    toolbox.register("mutate", mutBox, indpb=P_MUTATION)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    population, logbook = algelitism.eaSimpleElitism(population, toolbox,
                                                     cxpb=P_CROSSOVER,
                                                     mutpb=P_MUTATION,
                                                     ngen=MAX_GENERATIONS,
                                                     halloffame=hof,
                                                     stats=stats,
                                                     verbose=True)
    def diag_line_detect_for_show(kb_1, kb_2, l1, l2, i1, i2):
        # print()

        k1 = kb_1[0]
        b1 = kb_1[1]
        k2 = kb_2[0]
        b2 = kb_2[1]

        if k1 == k2:
            k1 += 0.00001
        x = (b2 - b1) / (k1 - k2)
        y = k2 * x + b2

        test1 = (l1[0][1] - SCALE_STEP <= x <= l1[1][1] + SCALE_STEP) and (
                l2[0][1] - SCALE_STEP <= x <= l2[1][1] + SCALE_STEP)

        test2 = (min(l1[0][0], l1[1][0]) - SCALE_STEP <= y <= max(l1[0][0], l1[1][0]) + SCALE_STEP) and (
                min(l2[0][0], l2[1][0]) - SCALE_STEP <= y <= max(l2[0][0], l2[1][0]) + SCALE_STEP)

        if test1 and test2:
            return 1
        else:
            return 0

    yyy = []
    yyy.append(hof.items[0])
    best = hof.items[0]




    # if True:
    #     import matplotlib.pyplot as plt
    #     from PIL import Image, ImageEnhance, ImageOps
    #     for i in range(len(yyy)):
    #         best = hof.items[i]
    #         pole_x = len(k[0])
    #         pole_y = len(k)
    #         Pimage1 = np.zeros((pole_y, pole_x))
    #         coordinate_best = np.reshape(best, (-1, 3))
    #
    #         for count in range(len(coordinate_best)):
    #             cl = correct_vector(boxes_array[count].obj_dot, [coordinate_best[count][0], coordinate_best[count][1]], boxes_array[count].sizeofbox)
    #             kb = k_find(cl)
    #             zero, tg, y_line, x_line = boxes_array[count].drawing_of_box(coordinate_best[count])
    #
    #             y_min = min(cl[0][0], cl[1][0])
    #             y_max = max(cl[0][0], cl[1][0])
    #             # l_y = max(coord[0][0], coord[1][0]) - min(coord[0][0], coord[1][0])
    #             #
    #             # if k_b[0] < 0:
    #             #     b_test = l_y
    #             # else:
    #             #     b_test = 0
    #
    #             ball_for_diag_line = 0
    #
    #             # for i in range(y_min, y_max):
    #             #     right = (i - b_test) / k_b[0]
    #             #     for j in range(coord[0][1], coord[1][1]):
    #             #         left = k_b[0] * j + b_test
    #             #         if math.isclose(i, left, abs_tol=1) and math.isclose(j, right, abs_tol=1):
    #             #             if k_for_test_width_zeros[i][j] > 2:
    #             #                 ball_for_diag_line += 1
    #
    #
    #
    #             for i in range(y_min, y_max):
    #                 # xxx1 = int((i - k_b[1]) / k_b[0])
    #                 x_1 = math.floor((i - kb[1]) / kb[0])
    #                 x_2 = math.ceil((i + 1 - kb[1]) / kb[0])
    #
    #                 x_min = math.floor(min(x_1, x_2))
    #                 x_max = math.ceil(max(x_1, x_2))
    #
    #                 for j in range(x_min-1, x_max+1):
    #                     zero[i][j]+=1
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #             Pimage1 += zero
    #
    #
    #         m = np.copy(k)
    #         matrix = np.sum([m, Pimage1], axis=0)*40
    #
    #         # plt.ion()
    #
    #         fig4 = plt.figure()
    #         matrix2 = ImageOps.flip(Image.fromarray(matrix))
    #         # plt.pcolor(matrix, cmap="cool", edgecolors='k')
    #         plt.imshow(matrix2, cmap="cool")
    #         plt.colorbar()
    #
    #         for count in range(len(coordinate_best)):
    #             plt.text(coordinate_best[count][1], coordinate_best[count][0], count)
    #             plt.text(coordinate_best[count][1], coordinate_best[count][0] + 3,
    #                      f"[{coordinate_best[count][0]}, {coordinate_best[count][1]}, {coordinate_best[count][2]}")
    #
    #         coordinates = coordinate_best
    #         box_coord = []
    #         line_coord = []
    #         k_b = []
    #         box_dirt = 0
    #         # print("****---***---***---****")
    #         for item, coord in zip(boxes_array, coordinates):
    #             cc = item.coordinate_box_gen(coord)
    #             box_coord.append(cc)
    #             cl = correct_vector(item.obj_dot, [coord[0], coord[1]], item.sizeofbox)
    #             line_coord.append(cl)
    #             kb = k_find(cl)
    #             k_b.append(kb)
    #             tttt = np.sum(item.image[min(cc[0][0],cc[1][0]):max(cc[0][0],cc[1][0]), cc[0][1]:cc[1][1]])
    #             box_dirt += tttt
    #
    #         square = 0
    #         lines = 0
    #         # l_and_b = 0
    #         for i in range(global_counter):
    #             for j in range(i, global_counter):
    #                 if i != j:
    #                     # print()
    #                     # print()
    #                     # print(f"Сочетание выносок {i} и {j}")
    #                     t = find_s(box_coord[i], box_coord[j])
    #                     if t > 0:
    #                         square += 1
    #                     tt = diag_line_detect_for_show(k_b[i], k_b[j], line_coord[i], line_coord[j], i, j)
    #                     lines += tt
    #                     # print()
    #                     # print()
    #
    #         # print("****---***---***---****")
    #         # plt.savefig(f'otchet_2/{random.randint(10000,99999)}.png')
    #         # plt.show(block=False)
    #         # plt.draw()
    #
    #     # print(hof.items)
    #
    #     # fig22332 = plt.figure()
    #     # plt.plot(maxFitnessValues, color='red')
    #     # plt.plot(meanFitnessValues, color='green')
    #     # plt.xlabel('Поколение')
    #     # plt.ylabel('Макс/средняя приспособленность')
    #     # plt.title('Зависимость максимальной и средней приспособленности от поколения')
    #     #
    #     # plt.ioff()
    #     #
    #     # plt.show(block=False)
    #     manager = plt.get_current_fig_manager()
    #     manager.resize(*manager.window.maxsize())
    #     now = datetime.now()
    #     current_time = now.strftime("%H.%M.%S" + str(random.randint(1000,9999)))
    #     plt.savefig(current_time+'.png')
    #     # figManager = plt.get_current_fig_manager()
    #     # figManager.window.showMaximized()
    #     plt.show()
    #     # print(k)
    #     # coordinate_best = np.reshape(hof.items[0], (-1, 3))
    # # except:
    # #     print("error")


    result = []
    coordinate_best = np.reshape(hof.items[0], (-1, 3))

    for i in range(len(coordinate_best)):
        if coordinate_best[i][2] == 0:
            result.append({"V":(coordinate_best[i][0] + boxes_array[i].sizeofbox[0] / 2*1),
                           "U":(coordinate_best[i][1] - boxes_array[i].sizeofbox[1] / 2*1),
                           "TagId":boxes_array[i].id,
                           "LeaderElbow_U": coordinate_best[i][1] ,
                           "LeaderElbow_V": coordinate_best[i][0] + boxes_array[i].sizeofbox[0] / 2*1})

        else:
            result.append({"V": (coordinate_best[i][0] + boxes_array[i].sizeofbox[0] / 2*1),
                           "U": (coordinate_best[i][1] + boxes_array[i].sizeofbox[1] / 2*1),
                           "TagId":boxes_array[i].id,
                           "LeaderElbow_U": coordinate_best[i][1],
                           "LeaderElbow_V": coordinate_best[i][0] + (boxes_array[i].sizeofbox[0] / 2)*1})

    print(result)
    return result