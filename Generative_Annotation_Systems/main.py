from genetic4 import genetic_generator_loop
from deserial import deserial_funk_for_class

import json
import time
import numpy as np
import random
from segment import Segment
from fastapi import FastAPI, UploadFile, File
from PIL import Image
from Image_constructor import image_generator_devide


from multiprocessing import Pool, Manager, Process


app = FastAPI()


def sort_dots(V_b_l, U_b_l, V_t_r, U_t_r, dot_array):
   result = []
   for item in dot_array:
      test1 = V_b_l < item["LeaderEnd_V"] <= V_t_r
      test2 = U_b_l < item["LeaderEnd_U"] <= U_t_r
      if test1 and test2:
         result.append(item)
   return result
#
SCALE_STEP = 0.7
FT_TO_MM = 304.8

def generate_automatic_size():
   pass


def generative(arg):
   # result1 = genetic_generator_loop((lenght_V_bt_sg_img, lenght_U_img), img_bottom, img_compress_bottom,
   #                                  array_convert_dots_bt)
   print("Флаг main/generative 1")
   result = genetic_generator_loop(arg[0], arg[1], arg[2], arg[3])
   print("Флаг main/generative 2")

   return result


def generative_process(arg, return_dict):

   result = arg.generator()
   print("Флаг main/generative_process")
   # result = genetic_generator_loop(arg[0], arg[1], arg[2], arg[3])
   print("Флаг main/generative_process")
   return_dict[random.randint(1000000, 9999999)] = result
   return result

"""
def calculation_part(separation, V_min, V_max, U_min, U_max, sheet_scale_convert, koef, dots, img, img_compr,
                     lenght_V_img, lenght_U_img):

   array_of_views = []
   V_full_size = V_max - V_min
   U_full_size = U_max - U_min
   V_step = V_full_size/separation[0]
   U_step = U_full_size / separation[1]
   V_step_img = lenght_V_img // separation[0]
   U_step_img = lenght_U_img // separation[1]

   for i in range(separation[0]):

      for j in range(separation[1]):

         dict_elem = {}

         dict_elem["Number_of_segment"] = str(i) + ":" + str(j)

         dict_elem["V_bottom_right"] = V_min + V_step * i

         dict_elem["U_bottom_right"] = U_min + U_step * j

         V_max = V_min + V_step * i + 1

         U_max = U_min + U_step * j + 1

         dict_elem["Dots"] = sort_dots(V_min, U_min, V_max, U_max, dots)

         dict_elem["Image"] = img

         dict_elem["Image_compress"] = img_compr

         if i != separation[0] - 1:

            V_lenght_img_sep = V_step_img

         else:

            V_lenght_img_sep = lenght_V_img - V_step_img * i

         if j != separation[1] - 1:

            U_lenght_img_sep = U_step_img

         else:

            U_lenght_img_sep = lenght_U_img - U_step_img * j

         pass

"""
@app.post("/data")
async def data(
      scrFile: UploadFile = File(...),
      jsFile: UploadFile = File(...)
   ):

   data = json.load(jsFile.file)
   img = Image.open(scrFile.file)
   dots= deserial_funk_for_class(data)
   sheet_scale_convert = FT_TO_MM / Segment.scale_sheet

   print(dots)

   dots_V = []
   dots_U = []

   for item in dots['Boxes_list']:
      dots_V.append(item["LeaderEnd_V"])
      dots_U.append(item["LeaderEnd_U"])

   # avarage_V = np.mean(dots_V)
   # V_bottom_segment_lenght = avarage_V - dots["BottomLeft_V"]
   # coordinate_V_top_segment = avarage_V
   #
   # avarage_V = np.mean(dots_V)
   # V_bottom_segment_lenght = avarage_V - dots["BottomLeft_V"]
   # coordinate_V_top_segment = avarage_V





   # определяем среднее значение игрик
   avarage_V = np.mean(dots_V)
   V_bottom_segment_lenght = avarage_V - dots["BottomLeft_V"]
   coordinate_V_top_segment = avarage_V

   # определяем среднее значение икс
   avarage_U = np.mean(dots_U)
   U_left_segment_lenght = avarage_U - dots["BottomLeft_U"]
   coordinate_U_left_segment = avarage_U

   segment_sort = {}
   segment_sort["bottom_left"] = sort_dots(dots["BottomLeft_V"], dots["BottomLeft_U"], avarage_V, avarage_U,
                                           dots["Boxes_list"])
   segment_sort["top_left"] = sort_dots(avarage_V, dots["BottomLeft_U"], dots["TopRight_V"], avarage_U,
                                        dots["Boxes_list"])
   segment_sort["bottom_right"] = sort_dots(dots["BottomLeft_V"], avarage_U, avarage_V, dots["TopRight_U"],
                                           dots["Boxes_list"])
   segment_sort["top_right"] = sort_dots(avarage_V, avarage_U, dots["TopRight_V"], dots["TopRight_U"],
                                        dots["Boxes_list"])

   lenght_V = dots["TopRight_V"] - dots["BottomLeft_V"]
   lenght_U = dots["TopRight_U"] - dots["BottomLeft_U"]

   lenght_V_on_list = lenght_V * sheet_scale_convert
   lenght_U_on_list = lenght_U * sheet_scale_convert

   lenght_V_img = np.around(np.divide(lenght_V_on_list, SCALE_STEP)).astype(int)
   lenght_U_img = np.around(np.divide(lenght_U_on_list, SCALE_STEP)).astype(int)

   img_full, img_full_compress = image_generator_devide(img, lenght_V_img, SCALE_STEP, lenght_U_img)

   lenght_V_bt_sg_img = np.around(np.divide(V_bottom_segment_lenght * sheet_scale_convert, SCALE_STEP)).astype(int)
   lenght_V_tp_sg_img = lenght_V_img - lenght_V_bt_sg_img



   array_of_screens = []

   test_top = len(segment_sort["top_left"]) + len(segment_sort["top_right"]) > 15

   test_bottom = len(segment_sort["bottom_left"]) + len(segment_sort["bottom_right"]) > 15


   if test_bottom:
      dots_bottom = segment_sort["bottom_left"] + segment_sort["bottom_right"]
      dots_U_list = []

      for item in dots_bottom:
         dots_U_list.append(item["LeaderEnd_U"])

      avarage_U_bottom = np.mean(dots_U_list)
      U_left_segment_lenght_bt = avarage_U_bottom - dots["BottomLeft_U"]
      coordinate_U_left_segment_bt = avarage_U_bottom

      lenght_U_left_sg_img_bt = np.around(np.divide(U_left_segment_lenght_bt * sheet_scale_convert, SCALE_STEP)).astype(int)
      lenght_U_right_sg_img_bt = lenght_U_img - lenght_U_left_sg_img_bt



      img_left, img_compress_left = img_full[0:lenght_V_bt_sg_img, 0:lenght_U_left_sg_img_bt], img_full_compress[0:lenght_V_bt_sg_img, 0:lenght_U_left_sg_img_bt]
      img_right, img_compress_right = img_full[0:lenght_V_bt_sg_img, lenght_U_left_sg_img_bt:lenght_U_img], img_full_compress[0:lenght_V_bt_sg_img, lenght_U_left_sg_img_bt:lenght_U_img]

      left = Segment(dots["BottomLeft_V"], dots["BottomLeft_U"], coordinate_V_top_segment, coordinate_U_left_segment_bt,
                            img_left, img_compress_left, lenght_V_bt_sg_img, lenght_U_left_sg_img_bt,
                            scale_conv = sheet_scale_convert, optimaze_k=SCALE_STEP, name="bottom_left")

      right = Segment(dots["BottomLeft_V"], coordinate_U_left_segment_bt, coordinate_V_top_segment, dots["TopRight_U"],
                  img_right, img_compress_right, lenght_V_bt_sg_img, lenght_U_right_sg_img_bt,
                  scale_conv=sheet_scale_convert, optimaze_k=SCALE_STEP, name="bottom_right")

      # left.dot_sort(dots["Boxes_list"])
      # left.dots_to_segment_coordinates()
      #
      # right.dot_sort(dots["Boxes_list"])
      # right.dots_to_segment_coordinates()

      array_of_screens.append(left)
      array_of_screens.append(right)

   else:
      img_bottom, img_compress_bottom = img_full[0:lenght_V_bt_sg_img, 0:lenght_U_img], img_full_compress[
                                                                                            0:lenght_V_bt_sg_img,
                                                                                            0:lenght_U_img]

      bottom = Segment(dots["BottomLeft_V"], dots["BottomLeft_U"], coordinate_V_top_segment, dots["TopRight_U"],
                     img_bottom, img_compress_bottom, lenght_V_bt_sg_img, lenght_U_img,
                     scale_conv=sheet_scale_convert, optimaze_k=SCALE_STEP, name="bottom")

      # bottom.dot_sort(dots["Boxes_list"])
      # bottom.dots_to_segment_coordinates()

      array_of_screens.append(bottom)




   if test_top:
      dots_top = segment_sort["top_left"] + segment_sort["top_right"]
      dots_U_list = []

      for item in dots_top:
         dots_U_list.append(item["LeaderEnd_U"])

      avarage_U_top = np.mean(dots_U_list)
      U_left_segment_lenght_tp = avarage_U_top - dots["BottomLeft_U"]
      coordinate_U_left_segment_tp = avarage_U_top

      lenght_U_left_sg_img_tp = np.around(np.divide(U_left_segment_lenght_tp * sheet_scale_convert, SCALE_STEP)).astype(int)
      lenght_U_right_sg_img_tp = lenght_U_img - lenght_U_left_sg_img_tp


      #
      # img_left, img_compress_left = img_full[0:lenght_V_tp_sg_img, 0:lenght_U_left_sg_img_tp], img_full_compress[0:lenght_V_tp_sg_img, 0:lenght_U_left_sg_img_tp]
      # img_right, img_compress_right = img_full[0:lenght_V_tp_sg_img, lenght_U_left_sg_img_tp:lenght_U_img], img_full_compress[0:lenght_V_tp_sg_img, lenght_U_left_sg_img_tp:lenght_U_img]

      img_left_tp, img_compress_left_tp = (img_full[lenght_V_bt_sg_img:lenght_V_img, 0:lenght_U_left_sg_img_tp],
                                     img_full_compress[lenght_V_bt_sg_img:lenght_V_img, 0:lenght_U_left_sg_img_tp])

      img_right_tp, img_compress_right_tp = (img_full[lenght_V_bt_sg_img:lenght_V_img, lenght_U_left_sg_img_tp:lenght_U_img],
                                       img_full_compress[lenght_V_bt_sg_img:lenght_V_img, lenght_U_left_sg_img_tp:lenght_U_img])

      left = Segment(coordinate_V_top_segment, dots["BottomLeft_U"], dots["TopRight_V"], coordinate_U_left_segment_tp,
                            img_left_tp, img_compress_left_tp, lenght_V_tp_sg_img, lenght_U_left_sg_img_tp,
                            scale_conv = sheet_scale_convert, optimaze_k=SCALE_STEP, name="top_left")

      right = Segment(coordinate_V_top_segment, coordinate_U_left_segment_tp, dots["TopRight_V"], dots["TopRight_U"],
                  img_right_tp, img_compress_right_tp, lenght_V_tp_sg_img, lenght_U_right_sg_img_tp,
                  scale_conv=sheet_scale_convert, optimaze_k=SCALE_STEP, name="top_right")

      # left.dot_sort(dots["Boxes_list"])
      # left.dots_to_segment_coordinates()
      #
      # right.dot_sort(dots["Boxes_list"])
      # right.dots_to_segment_coordinates()



      array_of_screens.append(left)
      array_of_screens.append(right)

   else:

      img_top, img_compress_top = img_full[lenght_V_bt_sg_img:lenght_V_img, 0:lenght_U_img], img_full_compress[lenght_V_bt_sg_img:lenght_V_img, 0:lenght_U_img]

      top = Segment(coordinate_V_top_segment, dots["BottomLeft_U"], dots["TopRight_V"], dots["TopRight_U"],
                     img_top, img_compress_top, lenght_V_tp_sg_img, lenght_U_img,
                     scale_conv=sheet_scale_convert, optimaze_k=SCALE_STEP, name="top")
      #
      # top.dot_sort(dots["Boxes_list"])
      # top.dots_to_segment_coordinates()

      array_of_screens.append(top)


   # img_bottom, img_compress_bottom = img_full[0:lenght_V_bt_sg_img, 0:lenght_U_img], img_full_compress[0:lenght_V_bt_sg_img, 0:lenght_U_img]
   #
   # img_top, img_compress_top = img_full[lenght_V_bt_sg_img:lenght_V_img, 0:lenght_U_img], img_full_compress[
   #                                                                                   lenght_V_bt_sg_img:lenght_V_img,
   #                                                                                   0:lenght_U_img]
   #
   # segment_bottom = Segment(dots["BottomLeft_V"], dots["BottomLeft_U"], coordinate_V_top_segment, dots["TopRight_U"],
   #                          img_bottom, img_compress_bottom, lenght_V_bt_sg_img, lenght_U_img,
   #                          scale_conv = sheet_scale_convert, optimaze_k=SCALE_STEP)
   #
   # segment_top = Segment(coordinate_V_top_segment, dots["BottomLeft_U"], dots["TopRight_V"], dots["TopRight_U"],
   #                       img_top, img_compress_top, lenght_V_tp_sg_img, lenght_U_img,
   #                       scale_conv = sheet_scale_convert, optimaze_k=SCALE_STEP)

   # segment_bottom.dot_sort(dots["Boxes_list"])
   #
   # segment_top.dot_sort(dots["Boxes_list"])
   #
   # segment_bottom.dots_to_segment_coordinates()
   #
   # segment_top.dots_to_segment_coordinates()

   manager = Manager()
   return_dict = manager.dict()
   processes = []
   for item in array_of_screens:
      item.dot_sort(dots["Boxes_list"])
      if item.dot_array != []:

         item.dots_to_segment_coordinates()
         p = Process(target=generative_process, args=(item, return_dict))
         p.start()
         processes.append(p)

   for item in processes:
      item.join()


   result = return_dict.values()

   otvet = []
   for pr in result:
      otvet.extend(pr)

   return json.dumps(otvet)

# @app.post("/da2ta")
# async def da2ta(
#       scrFile: UploadFile = File(...),
#
#       jsFile: UploadFile = File(...)
#    ):
#
#    # pool_genetic = Pool(3)
#    #
#    # box_for_separate = (2,1)
#
#    data = json.load(jsFile.file)
#    img = Image.open(scrFile.file)
#    dots= deserial_funk_for_class(data)
#
#
#    sheet_scale_convert = FT_TO_MM / Segment.scale_sheet
#
#    print(dots)
#
#    dots_V = []
#
#    for item in dots['Boxes_list']:
#       dots_V.append(item["LeaderEnd_V"])
#    avarage_V = np.mean(dots_V)
#
#    V_bottom_segment_lenght = avarage_V - dots["BottomLeft_V"]
#
#    coordinate_V_top_segment = avarage_V
#
#    lenght_V = dots["TopRight_V"] - dots["BottomLeft_V"]
#
#    lenght_U = dots["TopRight_U"] - dots["BottomLeft_U"]
#
#    # lenght_V_segment = lenght_V/2
#
#    lenght_V_on_list = lenght_V * sheet_scale_convert
#    lenght_U_on_list = lenght_U * sheet_scale_convert
#    lenght_V_img = np.around(np.divide(lenght_V_on_list, SCALE_STEP)).astype(int)
#    lenght_U_img = np.around(np.divide(lenght_U_on_list, SCALE_STEP)).astype(int)
#    lenght_V_bt_sg_img = np.around(np.divide(V_bottom_segment_lenght * sheet_scale_convert, SCALE_STEP)).astype(int)
#    lenght_V_tp_sg_img = lenght_V_img - lenght_V_bt_sg_img
#
#    img_full, img_full_compress = image_generator_devide(img, lenght_V_img, SCALE_STEP, lenght_U_img)
#
#    img_bottom, img_compress_bottom = img_full[0:lenght_V_bt_sg_img, 0:lenght_U_img], img_full_compress[0:lenght_V_bt_sg_img, 0:lenght_U_img]
#
#    img_top, img_compress_top = img_full[lenght_V_bt_sg_img:lenght_V_img, 0:lenght_U_img], img_full_compress[
#                                                                                      lenght_V_bt_sg_img:lenght_V_img,
#                                                                                      0:lenght_U_img]
#    segment_bottom = Segment(dots["BottomLeft_V"], dots["BottomLeft_U"], coordinate_V_top_segment, dots["TopRight_U"])
#
#    segment_top = Segment()
#
#    # fig4 = plt.figure()
#    # plt.pcolor(img_bottom, cmap="cool", edgecolors='k')
#    # plt.colorbar()
#    #
#    # fig5 = plt.figure()
#    # plt.pcolor(img_top, cmap="cool", edgecolors='k')
#    # plt.colorbar()
#    #
#    # plt.show()
#
#    array_bt_sg = sort_dots(dots["BottomLeft_V"], dots["BottomLeft_U"], coordinate_V_top_segment, dots["TopRight_U"],
#                            dots["Boxes_list"])
#    array_tp_sg = sort_dots(coordinate_V_top_segment, dots["BottomLeft_U"], dots["TopRight_V"], dots["TopRight_U"],
#                            dots["Boxes_list"])
#
#    array_convert_dots_bt = dots_to_segment_coordinates(array_bt_sg, dots["BottomLeft_V"], dots["BottomLeft_U"],
#                                                         sheet_scale_convert, SCALE_STEP)
#
#    array_convert_dots_tp = dots_to_segment_coordinates(array_tp_sg, coordinate_V_top_segment, dots["BottomLeft_U"],
#                                                        sheet_scale_convert, SCALE_STEP)
#
#    result = []
#    result1 = [(lenght_V_bt_sg_img, lenght_U_img), img_bottom, img_compress_bottom, array_convert_dots_bt, "bt"]
#
#    result2 = [(lenght_V_tp_sg_img, lenght_U_img), img_top, img_compress_top, array_convert_dots_tp, "tp"]
#
#    res = []
#    if array_convert_dots_bt != []:
#       res.append(result1)
#
#    if array_convert_dots_tp != []:
#       res.append(result2)
#
#    print("Флаг main 1")
#
#    start_rasch = time.time()
#    print("Флаг main 2")
#
#    print("создали менеджер")
#    manager = Manager()
#    print("создали возвращающий dict")
#    return_dict = manager.dict()
#    print("создали p1")
#    p1 = Process(target=generative_process, args=(result1, return_dict))
#    print("создали p2")
#    p2 = Process(target=generative_process, args=(result2, return_dict))
#
#    p1.start()
#    print("старт p2")
#    p2.start()
#    print("джоин p1")
#    p1.join()
#    print("джоин p2")
#    p2.join()
#    print("proc закончился")
#
#    result = return_dict.values()
#    #
#    # with Pool(2) as pool:
#    #    result = pool.map(generative, res)
#
#    print("Флаг main 3")
#    end_rasch = time.time()
#    print("Флаг main 4")
#    print(f"На генерацию ушло {end_rasch - start_rasch}")
#    print("Флаг main 5")
#
#    otvet = []
#
#    dict_array = {}
#    dict_array
#
#    # for item in result[0]:
#    #
#    #    otvet1 = {}
#    #    otvet1["V"] = dots["BottomLeft_V"]+item["V"]*SCALE_STEP/sheet_scale_convert
#    #    otvet1["U"] = dots["BottomLeft_U"] + item["U"] * SCALE_STEP / sheet_scale_convert
#    #
#    #    otvet1["LeaderElbow_U"] = dots["BottomLeft_U"] + item["LeaderElbow_U"] * SCALE_STEP / sheet_scale_convert
#    #    otvet1["LeaderElbow_V"] = dots["BottomLeft_V"] + item["LeaderElbow_V"] * SCALE_STEP / sheet_scale_convert
#    #
#    #    otvet1["TagId"] = item["TagId"]
#    #    otvet.append(otvet1)
#    #
#    #
#    # for item in result[1]:
#    #    otvet2 = {}
#    #    otvet2["V"] = coordinate_V_top_segment+item["V"]*SCALE_STEP/sheet_scale_convert
#    #    otvet2["U"] = dots["BottomLeft_U"] + item["U"] * SCALE_STEP / sheet_scale_convert
#    #
#    #    otvet2["LeaderElbow_U"] = dots["BottomLeft_U"] + item["LeaderElbow_U"] * SCALE_STEP / sheet_scale_convert
#    #    otvet2["LeaderElbow_V"] = coordinate_V_top_segment + item["LeaderElbow_V"] * SCALE_STEP / sheet_scale_convert
#    #
#    #    otvet2["TagId"] = item["TagId"]
#    #    otvet.append(otvet2)
#
#
#    print("Флаг 2")
#    return (json.dumps(otvet))



@app.post("/test")
async def testtest():
   hello = "Hello, world (annotation)!"
   return (json.dumps(hello))