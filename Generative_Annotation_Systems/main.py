from genetic4 import genetic_generator_loop
from deserial import deserial_funk_for_class

import json
import time
import numpy as np

from segment import Segment
from fastapi import FastAPI, UploadFile, File
from PIL import Image
from Image_constructor import image_generator_devide


from multiprocessing import Pool



def dots_to_segment_coordinates(array_dots, V_start, U_start, scale_conv, optimaze_k):
   for item in array_dots:
      item["Height"] = np.around(np.divide(item["Width"]*scale_conv,optimaze_k * 2.2)).astype(int)
      item["Width"] = np.around(np.divide(item["Height"] * scale_conv,optimaze_k * 2.2)).astype(int)
      item["LeaderEnd_V"] = np.ceil(np.divide((item["LeaderEnd_V"] - V_start)  * scale_conv,optimaze_k)).astype(int)
      item["LeaderEnd_U"] = np.ceil(np.divide((item["LeaderEnd_U"] - U_start) * scale_conv,optimaze_k)).astype(int)

   return array_dots


app = FastAPI()

# @app.post("/data")
# async def data(
#
#       scrFile: UploadFile = File(...),
#       jsFile: UploadFile = File(...)
#    ):
#    data = json.load(jsFile.file)
#    img = Image.open(scrFile.file)
#    automatic_size_list, automatic_size_box, automatic_coord_obj, id_s , x0, y0, scale_mn, size_orig_l= deserial_funk(data)
#
#    gen, size_list_g_y = genetic_generator(automatic_size_list, automatic_size_box, automatic_coord_obj, id_s, img)
#    scale_for_list= size_orig_l/size_list_g_y
#
#    result = serial(gen, x0, y0, scale_for_list)
#
#
#    return (json.dumps(result))
#
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

@app.post("/data3333333")
async def test222(

      scrFile: UploadFile = File(...),
      jsFile: UploadFile = File(...)
   ):

   pool_genetic = Pool(3)

   box_for_separate = (2,1)

   data = json.load(jsFile.file)
   img = Image.open(scrFile.file)
   dots= deserial_funk_for_class(data)
   Segment.scale_sheet = dots["Scale"]


   sheet_scale_convert = FT_TO_MM / Segment.scale_sheet

   print(dots)

   coordinate_V_top_segment = (dots["TopRight_V"] + dots["BottomLeft_V"])/2

   lenght_V = dots["TopRight_V"] - dots["BottomLeft_V"]
   lenght_U = dots["TopRight_U"] - dots["BottomLeft_U"]

   lenght_V_segment = lenght_V/2

   lenght_V_on_list = lenght_V*sheet_scale_convert
   lenght_U_on_list = lenght_U*sheet_scale_convert

   lenght_V_img = np.around(np.divide(lenght_V_on_list, SCALE_STEP)).astype(int)
   lenght_U_img = np.around(np.divide(lenght_U_on_list, SCALE_STEP)).astype(int)

   lenght_V_bt_sg_img = np.around(lenght_V_img/2).astype(int)
   lenght_V_tp_sg_img = lenght_V_img - lenght_V_bt_sg_img

   img_full, img_full_compress = image_generator_devide(img, lenght_V_img, SCALE_STEP, lenght_U_img)

   img_bottom, img_compress_bottom = img_full[0:lenght_V_bt_sg_img, 0:lenght_U_img], img_full_compress[0:lenght_V_bt_sg_img, 0:lenght_U_img]
   img_top, img_compress_top = img_full[lenght_V_bt_sg_img:lenght_V_img, 0:lenght_U_img], img_full_compress[
                                                                                     lenght_V_bt_sg_img:lenght_V_img,
                                                                                     0:lenght_U_img]

   # fig4 = plt.figure()
   # plt.pcolor(img_bottom, cmap="cool", edgecolors='k')
   # plt.colorbar()
   #
   # fig5 = plt.figure()
   # plt.pcolor(img_top, cmap="cool", edgecolors='k')
   # plt.colorbar()
   #
   # plt.show()


   array_bt_sg = sort_dots(dots["BottomLeft_V"], dots["BottomLeft_U"], coordinate_V_top_segment, dots["TopRight_U"],
                           dots["Boxes_list"])
   array_tp_sg = sort_dots(coordinate_V_top_segment, dots["BottomLeft_U"], dots["TopRight_V"], dots["TopRight_U"],
                           dots["Boxes_list"])

   array_convert_dots_bt = dots_to_segment_coordinates(array_bt_sg, dots["BottomLeft_V"], dots["BottomLeft_U"],
                                                        sheet_scale_convert, SCALE_STEP)

   array_convert_dots_tp = dots_to_segment_coordinates(array_tp_sg, coordinate_V_top_segment, dots["BottomLeft_U"],
                                                       sheet_scale_convert, SCALE_STEP)


   result = []
   result1 = [(lenght_V_bt_sg_img, lenght_U_img), img_bottom, img_compress_bottom, array_convert_dots_bt]

   result2 = [(lenght_V_tp_sg_img, lenght_U_img), img_top, img_compress_top, array_convert_dots_tp]

   res = []
   if array_convert_dots_bt != []:
      res.append(result1)

   if array_convert_dots_tp != []:
      res.append(result2)



   start_rasch = time.time()

   with Pool(4) as pool:
      result = pool.map(generative, res)

   end_rasch = time.time()

   print(f"На генерацию ушло {end_rasch - start_rasch}")

   otvet = []

   for item in result[0]:
      otvet1 = {}
      otvet1["V"] = dots["BottomLeft_V"]+item["V"]*SCALE_STEP/sheet_scale_convert
      otvet1["U"] = dots["BottomLeft_U"] + item["U"] * SCALE_STEP / sheet_scale_convert
      otvet1["LeaderElbow_U"] = dots["BottomLeft_U"] + item["LeaderElbow_U"] * SCALE_STEP / sheet_scale_convert
      otvet1["LeaderElbow_V"] = dots["BottomLeft_V"] + item["LeaderElbow_V"]  * SCALE_STEP / sheet_scale_convert
      otvet1["TagId"] = item["TagId"]
      otvet.append(otvet1)


   for item in result[1]:
      otvet2 = {}
      otvet2["V"] = coordinate_V_top_segment+item["V"]*SCALE_STEP/sheet_scale_convert
      otvet2["U"] = dots["BottomLeft_U"] + item["U"] * SCALE_STEP / sheet_scale_convert
      otvet2["TagId"] = item["TagId"]

      otvet2["LeaderElbow_U"] = dots["BottomLeft_U"] + item["LeaderElbow_U"] * SCALE_STEP / sheet_scale_convert
      otvet2["LeaderElbow_V"] = dots["BottomLeft_V"] + item["LeaderElbow_V"] * SCALE_STEP / sheet_scale_convert

      otvet.append(otvet2)
   # print(otvet)


   return (json.dumps(otvet))



@app.post("/data")
async def test22222(
      scrFile: UploadFile = File(...),

      jsFile: UploadFile = File(...)
   ):

   pool_genetic = Pool(3)

   box_for_separate = (2,1)

   data = json.load(jsFile.file)

   img = Image.open(scrFile.file)

   dots= deserial_funk_for_class(data)

   Segment.scale_sheet = dots["Scale"]


   sheet_scale_convert = FT_TO_MM / Segment.scale_sheet

   print(dots)

   dots_V = []

   for item in dots['Boxes_list']:

      dots_V.append(item["LeaderEnd_V"])

   avarage_V = np.mean(dots_V)

   V_bottom_segment_lenght = avarage_V - dots["BottomLeft_V"]

   coordinate_V_top_segment = avarage_V

   lenght_V = dots["TopRight_V"] - dots["BottomLeft_V"]

   lenght_U = dots["TopRight_U"] - dots["BottomLeft_U"]

   # lenght_V_segment = lenght_V/2

   lenght_V_on_list = lenght_V * sheet_scale_convert

   lenght_U_on_list = lenght_U * sheet_scale_convert

   lenght_V_img = np.around(np.divide(lenght_V_on_list, SCALE_STEP)).astype(int)

   lenght_U_img = np.around(np.divide(lenght_U_on_list, SCALE_STEP)).astype(int)

   lenght_V_bt_sg_img = np.around(np.divide(V_bottom_segment_lenght * sheet_scale_convert, SCALE_STEP)).astype(int)

   lenght_V_tp_sg_img = lenght_V_img - lenght_V_bt_sg_img

   img_full, img_full_compress = image_generator_devide(img, lenght_V_img, SCALE_STEP, lenght_U_img)

   img_bottom, img_compress_bottom = img_full[0:lenght_V_bt_sg_img, 0:lenght_U_img], img_full_compress[0:lenght_V_bt_sg_img, 0:lenght_U_img]

   img_top, img_compress_top = img_full[lenght_V_bt_sg_img:lenght_V_img, 0:lenght_U_img], img_full_compress[
                                                                                     lenght_V_bt_sg_img:lenght_V_img,
                                                                                     0:lenght_U_img]

   # fig4 = plt.figure()
   # plt.pcolor(img_bottom, cmap="cool", edgecolors='k')
   # plt.colorbar()
   #
   # fig5 = plt.figure()
   # plt.pcolor(img_top, cmap="cool", edgecolors='k')
   # plt.colorbar()
   #
   # plt.show()


   array_bt_sg = sort_dots(dots["BottomLeft_V"], dots["BottomLeft_U"], coordinate_V_top_segment, dots["TopRight_U"],
                           dots["Boxes_list"])
   array_tp_sg = sort_dots(coordinate_V_top_segment, dots["BottomLeft_U"], dots["TopRight_V"], dots["TopRight_U"],
                           dots["Boxes_list"])

   array_convert_dots_bt = dots_to_segment_coordinates(array_bt_sg, dots["BottomLeft_V"], dots["BottomLeft_U"],
                                                        sheet_scale_convert, SCALE_STEP)

   array_convert_dots_tp = dots_to_segment_coordinates(array_tp_sg, coordinate_V_top_segment, dots["BottomLeft_U"],
                                                       sheet_scale_convert, SCALE_STEP)


   result = []
   result1 = [(lenght_V_bt_sg_img, lenght_U_img), img_bottom, img_compress_bottom, array_convert_dots_bt]

   result2 = [(lenght_V_tp_sg_img, lenght_U_img), img_top, img_compress_top, array_convert_dots_tp]

   res = []
   if array_convert_dots_bt != []:
      res.append(result1)

   if array_convert_dots_tp != []:
      res.append(result2)




   print("Флаг main 1")

   start_rasch = time.time()
   print("Флаг main 2")

   with Pool(2) as pool:
      result = pool.map(generative, res)

   print("Флаг main 3")

   end_rasch = time.time()
   print("Флаг main 4")
   print(f"На генерацию ушло {end_rasch - start_rasch}")
   print("Флаг main 5")



   otvet = []

   for item in result[0]:
      otvet1 = {}
      otvet1["V"] = dots["BottomLeft_V"]+item["V"]*SCALE_STEP/sheet_scale_convert
      otvet1["U"] = dots["BottomLeft_U"] + item["U"] * SCALE_STEP / sheet_scale_convert

      otvet1["LeaderElbow_U"] = dots["BottomLeft_U"] + item["LeaderElbow_U"] * SCALE_STEP / sheet_scale_convert
      otvet1["LeaderElbow_V"] = dots["BottomLeft_V"] + item["LeaderElbow_V"] * SCALE_STEP / sheet_scale_convert

      otvet1["TagId"] = item["TagId"]
      otvet.append(otvet1)


   for item in result[1]:
      otvet2 = {}
      otvet2["V"] = coordinate_V_top_segment+item["V"]*SCALE_STEP/sheet_scale_convert
      otvet2["U"] = dots["BottomLeft_U"] + item["U"] * SCALE_STEP / sheet_scale_convert

      otvet2["LeaderElbow_U"] = dots["BottomLeft_U"] + item["LeaderElbow_U"] * SCALE_STEP / sheet_scale_convert
      otvet2["LeaderElbow_V"] = coordinate_V_top_segment + item["LeaderElbow_V"] * SCALE_STEP / sheet_scale_convert

      otvet2["TagId"] = item["TagId"]
      otvet.append(otvet2)
   # print(otvet)







   # array_dot_for_img_bottom =
   # array_dot_for_img_top =









   print("Флаг 2")
   return (json.dumps(otvet))